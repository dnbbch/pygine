"""
pygine - Simplified pygame library for game development education

A comprehensive library that simplifies game development with pygame,
designed for educational purposes and easy prototyping.
"""

__version__ = "1.0.0"
__author__ = "pygine contributors"

# Core imports
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
)
from .ui import UIElement, Button, HealthBar, ProgressBar, Text, Panel
from .camera import Camera
from .scene import Scene, SceneManager
from .physics import PhysicsBody
from .spritesheet_tools import visualize_spritesheet, create_spritesheet_from_frames

# Export all main classes and functions
__all__ = [
    # Core classes
    "AnimatedSprite",
    "Animation",
    "AnimationManager",
    "Game",
    # Utility functions
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
    # Effects
    "Particle",
    "ParticleSystem",
    "create_explosion",
    "create_smoke",
    "create_sparkles",
    # UI components
    "UIElement",
    "Button",
    "HealthBar",
    "ProgressBar",
    "Text",
    "Panel",
    # Advanced features
    "Camera",
    "Scene",
    "SceneManager",
    "PhysicsBody",
    # Spritesheet tools
    "visualize_spritesheet",
    "create_spritesheet_from_frames",
]

# ---------------------------------------------------------------------------
# Backward compatibility: allow "import pygame_easy as ..." to keep working
# ---------------------------------------------------------------------------
import sys as _sys, importlib as _importlib

# Expose this package under the old name
_sys.modules["pygame_easy"] = _sys.modules[__name__]

# Expose submodules too
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
