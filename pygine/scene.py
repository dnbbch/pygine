"""
Scene management system
"""

from typing import Dict, Optional, Callable
from abc import ABC, abstractmethod


class Scene(ABC):
    """Base class for game scenes."""

    def __init__(self, name: str):
        self.name = name
        self.active = False

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update scene logic."""
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        """Draw scene."""
        pass

    def on_enter(self) -> None:
        """Called when scene becomes active."""
        self.active = True

    def on_exit(self) -> None:
        """Called when scene becomes inactive."""
        self.active = False


class SceneManager:
    """Manages multiple game scenes."""

    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None

    def add_scene(self, scene: Scene) -> None:
        """Add a scene."""
        self.scenes[scene.name] = scene

    def switch_to(self, scene_name: str) -> bool:
        """Switch to a specific scene."""
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()

            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter()
            return True
        return False

    def update(self, dt: float) -> None:
        """Update current scene."""
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen) -> None:
        """Draw current scene."""
        if self.current_scene:
            self.current_scene.draw(screen)
