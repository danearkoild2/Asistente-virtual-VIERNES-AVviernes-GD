"""
Bézier FFD Warp Deformers & Head Rotation Engine
================================================
Implements Free-Form Deformation (FFD) using tensor product Bernstein polynomials,
and procedural 2.5D head yaw/pitch/roll parameter synthesizers.
"""

from __future__ import annotations
import math
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from .schema import WarpDeformer, Keyform, Mesh


def _bernstein(n: int, i: int, t: float) -> float:
    """Evaluates the i-th Bernstein polynomial of degree n at parameter t."""
    if t < 0.0:
        t = 0.0
    elif t > 1.0:
        t = 1.0
    coeff = math.comb(n, i)
    return coeff * (t ** i) * ((1.0 - t) ** (n - i))


class BezierWarpDeformer:
    """
    Evaluates Free-Form Deformation (FFD) over a regular grid of control points.
    Maps local (u, v) coordinates to deformed world (x, y) coordinates.
    """

    def __init__(self, rows: int = 4, cols: int = 4, control_points: Optional[List[List[float]]] = None):
        self.rows = rows
        self.cols = cols
        self.n = rows - 1  # degree in V
        self.m = cols - 1  # degree in U

        if control_points is not None:
            self.control_points = np.array(control_points, dtype=np.float32).reshape(rows, cols, 2)
        else:
            # Default [0, 1] normalized grid
            u_coords = np.linspace(0.0, 1.0, cols)
            v_coords = np.linspace(0.0, 1.0, rows)
            grid_u, grid_v = np.meshgrid(u_coords, v_coords)
            self.control_points = np.stack([grid_u, grid_v], axis=-1).astype(np.float32)

    def evaluate_point(self, u: float, v: float) -> Tuple[float, float]:
        """Evaluates deformed position for parametric coordinate (u, v)."""
        u = max(0.0, min(1.0, u))
        v = max(0.0, min(1.0, v))

        # Precompute 1D Bernstein basis
        bu = np.array([_bernstein(self.m, j, u) for j in range(self.cols)], dtype=np.float32)
        bv = np.array([_bernstein(self.n, i, v) for i in range(self.rows)], dtype=np.float32)

        # Tensor product: sum_i sum_j bv[i] * bu[j] * C[i, j]
        # outer product: (rows, cols)
        weights = np.outer(bv, bu)  # shape (rows, cols)
        deformed_x = np.sum(weights * self.control_points[:, :, 0])
        deformed_y = np.sum(weights * self.control_points[:, :, 1])

        return float(deformed_x), float(deformed_y)

    def deform_mesh(self, mesh: Mesh) -> Mesh:
        """Applies this warp deformer to all vertices in mesh using their UVs as coordinates."""
        new_vertices = []
        for uv in mesh.uvs:
            nx, ny = self.evaluate_point(uv[0], uv[1])
            new_vertices.append([nx, ny])

        return Mesh(
            vertices=new_vertices,
            uvs=[list(u) for u in mesh.uvs],
            triangles=[list(t) for t in mesh.triangles],
            weights=mesh.weights,
        )


class HeadRotationEngine:
    """
    Synthesizes realistic 2.5D head rotation keyforms (ParamAngleX, ParamAngleY, ParamAngleZ).
    Calculates cylindrical projection and perspective foreshortening.
    """

    @staticmethod
    def generate_yaw_keyform(
        base_grid: np.ndarray,
        angle_deg: float,
        depth_factor: float = 0.35,
    ) -> List[List[float]]:
        """
        Synthesizes control point offsets for horizontal head turn (ParamAngleX: -30 to +30 deg).
        Applies cylindrical rotation: x' = cos(theta) * x + depth * sin(theta).
        """
        rad = math.radians(angle_deg)
        cos_t = math.cos(rad)
        sin_t = math.sin(rad)

        rows, cols = base_grid.shape[:2]
        center_x = (base_grid[0, 0, 0] + base_grid[0, -1, 0]) / 2.0
        width = abs(base_grid[0, -1, 0] - base_grid[0, 0, 0])

        offsets = []
        for r in range(rows):
            for c in range(cols):
                orig_x = base_grid[r, c, 0]
                orig_y = base_grid[r, c, 1]

                # Normalized relative X in [-0.5, 0.5]
                rel_x = (orig_x - center_x) / max(width, 1.0)

                # Cylindrical projection with foreshortening
                # Receding side compresses, front side shifts
                cyl_x = rel_x * cos_t + depth_factor * sin_t * (1.0 - abs(rel_x) * 0.4)
                new_x = center_x + cyl_x * width

                # Slight vertical perspective shift (spherical curving)
                cyl_y_offset = -abs(sin_t) * (rel_x ** 2) * (width * 0.12)
                new_y = orig_y + cyl_y_offset

                dx = float(new_x - orig_x)
                dy = float(new_y - orig_y)
                offsets.append([dx, dy])

        return offsets

    @staticmethod
    def generate_pitch_keyform(
        base_grid: np.ndarray,
        angle_deg: float,
        pitch_factor: float = 0.30,
    ) -> List[List[float]]:
        """
        Synthesizes control point offsets for vertical head turn (ParamAngleY: -30 to +30 deg).
        """
        rad = math.radians(angle_deg)
        sin_t = math.sin(rad)

        rows, cols = base_grid.shape[:2]
        center_y = (base_grid[0, 0, 1] + base_grid[-1, 0, 1]) / 2.0
        height = abs(base_grid[-1, 0, 1] - base_grid[0, 0, 1])

        offsets = []
        for r in range(rows):
            for c in range(cols):
                orig_x = base_grid[r, c, 0]
                orig_y = base_grid[r, c, 1]

                rel_y = (orig_y - center_y) / max(height, 1.0)

                # Up/down pitch shifts features and curves chin/forehead
                new_y = orig_y + sin_t * height * pitch_factor * (1.0 - abs(rel_y) * 0.2)
                new_x = orig_x - sin_t * rel_y * 10.0  # slight trapezoid effect

                dx = float(new_x - orig_x)
                dy = float(new_y - orig_y)
                offsets.append([dx, dy])

        return offsets
