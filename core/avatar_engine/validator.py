"""
Rig Integrity Validator & Mesh Self-Correction Engine
=====================================================
Analyzes deformed meshes for inverted triangles (mesh folding), extreme edge strain,
and applies iterative Laplacian mesh relaxation to self-correct distorted rigs.
"""

from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from .schema import Mesh, RigModel, Part


@dataclass
class MeshIntegrityReport:
    is_valid: bool
    total_triangles: int
    inverted_triangles_count: int
    inverted_triangle_indices: List[int] = field(default_factory=list)
    max_edge_strain: float = 1.0
    min_edge_strain: float = 1.0
    severe_strain_count: int = 0
    repaired: bool = False
    iterations_used: int = 0


class RigValidator:
    """Inspector and automated corrector for 2D animation meshes."""

    @staticmethod
    def calculate_triangle_signed_area(p0: np.ndarray, p1: np.ndarray, p2: np.ndarray) -> float:
        """
        Computes 2D signed area of a triangle.
        Positive: Counter-Clockwise (standard).
        Negative: Inverted / Flipped triangle (defect).
        """
        return 0.5 * float((p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1]))

    @classmethod
    def inspect_mesh(
        cls,
        rest_mesh: Mesh,
        deformed_mesh: Mesh,
        strain_threshold_max: float = 1.80,
        strain_threshold_min: float = 0.20,
    ) -> MeshIntegrityReport:
        """Exhaustively inspects deformed mesh against rest configuration."""
        rest_pts = np.array(rest_mesh.vertices, dtype=np.float32)
        def_pts = np.array(deformed_mesh.vertices, dtype=np.float32)
        triangles = rest_mesh.triangles

        if len(def_pts) != len(rest_pts) or len(triangles) == 0:
            return MeshIntegrityReport(
                is_valid=False,
                total_triangles=len(triangles),
                inverted_triangles_count=0,
            )

        inverted_indices = []
        max_strain = 1.0
        min_strain = 1.0
        severe_strain_count = 0

        # 1. Inversion Check
        for idx, tri in enumerate(triangles):
            i0, i1, i2 = tri

            # Check original orientation
            rest_area = cls.calculate_triangle_signed_area(rest_pts[i0], rest_pts[i1], rest_pts[i2])
            def_area = cls.calculate_triangle_signed_area(def_pts[i0], def_pts[i1], def_pts[i2])

            # If signs differ or deformed area collapsed to zero, triangle is inverted
            if rest_area * def_area <= 1e-7:
                inverted_indices.append(idx)

            # 2. Edge Strain Check
            edges = [(i0, i1), (i1, i2), (i2, i0)]
            for u, v in edges:
                rest_len = float(np.linalg.norm(rest_pts[u] - rest_pts[v]))
                if rest_len > 1e-4:
                    def_len = float(np.linalg.norm(def_pts[u] - def_pts[v]))
                    strain = def_len / rest_len
                    max_strain = max(max_strain, strain)
                    min_strain = min(min_strain, strain)
                    if strain > strain_threshold_max or strain < strain_threshold_min:
                        severe_strain_count += 1

        is_valid = len(inverted_indices) == 0 and severe_strain_count == 0

        return MeshIntegrityReport(
            is_valid=is_valid,
            total_triangles=len(triangles),
            inverted_triangles_count=len(inverted_indices),
            inverted_triangle_indices=inverted_indices,
            max_edge_strain=max_strain,
            min_edge_strain=min_strain,
            severe_strain_count=severe_strain_count,
            repaired=False,
            iterations_used=0,
        )

    @classmethod
    def auto_repair_mesh(
        cls,
        rest_mesh: Mesh,
        deformed_mesh: Mesh,
        max_iterations: int = 15,
        relaxation_lambda: float = 0.45,
    ) -> Tuple[Mesh, MeshIntegrityReport]:
        """
        Iteratively repairs deformed mesh by applying localized Laplacian relaxation
        to vertices participating in inverted or collapsed triangles.
        """
        report = cls.inspect_mesh(rest_mesh, deformed_mesh)
        if report.is_valid:
            return deformed_mesh, report

        rest_pts = np.array(rest_mesh.vertices, dtype=np.float32)
        pts = np.array(deformed_mesh.vertices, dtype=np.float32)
        triangles = rest_mesh.triangles
        num_vertices = len(pts)

        # Build adjacency graph
        adj: Dict[int, set] = {i: set() for i in range(num_vertices)}
        for i0, i1, i2 in triangles:
            adj[i0].add(i1)
            adj[i0].add(i2)
            adj[i1].add(i0)
            adj[i1].add(i2)
            adj[i2].add(i0)
            adj[i2].add(i1)

        iterations = 0
        while iterations < max_iterations:
            iterations += 1

            # Identify problematic vertices
            problem_vertices = set()
            for idx in report.inverted_triangle_indices:
                i0, i1, i2 = triangles[idx]
                problem_vertices.update([i0, i1, i2])

            if not problem_vertices:
                break

            # Apply local Laplacian smoothing
            new_pts = pts.copy()
            for v_idx in problem_vertices:
                neighbors = list(adj[v_idx])
                if neighbors:
                    centroid = np.mean(pts[neighbors], axis=0)
                    new_pts[v_idx] = (1.0 - relaxation_lambda) * pts[v_idx] + relaxation_lambda * centroid

            pts = new_pts

            # Re-evaluate
            candidate_mesh = Mesh(
                vertices=[[float(p[0]), float(p[1])] for p in pts],
                uvs=deformed_mesh.uvs,
                triangles=triangles,
            )
            report = cls.inspect_mesh(rest_mesh, candidate_mesh)
            if report.inverted_triangles_count == 0:
                report.repaired = True
                report.iterations_used = iterations
                return candidate_mesh, report

        report.iterations_used = iterations
        report.repaired = (report.inverted_triangles_count == 0)

        final_mesh = Mesh(
            vertices=[[float(p[0]), float(p[1])] for p in pts],
            uvs=deformed_mesh.uvs,
            triangles=triangles,
        )
        return final_mesh, report
