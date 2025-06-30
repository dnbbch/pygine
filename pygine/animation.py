"""
Animation system for sprite animations
"""

import time
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class Animation:
    """
    Represents a single animation sequence.

    Args:
        name: Unique identifier for the animation
        frames: List of frame indices to play
        fps: Animation speed in frames per second
        loop: Whether animation should repeat
    """

    name: str
    frames: List[int]
    fps: float
    loop: bool = True

    def __post_init__(self):
        """Validate animation parameters after initialization."""
        if not self.frames:
            raise ValueError(f"Animation '{self.name}' must have at least one frame")
        if self.fps <= 0:
            raise ValueError(f"Animation '{self.name}' fps must be positive")

        # Calculate frame duration
        self.frame_duration = 1.0 / self.fps
        self.total_duration = len(self.frames) * self.frame_duration


class AnimationManager:
    """
    Manages animation playback for sprites.

    Handles animation state, timing, and transitions between different animations.
    """

    def __init__(self):
        self.animations: Dict[str, Animation] = {}
        self.current_animation: Optional[Animation] = None
        self.current_animation_name: Optional[str] = None

        # Timing
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.start_time = 0.0

        # State
        self.is_playing = False
        self.is_paused = False
        self.finished = False

    def add_animation(self, animation: Animation) -> None:
        """
        Add an animation to the manager.

        Args:
            animation: Animation object to add
        """
        self.animations[animation.name] = animation

    def play_animation(self, name: str, restart: bool = False) -> bool:
        """
        Play a specific animation.

        Args:
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
        """Stop current animation."""
        self.is_playing = False
        self.is_paused = False
        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.finished = False

    def pause(self) -> None:
        """Pause current animation."""
        if self.is_playing:
            self.is_paused = True

    def resume(self) -> None:
        """Resume paused animation."""
        if self.is_playing and self.is_paused:
            self.is_paused = False

    def update(self, dt: float) -> None:
        """
        Update animation timing and frame.

        Args:
            dt: Delta time in seconds
        """
        if not self.is_playing or self.is_paused or not self.current_animation:
            return

        if self.finished and not self.current_animation.loop:
            return

        # Update timer
        self.frame_timer += dt

        # Check if it's time for next frame
        if self.frame_timer >= self.current_animation.frame_duration:
            self.frame_timer = 0.0
            self.current_frame_index += 1

            # Handle animation end
            if self.current_frame_index >= len(self.current_animation.frames):
                if self.current_animation.loop:
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = len(self.current_animation.frames) - 1
                    self.finished = True
                    self.is_playing = False

    def get_current_animation(self) -> Optional[Animation]:
        """Get the currently playing animation."""
        return self.current_animation

    def get_current_frame_index(self) -> int:
        """Get current frame index within the animation."""
        return self.current_frame_index

    def is_finished(self) -> bool:
        """Check if current animation has finished (for non-looping animations)."""
        return self.finished

    def get_animation_progress(self) -> float:
        """
        Get animation progress as a value between 0.0 and 1.0.

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
        Get remaining time for current animation in seconds.

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
        """Check if animation exists."""
        return name in self.animations

    def get_animation_names(self) -> List[str]:
        """Get list of all animation names."""
        return list(self.animations.keys())

    def remove_animation(self, name: str) -> bool:
        """
        Remove an animation.

        Args:
            name: Name of animation to remove

        Returns:
            True if animation was removed, False if not found
        """
        if name in self.animations:
            # Stop current animation if it's the one being removed
            if self.current_animation_name == name:
                self.stop()

            del self.animations[name]
            return True
        return False

    def clear_animations(self) -> None:
        """Remove all animations."""
        self.stop()
        self.animations.clear()

    def debug_info(self) -> Dict:
        """Get debug information about animation state."""
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
