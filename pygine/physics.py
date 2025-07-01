"""
Базовая система физики
"""

from typing import Tuple


class PhysicsBody:
    """Базовое физическое тело для спрайтов."""

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
        """Применить силу к телу."""
        self.acceleration[0] += force_x / self.mass
        self.acceleration[1] += force_y / self.mass

    def apply_gravity(self, dt: float) -> None:
        """Применить силу гравитации."""
        if not self.on_ground:
            # Гравитация - постоянное ускорение вниз
            self.acceleration[1] += self.gravity

    def update(self, dt: float) -> Tuple[float, float]:
        """Обновить физику и вернуть изменение позиции."""
        # Применяем гравитацию
        self.apply_gravity(dt)

        # Обновляем скорость
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        # Применяем сопротивление воздуха
        if not self.on_ground:
            self.velocity[0] *= self.air_resistance
            self.velocity[1] *= self.air_resistance

        # Применяем трение о землю
        if self.on_ground:
            self.velocity[0] *= self.friction

        # Вычисляем изменение позиции
        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt

        # Сбрасываем ускорение
        self.acceleration = [0.0, 0.0]

        return dx, dy

    def bounce(self, surface_normal: Tuple[float, float]) -> None:
        """Отскочить от поверхности с заданным нормальным вектором."""
        nx, ny = surface_normal
        
        # Отражение скорости от поверхности
        dot_product = self.velocity[0] * nx + self.velocity[1] * ny
        
        self.velocity[0] = self.velocity[0] - 2 * dot_product * nx
        self.velocity[1] = self.velocity[1] - 2 * dot_product * ny
        
        # Применяем коэффициент упругости
        self.velocity[0] *= self.bounce_factor
        self.velocity[1] *= self.bounce_factor

    def set_bounce_factor(self, factor: float) -> None:
        """Задать коэффициент упругости (0.0 = без отскока, 1.0 = идеальный)."""
        self.bounce_factor = max(0.0, min(1.0, factor))

    def set_friction(self, friction: float) -> None:
        """Задать коэффициент трения (0.0 = без трения, 1.0 = полная остановка)."""
        self.friction = max(0.0, min(1.0, friction))
