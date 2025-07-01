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


class ScreenShake:
    """Система тряски экрана для создания эффектов воздействия."""

    def __init__(self):
        self.intensity = 0.0  # Текущая интенсивность тряски
        self.duration = 0.0   # Оставшееся время тряски
        self.frequency = 30.0 # Частота тряски (в герцах)
        self.time = 0.0       # Внутренний таймер
        
    def start_shake(self, intensity: float, duration: float, frequency: float = 30.0) -> None:
        """
        Начать эффект тряски экрана.
        
        Аргументы:
            intensity: Интенсивность тряски (в пикселях)
            duration: Продолжительность тряски (в секундах)
            frequency: Частота тряски (колебаний в секунду)
        """
        self.intensity = max(intensity, self.intensity)  # Берём максимальную интенсивность
        self.duration = max(duration, self.duration)     # Продлеваем время, если нужно
        self.frequency = frequency
        
    def update(self, dt: float) -> None:
        """Обновить состояние тряски."""
        if self.duration > 0:
            self.duration -= dt
            self.time += dt
            
            # Уменьшаем интенсивность со временем
            if self.duration <= 0:
                self.intensity = 0.0
                self.duration = 0.0
                self.time = 0.0
            
    def get_offset(self) -> Tuple[float, float]:
        """
        Получить текущее смещение для тряски.
        
        Возвращает:
            Кортеж (offset_x, offset_y) в пикселях
        """
        if self.duration <= 0 or self.intensity <= 0:
            return (0.0, 0.0)
            
        # Создаём случайное смещение на основе времени и частоты
        angle = self.time * self.frequency * 2 * math.pi
        random_factor = random.uniform(0.7, 1.0)  # Добавляем случайность
        
        offset_x = math.sin(angle) * self.intensity * random_factor
        offset_y = math.cos(angle * 1.3) * self.intensity * random_factor  # Разная частота для Y
        
        return (offset_x, offset_y)
        
    def is_active(self) -> bool:
        """Проверить, активна ли тряска."""
        return self.duration > 0 and self.intensity > 0


# Глобальная система частиц
_particle_system = ParticleSystem()

# Глобальная система тряски экрана
_screen_shake = ScreenShake()


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


def start_screen_shake(intensity: float, duration: float, frequency: float = 30.0) -> None:
    """
    Запустить эффект тряски экрана.
    
    Аргументы:
        intensity: Интенсивность тряски (в пикселях, рекомендуется 1-10)
        duration: Продолжительность тряски (в секундах)
        frequency: Частота тряски (колебаний в секунду, по умолчанию 30)
    
    Пример:
        >>> start_screen_shake(5, 0.5)  # Средняя тряска на полсекунды
        >>> start_screen_shake(10, 1.0, 20)  # Сильная тряска на секунду с низкой частотой
    """
    _screen_shake.start_shake(intensity, duration, frequency)


def get_screen_shake_offset() -> Tuple[float, float]:
    """
    Получить текущее смещение для тряски экрана.
    
    Возвращает:
        Кортеж (offset_x, offset_y) в пикселях для применения к камере или отрисовке
    """
    return _screen_shake.get_offset()


def is_screen_shaking() -> bool:
    """
    Проверить, активна ли тряска экрана.
    
    Возвращает:
        True, если тряска активна
    """
    return _screen_shake.is_active()


def update_effects(dt: float) -> None:
    """Обновить все эффекты. Вызывать из игрового цикла."""
    _particle_system.update(dt)
    _screen_shake.update(dt)


def draw_effects(screen: pygame.Surface) -> None:
    """Отрисовать все эффекты. Вызывать из игрового цикла."""
    _particle_system.draw(screen)
