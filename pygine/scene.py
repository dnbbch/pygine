"""
Система управления сценами
"""

from typing import Dict, Optional, Callable
from abc import ABC, abstractmethod


class Scene(ABC):
    """Базовый класс для игровых сцен."""

    def __init__(self, name: str):
        self.name = name
        self.active = False

    @abstractmethod
    def update(self, dt: float) -> None:
        """Обновить логику сцены."""
        pass

    @abstractmethod
    def draw(self, screen) -> None:
        """Отрисовать сцену."""
        pass

    def on_enter(self) -> None:
        """Вызывается, когда сцена становится активной."""
        self.active = True

    def on_exit(self) -> None:
        """Вызывается, когда сцена деактивируется."""
        self.active = False


class SceneManager:
    """Управляет несколькими игровыми сценами."""

    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None

    def add_scene(self, scene: Scene) -> None:
        """Добавить сцену."""
        self.scenes[scene.name] = scene

    def switch_to(self, scene_name: str) -> bool:
        """Переключиться на указанную сцену."""
        if scene_name in self.scenes:
            if self.current_scene:
                self.current_scene.on_exit()

            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter()
            return True
        return False

    def update(self, dt: float) -> None:
        """Обновить текущую сцену."""
        if self.current_scene:
            self.current_scene.update(dt)

    def draw(self, screen) -> None:
        """Отрисовать текущую сцену."""
        if self.current_scene:
            self.current_scene.draw(screen)
