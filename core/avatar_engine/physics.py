"""
Verlet Secondary Physics Engine for Edith 2D
============================================
Simulates realistic secondary dynamics (hair, clothing, ribbons, tails)
using damped Verlet particle integration, distance constraints, and angle clamping.
"""

from __future__ import annotations
import math
import numpy as np
from typing import List, Dict, Optional, Tuple
from .schema import PhysicsChain, PhysicsParticle


class VerletPhysicsEngine:
    """Real-time procedural physics solver for 2D character dynamics."""

    def __init__(self, fps: float = 60.0):
        self.dt = 1.0 / max(1.0, fps)
        self.dt2 = self.dt * self.dt
        self.gravity = np.array([0.0, 380.0], dtype=np.float32)  # px/s^2 downwards

    def step_chain(
        self,
        chain: PhysicsChain,
        root_offset_x: float = 0.0,
        root_offset_y: float = 0.0,
        external_force: Optional[np.ndarray] = None,
        iterations: int = 4,
    ) -> List[Tuple[float, float]]:
        """
        Advances one physics time step for a particle chain.
        Returns the updated [x, y] coordinates of all particles in the chain.
        """
        particles = chain.particles
        if not particles:
            return []

        ext_f = external_force if external_force is not None else np.zeros(2, dtype=np.float32)
        total_acc = self.gravity + ext_f

        # 1. Update root particle with animated anchor motion
        if particles[0].pinned:
            particles[0].pos[0] += root_offset_x
            particles[0].pos[1] += root_offset_y
            particles[0].prev_pos[0] = particles[0].pos[0]
            particles[0].prev_pos[1] = particles[0].pos[1]

        # 2. Verlet Integration on non-pinned particles
        damping = max(0.5, min(0.99, chain.damping))

        for p in particles:
            if p.pinned:
                continue

            curr = np.array(p.pos, dtype=np.float32)
            prev = np.array(p.prev_pos, dtype=np.float32)

            # Velocity term with damping
            velocity = (curr - prev) * damping

            # Next position
            next_pos = curr + velocity + total_acc * self.dt2

            p.prev_pos = [float(curr[0]), float(curr[1])]
            p.pos = [float(next_pos[0]), float(next_pos[1])]

        # 3. Solve Distance & Angular Constraints iteratively
        for _ in range(iterations):
            for i in range(len(particles) - 1):
                p0 = particles[i]
                p1 = particles[i + 1]

                delta = np.array([p1.pos[0] - p0.pos[0], p1.pos[1] - p0.pos[1]], dtype=np.float32)
                dist = np.linalg.norm(delta)
                if dist < 1e-4:
                    continue

                # Target rest distance: preserve initial distance
                rest_dist = 40.0  # nominal segment length

                diff = (dist - rest_dist) / dist

                # Relaxation
                stiffness = chain.stiffness
                correction = delta * (0.5 * diff * stiffness)

                if not p0.pinned:
                    p0.pos[0] += float(correction[0])
                    p0.pos[1] += float(correction[1])

                if not p1.pinned:
                    p1.pos[0] -= float(correction[0])
                    p1.pos[1] -= float(correction[1])

            # Angle constraint relative to vertical
            max_rad = math.radians(chain.angle_limit_deg)
            for i in range(len(particles) - 1):
                p0 = particles[i]
                p1 = particles[i + 1]
                dx = p1.pos[0] - p0.pos[0]
                dy = p1.pos[1] - p0.pos[1]
                angle = math.atan2(dx, dy)  # angle from downwards (0 = straight down)

                if abs(angle) > max_rad:
                    clamped_angle = math.copysign(max_rad, angle)
                    length = math.hypot(dx, dy)
                    p1.pos[0] = p0.pos[0] + length * math.sin(clamped_angle)
                    p1.pos[1] = p0.pos[1] + length * math.cos(clamped_angle)

        return [(float(p.pos[0]), float(p.pos[1])) for p in particles]

    @staticmethod
    def calculate_normalized_physics_output(chain: PhysicsChain) -> float:
        """
        Computes a normalized output parameter value in [-1.0, 1.0] from the tip displacement.
        """
        if len(chain.particles) < 2:
            return 0.0
        root = chain.particles[0].pos
        tip = chain.particles[-1].pos
        dx = tip[0] - root[0]
        # Normalize by chain total length (approx 120px)
        norm = dx / 60.0
        return max(-1.0, min(1.0, float(norm)))
