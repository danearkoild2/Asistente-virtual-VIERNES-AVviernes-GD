"""
Mesh Builder for Edith 2D
=========================
Generates adaptive, boundary-conforming 2D triangular meshes from image alpha channels
using contour extraction, internal Poisson/grid point distribution, and Delaunay Triangulation.
"""

from __future__ import annotations
import cv2
import numpy as np
from scipy.spatial import Delaunay
from typing import List, Tuple, Optional
from .schema import Mesh


class MeshBuilder:
    """Creates optimized 2D meshes tailored for 2D puppet deformation."""

    @staticmethod
    def build_mesh_from_alpha(
        alpha_mask: np.ndarray,
        origin_x: float = 0.0,
        origin_y: float = 0.0,
        density: str = "medium",  # "low", "medium", "high", "facial_feature"
        contour_eps: float = 1.5,
    ) -> Mesh:
        """
        Extracts boundary contour from alpha_mask (H, W uint8), samples interior points,
        computes Delaunay Triangulation, and rejects external triangles.
        """
        h, w = alpha_mask.shape[:2]
        if w < 4 or h < 4:
            return Mesh()

        # 1. Binarize
        _, bin_mask = cv2.threshold(alpha_mask, 25, 255, cv2.THRESH_BINARY)

        # 2. Extract external contours
        contours, _ = cv2.findContours(bin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
        if not contours:
            return Mesh()

        # Pick largest contour by area
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) < 16:
            return Mesh()

        # 3. Simplify contour with Douglas-Peucker
        approx = cv2.approxPolyDP(c, contour_eps, closed=True)
        boundary_pts = approx.reshape(-1, 2).astype(np.float32)

        # 4. Determine grid sampling step based on density
        density_steps = {
            "low": max(24, min(w, h) // 8),
            "medium": max(16, min(w, h) // 14),
            "high": max(10, min(w, h) // 22),
            "facial_feature": max(6, min(w, h) // 30),
        }
        step = density_steps.get(density, 16)

        # 5. Generate interior candidate points
        x_coords = np.arange(step // 2, w, step)
        y_coords = np.arange(step // 2, h, step)
        grid_x, grid_y = np.meshgrid(x_coords, y_coords)
        candidates = np.column_stack([grid_x.ravel(), grid_y.ravel()]).astype(np.float32)

        # Filter candidates: must be strictly inside the alpha mask
        interior_pts = []
        for pt in candidates:
            ix, iy = int(round(pt[0])), int(round(pt[1]))
            if 0 <= ix < w and 0 <= iy < h:
                # Check point in polygon distance
                dist = cv2.pointPolygonTest(c, (float(pt[0]), float(pt[1])), measureDist=True)
                if dist > step * 0.45:  # safely inside boundary
                    interior_pts.append(pt)

        if interior_pts:
            all_pts = np.vstack([boundary_pts, np.array(interior_pts, dtype=np.float32)])
        else:
            all_pts = boundary_pts

        if len(all_pts) < 3:
            return Mesh()

        # 6. Delaunay Triangulation
        tri = Delaunay(all_pts)
        valid_triangles = []

        # 7. Prune triangles whose centroid lies outside the polygon
        for simplex in tri.simplices:
            p0 = all_pts[simplex[0]]
            p1 = all_pts[simplex[1]]
            p2 = all_pts[simplex[2]]
            centroid = (p0 + p1 + p2) / 3.0

            # Verify centroid lies inside alpha mask
            cx, cy = int(round(centroid[0])), int(round(centroid[1]))
            if 0 <= cx < w and 0 <= cy < h and bin_mask[cy, cx] > 0:
                # Check point in polygon
                if cv2.pointPolygonTest(c, (float(centroid[0]), float(centroid[1])), False) >= 0:
                    valid_triangles.append([int(simplex[0]), int(simplex[1]), int(simplex[2])])

        # 8. Compute global canvas vertices and normalized UVs
        vertices = []
        uvs = []
        for pt in all_pts:
            vx = float(origin_x + pt[0])
            vy = float(origin_y + pt[1])
            u = float(pt[0] / max(w - 1, 1))
            v = float(pt[1] / max(h - 1, 1))
            vertices.append([vx, vy])
            uvs.append([u, v])

        return Mesh(
            vertices=vertices,
            uvs=uvs,
            triangles=valid_triangles,
            weights=None,
        )

    @staticmethod
    def build_grid_mesh(
        origin_x: float,
        origin_y: float,
        width: float,
        height: float,
        rows: int = 4,
        cols: int = 4,
    ) -> Mesh:
        """Generates a regular rectangular quad-subdivided mesh (useful for warp deformer lattices)."""
        vertices = []
        uvs = []
        for r in range(rows + 1):
            v = r / rows
            y = origin_y + v * height
            for c in range(cols + 1):
                u = c / cols
                x = origin_x + u * width
                vertices.append([float(x), float(y)])
                uvs.append([float(u), float(v)])

        triangles = []
        for r in range(rows):
            for c in range(cols):
                i0 = r * (cols + 1) + c
                i1 = i0 + 1
                i2 = (r + 1) * (cols + 1) + c
                i3 = i2 + 1
                # Two triangles per quad
                triangles.append([i0, i1, i2])
                triangles.append([i1, i3, i2])

        return Mesh(vertices=vertices, uvs=uvs, triangles=triangles)
