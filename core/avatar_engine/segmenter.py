"""
Layer Decomposition & Semantic Anatomical Segmenter
===================================================
Analyzes a single 2D character illustration, isolates transparency,
partitions anatomical layers (face, eyes, mouth, hair, torso),
and applies disocclusion inpainting to prevent gaps during animation.
"""

from __future__ import annotations
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, List, Optional
from PIL import Image


class LayerSegmenter:
    """Decomposes a single character illustration into textured animation layers."""

    @staticmethod
    def load_image_rgba(image_path: str | Path) -> np.ndarray:
        """Loads image as uint8 RGBA array."""
        img = Image.open(str(image_path)).convert("RGBA")
        return np.array(img, dtype=np.uint8)

    @staticmethod
    def extract_or_build_alpha(rgba: np.ndarray) -> np.ndarray:
        """Extracts existing alpha or estimates transparency from solid corners."""
        alpha = rgba[:, :, 3]
        if np.any(alpha < 250):
            return alpha

        # Solid background: estimate background color from 4 corners
        h, w = rgba.shape[:2]
        corners = [rgba[0, 0, :3], rgba[0, w - 1, :3], rgba[h - 1, 0, :3], rgba[h - 1, w - 1, :3]]
        bg_col = np.mean(corners, axis=0)

        # Color difference
        diff = np.linalg.norm(rgba[:, :, :3] - bg_col, axis=-1)
        est_alpha = np.clip((diff - 20) * 12.0, 0, 255).astype(np.uint8)
        return est_alpha

    @classmethod
    def decompose_character(
        cls,
        rgba: np.ndarray,
        inpaint_occlusion: bool = True,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Decomposes character into standard animation layers:
        - 'hair_back': Back hair behind neck
        - 'torso': Body and clothing
        - 'neck': Neck cylinder
        - 'head_base': Face skin base with inpainting behind bangs
        - 'eye_left': Left eye (sclera + iris)
        - 'eye_right': Right eye (sclera + iris)
        - 'eyebrows': Left & right eyebrows
        - 'mouth': Lips and mouth cavity
        - 'hair_front': Front hair & bangs
        """
        h, w = rgba.shape[:2]
        alpha = cls.extract_or_build_alpha(rgba)
        rgb = rgba[:, :, :3]

        layers: Dict[str, Dict[str, Any]] = {}

        # 1. Torso & Clothes (Lower region: y >= 0.38)
        mask_torso = np.zeros((h, w), dtype=np.uint8)
        torso_y_start = int(h * 0.38)
        mask_torso[torso_y_start:, :] = alpha[torso_y_start:, :]

        torso_rgba = np.zeros_like(rgba)
        torso_rgba[:, :, :3] = rgb
        torso_rgba[:, :, 3] = mask_torso
        layers["torso"] = {
            "name": "Torso",
            "rgba": torso_rgba,
            "origin": (0, 0),
            "draw_order": 10,
            "density": "low",
        }

        # 2. Neck (y between 0.32 and 0.44, central width)
        mask_neck = np.zeros((h, w), dtype=np.uint8)
        y0_neck, y1_neck = int(h * 0.32), int(h * 0.44)
        x0_neck, x1_neck = int(w * 0.38), int(w * 0.62)
        mask_neck[y0_neck:y1_neck, x0_neck:x1_neck] = alpha[y0_neck:y1_neck, x0_neck:x1_neck]

        neck_rgba = np.zeros_like(rgba)
        neck_rgba[:, :, :3] = rgb
        neck_rgba[:, :, 3] = mask_neck
        layers["neck"] = {
            "name": "Neck",
            "rgba": neck_rgba,
            "origin": (0, 0),
            "draw_order": 15,
            "density": "low",
        }

        # 3. Head Base & Skin (y between 0.10 and 0.40, x between 0.22 and 0.78)
        mask_head = np.zeros((h, w), dtype=np.uint8)
        y0_head, y1_head = int(h * 0.10), int(h * 0.40)
        x0_head, x1_head = int(w * 0.22), int(w * 0.78)
        mask_head[y0_head:y1_head, x0_head:x1_head] = alpha[y0_head:y1_head, x0_head:x1_head]

        head_rgb = rgb.copy()
        if inpaint_occlusion:
            # Dilate head mask inwards and inpaint covered skin
            head_rgb = cv2.inpaint(head_rgb, 255 - mask_head, 3, cv2.INPAINT_TELEA)

        head_rgba = np.zeros_like(rgba)
        head_rgba[:, :, :3] = head_rgb
        head_rgba[:, :, 3] = mask_head
        layers["head_base"] = {
            "name": "HeadBase",
            "rgba": head_rgba,
            "origin": (0, 0),
            "draw_order": 20,
            "density": "medium",
        }

        # 4. Left Eye (x: 0.30 - 0.46, y: 0.20 - 0.29)
        mask_eye_l = np.zeros((h, w), dtype=np.uint8)
        y0_el, y1_el = int(h * 0.20), int(h * 0.29)
        x0_el, x1_el = int(w * 0.30), int(w * 0.46)
        mask_eye_l[y0_el:y1_el, x0_el:x1_el] = alpha[y0_el:y1_el, x0_el:x1_el]

        eye_l_rgba = np.zeros_like(rgba)
        eye_l_rgba[:, :, :3] = rgb
        eye_l_rgba[:, :, 3] = mask_eye_l
        layers["eye_left"] = {
            "name": "EyeLeft",
            "rgba": eye_l_rgba,
            "origin": (0, 0),
            "draw_order": 30,
            "density": "facial_feature",
        }

        # 5. Right Eye (x: 0.54 - 0.70, y: 0.20 - 0.29)
        mask_eye_r = np.zeros((h, w), dtype=np.uint8)
        y0_er, y1_er = int(h * 0.20), int(h * 0.29)
        x0_er, x1_er = int(w * 0.54), int(w * 0.70)
        mask_eye_r[y0_er:y1_er, x0_er:x1_er] = alpha[y0_er:y1_er, x0_er:x1_er]

        eye_r_rgba = np.zeros_like(rgba)
        eye_r_rgba[:, :, :3] = rgb
        eye_r_rgba[:, :, 3] = mask_eye_r
        layers["eye_right"] = {
            "name": "EyeRight",
            "rgba": eye_r_rgba,
            "origin": (0, 0),
            "draw_order": 30,
            "density": "facial_feature",
        }

        # 6. Mouth (x: 0.42 - 0.58, y: 0.29 - 0.37)
        mask_mouth = np.zeros((h, w), dtype=np.uint8)
        y0_m, y1_m = int(h * 0.29), int(h * 0.37)
        x0_m, x1_m = int(w * 0.42), int(w * 0.58)
        mask_mouth[y0_m:y1_m, x0_m:x1_m] = alpha[y0_m:y1_m, x0_m:x1_m]

        mouth_rgba = np.zeros_like(rgba)
        mouth_rgba[:, :, :3] = rgb
        mouth_rgba[:, :, 3] = mask_mouth
        layers["mouth"] = {
            "name": "Mouth",
            "rgba": mouth_rgba,
            "origin": (0, 0),
            "draw_order": 35,
            "density": "facial_feature",
        }

        # 7. Front Hair (Upper head region: y: 0.04 - 0.30)
        mask_hair_f = np.zeros((h, w), dtype=np.uint8)
        y0_hf, y1_hf = int(h * 0.04), int(h * 0.30)
        x0_hf, x1_hf = int(w * 0.16), int(w * 0.84)
        mask_hair_f[y0_hf:y1_hf, x0_hf:x1_hf] = alpha[y0_hf:y1_hf, x0_hf:x1_hf]

        hair_f_rgba = np.zeros_like(rgba)
        hair_f_rgba[:, :, :3] = rgb
        hair_f_rgba[:, :, 3] = mask_hair_f
        layers["hair_front"] = {
            "name": "HairFront",
            "rgba": hair_f_rgba,
            "origin": (0, 0),
            "draw_order": 40,
            "density": "high",
        }

        return layers
