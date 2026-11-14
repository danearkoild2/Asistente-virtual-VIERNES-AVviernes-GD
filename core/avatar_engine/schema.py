"""
Rigging & Animation Schema for Edith 2D
=======================================
Self-contained, JSON-serializable 2D rigging representation.
Compatible with standard Live2D parameter semantics and Rev2D open layout.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class Parameter:
    id: str
    name: str
    min_val: float = -1.0
    max_val: float = 1.0
    default_val: float = 0.0
    current_val: float = 0.0

    def clamp(self, val: float) -> float:
        return max(self.min_val, min(self.max_val, val))


@dataclass
class Keyform:
    param_id: str
    param_value: float
    vertex_offsets: Optional[List[List[float]]] = None  # [[dx, dy], ...] for mesh vertices
    control_point_offsets: Optional[List[List[float]]] = None  # [[dx, dy], ...] for deformer grid
    opacity: float = 1.0
    visible: bool = True


@dataclass
class Mesh:
    vertices: List[List[float]] = field(default_factory=list)  # [[x, y], ...]
    uvs: List[List[float]] = field(default_factory=list)       # [[u, v], ...] in [0, 1]
    triangles: List[List[int]] = field(default_factory=list)   # [[i0, i1, i2], ...]
    weights: Optional[List[Dict[str, float]]] = None          # [{bone_id: weight, ...}, ...]


@dataclass
class Part:
    id: str
    name: str
    draw_order: int = 0
    texture_path: Optional[str] = None
    texture_base64: Optional[str] = None
    mesh: Mesh = field(default_factory=Mesh)
    warp_deformer_id: Optional[str] = None
    bone_id: Optional[str] = None
    opacity: float = 1.0
    visible: bool = True
    blend_mode: str = "normal"  # "normal", "multiply", "screen", "additive"
    keyforms: List[Keyform] = field(default_factory=list)


@dataclass
class WarpDeformer:
    id: str
    name: str
    rows: int = 4
    cols: int = 4
    control_points: List[List[float]] = field(default_factory=list)  # [(rows x cols), [x, y]]
    parent_id: Optional[str] = None
    keyforms: List[Keyform] = field(default_factory=list)


@dataclass
class Bone:
    id: str
    name: str
    head: List[float] = field(default_factory=lambda: [0.0, 0.0])
    tail: List[float] = field(default_factory=lambda: [0.0, 100.0])
    parent_id: Optional[str] = None
    rotation_deg: float = 0.0
    length: float = 100.0
    keyforms: List[Keyform] = field(default_factory=list)


@dataclass
class PhysicsParticle:
    pos: List[float] = field(default_factory=lambda: [0.0, 0.0])
    prev_pos: List[float] = field(default_factory=lambda: [0.0, 0.0])
    mass: float = 1.0
    pinned: bool = False


@dataclass
class PhysicsChain:
    id: str
    name: str
    source_param_id: str
    target_param_id: str
    damping: float = 0.92
    stiffness: float = 0.35
    gravity: List[float] = field(default_factory=lambda: [0.0, 9.8])
    angle_limit_deg: float = 45.0
    particles: List[PhysicsParticle] = field(default_factory=list)


@dataclass
class RigModel:
    name: str = "EdithAvatar"
    canvas_width: int = 1024
    canvas_height: int = 1024
    version: str = "2.0.0"
    parameters: Dict[str, Parameter] = field(default_factory=dict)
    parts: Dict[str, Part] = field(default_factory=dict)
    warp_deformers: Dict[str, WarpDeformer] = field(default_factory=dict)
    bones: Dict[str, Bone] = field(default_factory=dict)
    physics_chains: Dict[str, PhysicsChain] = field(default_factory=dict)

    @classmethod
    def create_standard_rig(cls, name: str = "Edith", w: int = 1024, h: int = 1024) -> RigModel:
        """Instantiates a rig pre-configured with all standard Live2D / Rev2D parameters."""
        rig = cls(name=name, canvas_width=w, canvas_height=h)

        std_params = [
            ("ParamAngleX", "Head Turn X", -30.0, 30.0, 0.0),
            ("ParamAngleY", "Head Turn Y", -30.0, 30.0, 0.0),
            ("ParamAngleZ", "Head Tilt Z", -30.0, 30.0, 0.0),
            ("ParamEyeLOpen", "Left Eye Open", 0.0, 1.0, 1.0),
            ("ParamEyeROpen", "Right Eye Open", 0.0, 1.0, 1.0),
            ("ParamEyeLSmile", "Left Eye Smile", 0.0, 1.0, 0.0),
            ("ParamEyeRSmile", "Right Eye Smile", 0.0, 1.0, 0.0),
            ("ParamEyeBallX", "Eyeball X", -1.0, 1.0, 0.0),
            ("ParamEyeBallY", "Eyeball Y", -1.0, 1.0, 0.0),
            ("ParamBrowLY", "Left Eyebrow Y", -1.0, 1.0, 0.0),
            ("ParamBrowRY", "Right Eyebrow Y", -1.0, 1.0, 0.0),
            ("ParamBrowLAngle", "Left Eyebrow Angle", -1.0, 1.0, 0.0),
            ("ParamBrowRAngle", "Right Eyebrow Angle", -1.0, 1.0, 0.0),
            ("ParamMouthOpenY", "Mouth Open", 0.0, 1.0, 0.0),
            ("ParamMouthForm", "Mouth Form", -1.0, 1.0, 0.0),
            ("ParamBodyAngleX", "Body Turn X", -10.0, 10.0, 0.0),
            ("ParamBodyAngleZ", "Body Tilt Z", -10.0, 10.0, 0.0),
            ("ParamBreath", "Breathing Cycle", 0.0, 1.0, 0.0),
            ("ParamHairFront", "Front Hair Physics", -1.0, 1.0, 0.0),
            ("ParamHairBack", "Back Hair Physics", -1.0, 1.0, 0.0),
        ]

        for pid, pname, pmin, pmax, pdef in std_params:
            rig.parameters[pid] = Parameter(
                id=pid, name=pname, min_val=pmin, max_val=pmax, default_val=pdef, current_val=pdef
            )

        return rig

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the rig hierarchy to a plain dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RigModel:
        """Constructs a RigModel from a dictionary with strict typing."""
        model = cls(
            name=data.get("name", "Avatar"),
            canvas_width=data.get("canvas_width", 1024),
            canvas_height=data.get("canvas_height", 1024),
            version=data.get("version", "2.0.0"),
        )

        for pid, pdata in data.get("parameters", {}).items():
            model.parameters[pid] = Parameter(**pdata)

        for wid, wdata in data.get("warp_deformers", {}).items():
            kfs = [Keyform(**kf) for kf in wdata.pop("keyforms", [])]
            model.warp_deformers[wid] = WarpDeformer(keyforms=kfs, **wdata)

        for bid, bdata in data.get("bones", {}).items():
            kfs = [Keyform(**kf) for kf in bdata.pop("keyforms", [])]
            model.bones[bid] = Bone(keyforms=kfs, **bdata)

        for pid, pdata in data.get("parts", {}).items():
            m_data = pdata.pop("mesh", {})
            mesh = Mesh(**m_data) if m_data else Mesh()
            kfs = [Keyform(**kf) for kf in pdata.pop("keyforms", [])]
            model.parts[pid] = Part(mesh=mesh, keyforms=kfs, **pdata)

        for cid, cdata in data.get("physics_chains", {}).items():
            particles = [PhysicsParticle(**pt) for pt in cdata.pop("particles", [])]
            model.physics_chains[cid] = PhysicsChain(particles=particles, **cdata)

        return model

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def save(self, filepath: str | Path) -> None:
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def load(cls, filepath: str | Path) -> RigModel:
        p = Path(filepath)
        data = json.loads(p.read_text(encoding="utf-8"))
        return cls.from_dict(data)
