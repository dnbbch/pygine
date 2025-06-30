"""
Basic physics system
"""

from typing import Tuple


class PhysicsBody:
    """Basic physics body for sprites."""

    def __init__(self, mass: float = 1.0, gravity: float = 400.0):
        self.mass = mass
        self.gravity = gravity
        self.velocity = [0.0, 0.0]
        self.acceleration = [0.0, 0.0]
        self.on_ground = False
        self.friction = 0.8
        self.bounce_factor = 0.7  # Коэффициент упругости (0.0 - 1.0)
        self.air_resistance = 0.99  # Сопротивление воздуха

    def apply_force(self, force_x: float, force_y: float) -> None:
        """Apply force to the body."""
        self.acceleration[0] += force_x / self.mass
        self.acceleration[1] += force_y / self.mass

    def apply_gravity(self, dt: float) -> None:
        """Apply gravity force."""
        if not self.on_ground:
            # Гравитация - постоянное ускорение вниз
            self.acceleration[1] += self.gravity

    def update(self, dt: float) -> Tuple[float, float]:
        """Update physics and return position change."""
        # Apply gravity
        self.apply_gravity(dt)

        # Update velocity
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        # Apply air resistance (затухание в воздухе)
        if not self.on_ground:
            self.velocity[0] *= self.air_resistance
            self.velocity[1] *= self.air_resistance

        # Apply friction (трение о землю)
        if self.on_ground:
            self.velocity[0] *= self.friction

        # Calculate position change
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt

        # Reset acceleration
        self.acceleration = [0.0, 0.0]

        return dx, dy

    def bounce(self, surface_normal: Tuple[float, float]) -> None:
        """Bounce off a surface with given normal vector."""
        nx, ny = surface_normal
        
        # Отражение скорости от поверхности
        dot_product = self.velocity[0] * nx + self.velocity[1] * ny
        
        self.velocity[0] = self.velocity[0] - 2 * dot_product * nx
        self.velocity[1] = self.velocity[1] - 2 * dot_product * ny
        
        # Применяем коэффициент упругости
        self.velocity[0] *= self.bounce_factor
        self.velocity[1] *= self.bounce_factor

    def set_bounce_factor(self, factor: float) -> None:
        """Set bounce factor (0.0 = no bounce, 1.0 = perfect bounce)."""
        self.bounce_factor = max(0.0, min(1.0, factor))

    def set_friction(self, friction: float) -> None:
        """Set friction factor (0.0 = no friction, 1.0 = full stop)."""
        self.friction = max(0.0, min(1.0, friction))
