"""
Система частиц и визуальных эффектов.
"""

import pygame
import random
import math
from typing import List, Tuple, Optional


class Particle:
    """Базовая частица для системы эффектов."""

    def __init__(
        self,
        x: float,
        y: float,
        velocity: Tuple[float, float] = (0, 0),
        lifetime: float = 1.0,
        color: Tuple[int, int, int] = (255, 255, 255),
    ):
        self.x = x
        self.y = y
        self.velocity = list(velocity)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = 2
        self.alive = True

    def update(self, dt: float) -> None:
        """Обновить состояние частицы."""
        if not self.alive:
            return

        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.alive = False

    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать частицу на экране."""
        if self.alive:
            pygame.draw.circle(
                screen, self.color, (int(self.x), int(self.y)), self.size
            )


class ParticleSystem:
    """Система для управления множеством частиц."""

    def __init__(self):
        self.particles: List[Particle] = []

    def add_particle(self, particle: Particle) -> None:
        """Добавить частицу в систему."""
        self.particles.append(particle)

    def update(self, dt: float) -> None:
        """Обновить все частицы."""
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)

    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать все частицы."""
        for particle in self.particles:
            particle.draw(screen)

    def clear(self) -> None:
        """Удалить все частицы."""
        self.particles.clear()


# Глобальная система частиц
_particle_system = ParticleSystem()


def create_explosion(x: float, y: float, size: int = 20) -> None:
    """Создать эффект взрыва в указанной позиции."""
    for _ in range(size):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed

        particle = Particle(
            x,
            y,
            (vx, vy),
            lifetime=random.uniform(0.5, 1.5),
            color=(255, random.randint(100, 255), 0),
        )
        _particle_system.add_particle(particle)


def create_smoke(x: float, y: float, amount: int = 10) -> None:
    """Создать эффект дыма в указанной позиции."""
    for _ in range(amount):
        vx = random.uniform(-20, 20)
        vy = random.uniform(-50, -20)

        gray = random.randint(100, 200)
        particle = Particle(
            x, y, (vx, vy), lifetime=random.uniform(1.0, 3.0), color=(gray, gray, gray)
        )
        _particle_system.add_particle(particle)


def create_sparkles(x: float, y: float, amount: int = 15) -> None:
    """Создать эффект искр в указанной позиции."""
    for _ in range(amount):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(30, 100)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed

        particle = Particle(
            x,
            y,
            (vx, vy),
            lifetime=random.uniform(0.3, 1.0),
            color=(255, 255, random.randint(100, 255)),
        )
        _particle_system.add_particle(particle)


def update_effects(dt: float) -> None:
    """Обновить все эффекты. Вызывать из игрового цикла."""
    _particle_system.update(dt)


def draw_effects(screen: pygame.Surface) -> None:
    """Отрисовать все эффекты. Вызывать из игрового цикла."""
    _particle_system.draw(screen)
