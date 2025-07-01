"""
pygine — упрощённая библиотека поверх pygame для обучения разработке игр

Универсальная библиотека, которая упрощает создание игр с использованием
pygame. Предназначена для образовательных целей и быстрого прототипирования.
"""

__version__ = "1.0.0"
__author__ = "pygine contributors"

# Основные импорты
from .sprite import AnimatedSprite
from .animation import Animation, AnimationManager
from .game import Game
from .utils import (
    wait,
    wait_for_key,
    wait_for_click,
    wait_for_animation,
    get_mouse_pos,
    get_mouse_pressed,
    key_pressed,
    key_just_pressed,
    key_just_released,
    normalize_vector,
    lerp,
    clamp,
)
from .effects import (
    Particle,
    ParticleSystem,
    create_explosion,
    create_smoke,
    create_sparkles,
    start_screen_shake,
    get_screen_shake_offset,
    is_screen_shaking,
)
from .ui import UIElement, Button, HealthBar, ProgressBar, Text, Panel, TextInput, draw_rounded_rect, draw_rounded_rect_border
from .camera import Camera
from .scene import Scene, SceneManager
from .physics import PhysicsBody
from .spritesheet_tools import visualize_spritesheet, create_spritesheet_from_frames

# Экспорт основных классов и функций
__all__ = [
    # Базовые классы
    "AnimatedSprite",
    "Animation",
    "AnimationManager",
    "Game",
    # Утилитарные функции
    "wait",
    "wait_for_key",
    "wait_for_click",
    "wait_for_animation",
    "get_mouse_pos",
    "get_mouse_pressed",
    "key_pressed",
    "key_just_pressed",
    "key_just_released",
    "normalize_vector",
    "lerp",
    "clamp",
    # Эффекты
    "Particle",
    "ParticleSystem",
    "create_explosion",
    "create_smoke",
    "create_sparkles",
    "start_screen_shake",
    "get_screen_shake_offset",
    "is_screen_shaking",
    # Компоненты интерфейса
    "UIElement",
    "Button",
    "HealthBar",
    "ProgressBar",
    "Text",
    "Panel",
    "TextInput",
    "draw_rounded_rect",
    "draw_rounded_rect_border",
    # Расширенные возможности
    "Camera",
    "Scene",
    "SceneManager",
    "PhysicsBody",
    # Инструменты для спрайтшитов
    "visualize_spritesheet",
    "create_spritesheet_from_frames",
]

# ---------------------------------------------------------------------------
# Обратная совместимость: поддержка старого импорта "import pygame_easy as ..."
# ---------------------------------------------------------------------------
import sys as _sys, importlib as _importlib

# Публикуем пакет под старым именем
_sys.modules["pygame_easy"] = _sys.modules[__name__]

# И подмодули тоже
_submodules = [
    "animation",
    "sprite",
    "game",
    "utils",
    "effects",
    "ui",
    "camera",
    "scene",
    "physics",
    "spritesheet_tools",
]

for _sub in _submodules:
    _sys.modules[f"pygame_easy.{_sub}"] = _importlib.import_module(f".{_sub}", __name__)
del _sys, _importlib, _submodules
