"""
Система анимации для спрайтов.
"""

import time
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Animation:
    """
    Представляет одну анимационную последовательность.

    Аргументы:
        name: Уникальный идентификатор анимации
        frames: Список индексов кадров для воспроизведения
        fps: Скорость анимации (кадров в секунду)
        loop: Зацикливать ли анимацию
    """

    name: str
    frames: List[int]
    fps: float
    loop: bool = True

    def __post_init__(self):
        """Проверяет параметры анимации после инициализации."""
        if not self.frames:
            raise ValueError(f"Animation '{self.name}' must have at least one frame")
        if self.fps <= 0:
            raise ValueError(f"Animation '{self.name}' fps must be positive")

        # Рассчитываем длительность кадра
        self.frame_duration = 1.0 / self.fps
        self.total_duration = len(self.frames) * self.frame_duration


class AnimationManager:
    """
    Управляет воспроизведением анимаций спрайтов.

    Отвечает за состояние, тайминги и переходы между различными анимациями.
    """

    def __init__(self):
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[Animation] = None
        self.current_animation_name: Optional[str] = None

        # Тайминг
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.start_time = 0.0

        # Состояние
        self.is_playing = False
        self.is_paused = False
        self.finished = False

    def add_animation(self, animation: Animation) -> None:
        """
        Добавить анимацию в менеджер.

        Аргументы:
            animation: Animation object to add
        """
        self.animations[animation.name] = animation

    def play_animation(self, name: str, restart: bool = False) -> bool:
        """
        Запустить указанную анимацию.

        Аргументы:
            name: Name of animation to play
            restart: Force restart if animation is already playing

        Returns:
            True if animation started successfully, False if not found
        """
        if name not in self.animations:
            return False

        animation = self.animations[name]

        # Check if we're already playing this animation
        if (
            self.current_animation_name == name
            and self.is_playing
            and not restart
            and not self.finished
        ):
            return True

        # Start new animation
        self.current_animation = animation
        self.current_animation_name = name
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.start_time = time.time()
        self.is_playing = True
        self.is_paused = False
        self.finished = False

        return True

    def stop(self) -> None:
        """Остановить текущую анимацию."""
        self.is_playing = False
        self.is_paused = False
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.finished = False

    def pause(self) -> None:
        """Приостановить текущую анимацию."""
        if self.is_playing:
            self.is_paused = True

    def resume(self) -> None:
        """Возобновить приостановленную анимацию."""
        if self.is_playing and self.is_paused:
            self.is_paused = False

    def update(self, dt: float) -> None:
        """
        Обновить таймер анимации и, при необходимости, переключить кадр.

        Аргументы:
            dt: Дельта‑время в секундах
        """
        if not self.is_playing or self.is_paused or not self.current_animation:
            return

        if self.finished and not self.current_animation.loop:
            return

        # Обновляем таймер
        self.frame_timer += dt

        # Проверяем, пора ли перейти к следующему кадру
        if self.frame_timer >= self.current_animation.frame_duration:
            self.frame_timer = 0.0
            self.current_frame_index += 1

            # Обрабатываем окончание анимации
            if self.current_frame_index >= len(self.current_animation.frames):
                if self.current_animation.loop:
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = len(self.current_animation.frames) - 1
                    self.finished = True
                    self.is_playing = False

    def get_current_animation(self) -> Optional[Animation]:
        """Получить текущую воспроизводимую анимацию."""
        return self.current_animation

    def get_current_frame_index(self) -> int:
        """Получить индекс текущего кадра внутри анимации."""
        return self.current_frame_index

    def is_finished(self) -> bool:
        """Проверить, завершилась ли текущая анимация (если она не зациклена)."""
        return self.finished

    def get_animation_progress(self) -> float:
        """
        Получить прогресс анимации в диапазоне от 0.0 до 1.0.

        Returns:
            Progress value (0.0 = start, 1.0 = end)
        """
        if not self.current_animation or not self.current_animation.frames:
            return 0.0

        frame_progress = self.current_frame_index / len(self.current_animation.frames)
        within_frame_progress = self.frame_timer / self.current_animation.frame_duration

        total_progress = (self.current_frame_index + within_frame_progress) / len(
            self.current_animation.frames
        )
        return min(1.0, total_progress)

    def get_animation_time_remaining(self) -> float:
        """
        Получить оставшееся время текущей анимации в секундах.

        Returns:
            Remaining time (0.0 if animation is looping or finished)
        """
        if not self.current_animation or self.current_animation.loop or self.finished:
            return 0.0

        frames_remaining = (
            len(self.current_animation.frames) - self.current_frame_index - 1
        )
        time_in_current_frame = self.current_animation.frame_duration - self.frame_timer

        return (
            frames_remaining * self.current_animation.frame_duration
            + time_in_current_frame
        )

    def has_animation(self, name: str) -> bool:
        """Проверить, существует ли анимация с таким именем."""
        return name in self.animations

    def get_animation_names(self) -> List[str]:
        """Получить список всех имён анимаций."""
        return list(self.animations.keys())

    def remove_animation(self, name: str) -> bool:
        """
        Удалить анимацию.

        Args:
            name: Name of animation to remove

        Returns:
            True if animation was removed, False if not found
        """
        if name in self.animations:
            # Останавливаем текущую анимацию, если её удаляем
            if self.current_animation_name == name:
                self.stop()

            del self.animations[name]
            return True
        return False

    def clear_animations(self) -> None:
        """Удалить все анимации."""
        self.stop()
        self.animations.clear()

    def debug_info(self) -> Dict:
        """Получить отладочную информацию о состоянии анимации."""
        return {
            "current_animation": self.current_animation_name,
            "frame_index": self.current_frame_index,
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "finished": self.finished,
            "progress": self.get_animation_progress(),
            "time_remaining": self.get_animation_time_remaining(),
            "total_animations": len(self.animations),
            "frame_timer": self.frame_timer,
        }
