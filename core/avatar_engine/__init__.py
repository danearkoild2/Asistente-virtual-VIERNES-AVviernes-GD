"""
Edith 2D AI Rigging & Animation Engine
======================================
Next-generation 2D avatar pipeline: semantic layer decomposition,
occlusion inpainting, adaptive CDT mesh generation, Bézier FFD warp deformers,
Verlet secondary physics, and agent-driven self-correction.
"""

from .schema import RigModel, Part, Mesh, WarpDeformer, Bone, Parameter, Keyform, PhysicsChain
from .mesh_builder import MeshBuilder
from .deformer import BezierWarpDeformer, HeadRotationEngine
from .physics import VerletPhysicsEngine
from .validator import RigValidator, MeshIntegrityReport
from .segmenter import LayerSegmenter
from .autorigger import AutoRigger

__all__ = [
    "RigModel",
    "Part",
    "Mesh",
    "WarpDeformer",
    "Bone",
    "Parameter",
    "Keyform",
    "PhysicsChain",
    "MeshBuilder",
    "BezierWarpDeformer",
    "HeadRotationEngine",
    "VerletPhysicsEngine",
    "RigValidator",
    "MeshIntegrityReport",
    "LayerSegmenter",
    "AutoRigger",
]
