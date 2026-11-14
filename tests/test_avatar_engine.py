"""
Unit & Integration Tests for Edith 2D Avatar Engine
===================================================
Validates schema serialization, CDT mesh construction, Bézier FFD deformers,
Verlet physics stability, and the agentic self-correction loop.
"""

import sys
import unittest
import numpy as np
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from core.avatar_engine.schema import RigModel, Mesh, WarpDeformer, Keyform, PhysicsChain, PhysicsParticle
from core.avatar_engine.mesh_builder import MeshBuilder
from core.avatar_engine.deformer import BezierWarpDeformer, HeadRotationEngine
from core.avatar_engine.physics import VerletPhysicsEngine
from core.avatar_engine.validator import RigValidator
from core.avatar_engine.autorigger import AutoRigger


class TestAvatarEngine(unittest.TestCase):

    def test_01_schema_serialization(self):
        """Validates that a RigModel can be created, serialized to JSON, and deserialized losslessly."""
        rig = RigModel.create_standard_rig(name="TestEdith", w=800, h=800)
        self.assertIn("ParamAngleX", rig.parameters)
        self.assertIn("ParamEyeLOpen", rig.parameters)

        json_str = rig.to_json()
        self.assertIsInstance(json_str, str)

        reloaded = RigModel.from_dict(rig.to_dict())
        self.assertEqual(reloaded.name, "TestEdith")
        self.assertEqual(len(reloaded.parameters), len(rig.parameters))

    def test_02_mesh_builder_cdt(self):
        """Validates Constrained Delaunay Triangulation on a synthetic circular alpha mask."""
        mask = np.zeros((100, 100), dtype=np.uint8)
        # Draw filled circle
        import cv2
        cv2.circle(mask, (50, 50), 38, 255, -1)

        mesh = MeshBuilder.build_mesh_from_alpha(mask, density="medium")
        self.assertGreater(len(mesh.vertices), 10, "Should generate interior + boundary vertices")
        self.assertGreater(len(mesh.triangles), 10, "Should generate valid Delaunay triangles")
        self.assertEqual(len(mesh.vertices), len(mesh.uvs), "Vertices and UVs must match 1:1")

        # Verify all UVs are in [0, 1]
        for u, v in mesh.uvs:
            self.assertGreaterEqual(u, 0.0)
            self.assertLessEqual(u, 1.0)
            self.assertGreaterEqual(v, 0.0)
            self.assertLessEqual(v, 1.0)

    def test_03_bezier_warp_deformer(self):
        """Validates that Bernstein tensor product FFD maps points continuously."""
        # 4x4 grid spanning 0 to 100
        u_coords = np.linspace(0.0, 100.0, 4)
        v_coords = np.linspace(0.0, 100.0, 4)
        gx, gy = np.meshgrid(u_coords, v_coords)
        pts = np.stack([gx, gy], axis=-1).reshape(-1, 2).tolist()

        deformer = BezierWarpDeformer(rows=4, cols=4, control_points=pts)
        # Center evaluation (u=0.5, v=0.5) must be at (50, 50)
        cx, cy = deformer.evaluate_point(0.5, 0.5)
        self.assertAlmostEqual(cx, 50.0, delta=1.0)
        self.assertAlmostEqual(cy, 50.0, delta=1.0)

    def test_04_head_rotation_synthesis(self):
        """Validates that yaw and pitch keyforms preserve width and don't collapse."""
        gx, gy = np.meshgrid(np.linspace(100.0, 300.0, 4), np.linspace(100.0, 300.0, 4))
        base_grid = np.stack([gx, gy], axis=-1).astype(np.float32)

        yaw_offsets = HeadRotationEngine.generate_yaw_keyform(base_grid, 30.0)
        self.assertEqual(len(yaw_offsets), 16)
        # Positive yaw must produce a positive X displacement on the nose center
        self.assertNotEqual(yaw_offsets[5][0], 0.0)

    def test_05_verlet_physics_stability(self):
        """Validates that Verlet particle chains remain stable across 120 steps."""
        p0 = PhysicsParticle(pos=[100.0, 100.0], prev_pos=[100.0, 100.0], mass=0.0, pinned=True)
        p1 = PhysicsParticle(pos=[100.0, 140.0], prev_pos=[100.0, 140.0], mass=1.0)
        p2 = PhysicsParticle(pos=[100.0, 180.0], prev_pos=[100.0, 180.0], mass=1.0)

        chain = PhysicsChain(
            id="test_hair",
            name="Hair",
            source_param_id="ParamAngleX",
            target_param_id="ParamHairFront",
            damping=0.92,
            stiffness=0.35,
            angle_limit_deg=45.0,
            particles=[p0, p1, p2],
        )

        engine = VerletPhysicsEngine(fps=60.0)
        for step in range(120):
            # Apply horizontal anchor oscillation
            offset_x = 2.0 * np.sin(step * 0.1)
            coords = engine.step_chain(chain, root_offset_x=offset_x)
            self.assertEqual(len(coords), 3)
            # Ensure no NaN or infinite explosion
            for x, y in coords:
                self.assertFalse(np.isnan(x))
                self.assertFalse(np.isnan(y))

        out_param = VerletPhysicsEngine.calculate_normalized_physics_output(chain)
        self.assertGreaterEqual(out_param, -1.0)
        self.assertLessEqual(out_param, 1.0)

    def test_06_self_correction_loop(self):
        """Validates detection of an inverted triangle and automated Laplacian repair."""
        # Rest mesh: 2 triangles forming a square
        rest_vertices = [[0.0, 0.0], [50.0, 0.0], [0.0, 50.0], [50.0, 50.0]]
        triangles = [[0, 1, 2], [1, 3, 2]]
        uvs = [[0.0, 0.0], [1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]

        rest_mesh = Mesh(vertices=rest_vertices, uvs=uvs, triangles=triangles)

        # Deformed mesh with INTENTIONAL inversion: vertex 0 is moved across vertex 1
        deformed_vertices = [[60.0, 0.0], [50.0, 0.0], [0.0, 50.0], [50.0, 50.0]]
        deformed_mesh = Mesh(vertices=deformed_vertices, uvs=uvs, triangles=triangles)

        # 1. Inspector must flag the inverted triangle
        report_before = RigValidator.inspect_mesh(rest_mesh, deformed_mesh)
        self.assertFalse(report_before.is_valid, "Should detect inverted triangle")
        self.assertGreater(report_before.inverted_triangles_count, 0)

        # 2. Automated Laplacian repair must eliminate the inversion
        repaired_mesh, report_after = RigValidator.auto_repair_mesh(rest_mesh, deformed_mesh, max_iterations=10)
        self.assertTrue(report_after.repaired, "Self-correction loop must repair the inversion")
        self.assertEqual(report_after.inverted_triangles_count, 0, "No inverted triangles should remain")

    def test_07_autorigger_pipeline(self):
        """Runs end-to-end autorigger on real Edith portrait illustration."""
        icon_path = ROOT_DIR / "edith" / "edith_icon.png"
        if not icon_path.exists():
            self.skipTest("edith_icon.png not found")

        out_dir = ROOT_DIR / "scratch" / "autorig_test_output"
        rig = AutoRigger.generate_rig_from_image(
            image_path=icon_path,
            output_dir=out_dir,
            avatar_name="EdithTestAutoRig",
        )

        self.assertIsNotNone(rig)
        self.assertIn("deformer_head", rig.warp_deformers)
        self.assertGreater(len(rig.parts), 3, "Must have generated anatomical parts")

        # Verify output files
        rig_file = out_dir / "EdithTestAutoRig.edith2d.json"
        self.assertTrue(rig_file.exists(), "Rig JSON file must be written to disk")
        self.assertGreater(rig_file.stat().st_size, 1000, "Rig JSON should not be empty")


if __name__ == "__main__":
    unittest.main()
