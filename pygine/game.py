"""
Main game class for managing the game loop and window
"""

import pygame
import sys
from typing import Tuple, Optional, Callable, List
from .utils import update_input_state


class Game:
    """
    Main game class that manages the game window, loop, and basic functionality.

    This class provides a simple interface for creating games with automatic
    game loop management, event handling, and frame rate control.

    Args:
        width: Window width in pixels
        height: Window height in pixels
        title: Window title
        fps: Target frames per second
        background_color: Background color as (R, G, B) tuple
        *,
        create_display: bool = True,

    Example:
        >>> game = Game(800, 600, "My Game")
        >>> player = AnimatedSprite("player.png", (32, 32))
        >>>
        >>> def update():
        ...     player.update()
        ...
        >>> def draw():
        ...     player.draw(game.screen)
        ...
        >>> game.run(update, draw)
    """

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "Pygame Easy Game",
        fps: int = 60,
        background_color: Tuple[int, int, int] = (50, 50, 50),
        *,
        create_display: bool = True,
    ):
        # Initialize pygame
        if not pygame.get_init():
            pygame.init()

        # Window properties
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        self.background_color = background_color

        # Создаём окно, только если об этом явно не попросили отказаться.
        if create_display:
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption(title)
        else:
            # Если пользователь уже создал окно – забираем его.
            existing = pygame.display.get_surface()
            if existing is not None:
                self.screen = existing
            else:
                # Fallback: создаём временную поверхность (off-screen).
                self.screen = pygame.Surface((width, height))

        # Game loop control
        self.clock = pygame.time.Clock()
        self.running = False
        self.paused = False

        # Delta time tracking
        self.dt = 0.0
        self.last_time = 0.0

        # Event callbacks
        self.update_callback: Optional[Callable] = None
        self.draw_callback: Optional[Callable] = None
        self.event_callbacks: List[Callable] = []

        # Sprite groups for automatic management
        self.all_sprites = pygame.sprite.Group()

        # Debug information
        self.show_fps = False
        self.font = None

    def run(
        self,
        update_func: Optional[Callable] = None,
        draw_func: Optional[Callable] = None,
    ) -> None:
        """
        Start the main game loop.

        Args:
            update_func: Function called each frame for game logic
            draw_func: Function called each frame for drawing

        Example:
            >>> def update():
            ...     # Game logic here
            ...     pass
            ...
            >>> def draw():
            ...     # Drawing code here
            ...     pass
            ...
            >>> game.run(update, draw)
        """
        self.update_callback = update_func
        self.draw_callback = draw_func
        self.running = True

        try:
            self._game_loop()
        except KeyboardInterrupt:
            pass
        finally:
            self.quit()

    def _game_loop(self) -> None:
        """Main game loop implementation."""
        while self.running:
            # Calculate delta time
            current_time = pygame.time.get_ticks() / 1000.0
            if self.last_time > 0:
                self.dt = current_time - self.last_time
            else:
                self.dt = 1.0 / self.fps
            self.last_time = current_time

            # Handle events
            self._handle_events()

            # Update input state
            update_input_state()

            if not self.paused:
                # Update game logic
                self._update()

            # Draw everything
            self._draw()

            # Maintain frame rate
            self.clock.tick(self.fps)

    def _handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.toggle_fps_display()
                elif event.key == pygame.K_PAUSE or event.key == pygame.K_p:
                    self.toggle_pause()

            # Call custom event callbacks
            for callback in self.event_callbacks:
                callback(event)

    def _update(self) -> None:
        """Update game logic."""
        # Update all sprites in the group
        self.all_sprites.update(self.dt)

        # Call custom update function
        if self.update_callback:
            self.update_callback()

    def _draw(self) -> None:
        """Draw everything to the screen."""
        # Clear screen
        self.screen.fill(self.background_color)

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Call custom draw function
        if self.draw_callback:
            self.draw_callback()

        # Draw debug information
        if self.show_fps:
            self._draw_fps()

        # Обновляем только если инициализировано окно отображения
        if pygame.display.get_init() and pygame.display.get_surface() is not None:
            pygame.display.flip()

    def _draw_fps(self) -> None:
        """Draw FPS counter."""
        if not self.font:
            self.font = pygame.font.Font(None, 36)

        fps_text = f"FPS: {int(self.clock.get_fps())}"
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        self.screen.blit(fps_surface, (10, 10))

    def add_sprite(self, sprite: pygame.sprite.Sprite) -> None:
        """
        Add a sprite to the automatic update and draw system.

        Args:
            sprite: Sprite to add
        """
        self.all_sprites.add(sprite)

    def remove_sprite(self, sprite: pygame.sprite.Sprite) -> None:
        """
        Remove a sprite from the automatic system.

        Args:
            sprite: Sprite to remove
        """
        self.all_sprites.remove(sprite)

    def add_event_callback(self, callback: Callable) -> None:
        """
        Add a custom event handler.

        Args:
            callback: Function that takes a pygame event
        """
        self.event_callbacks.append(callback)

    def set_background_color(self, color: Tuple[int, int, int]) -> None:
        """
        Set the background color.

        Args:
            color: RGB color tuple (0-255 each)
        """
        self.background_color = color

    def set_title(self, title: str) -> None:
        """
        Set the window title.

        Args:
            title: New window title
        """
        self.title = title
        pygame.display.set_caption(title)

    def set_fps(self, fps: int) -> None:
        """
        Set target frame rate.

        Args:
            fps: Target frames per second
        """
        self.fps = max(1, fps)

    def toggle_fps_display(self) -> None:
        """Toggle FPS counter display."""
        self.show_fps = not self.show_fps

    def toggle_pause(self) -> None:
        """Toggle game pause state."""
        self.paused = not self.paused

    def pause(self) -> None:
        """Pause the game."""
        self.paused = True

    def resume(self) -> None:
        """Resume the game."""
        self.paused = False

    def quit(self) -> None:
        """
        Quit the game and clean up.
        """
        self.running = False
        pygame.quit()
        sys.exit()

    def get_screen_rect(self) -> pygame.Rect:
        """
        Get screen rectangle for boundary checking.

        Returns:
            Rectangle representing screen boundaries
        """
        return pygame.Rect(0, 0, self.width, self.height)

    def get_center(self) -> Tuple[int, int]:
        """
        Get center point of the screen.

        Returns:
            Center coordinates as (x, y)
        """
        return (self.width // 2, self.height // 2)

    def is_point_on_screen(self, x: int, y: int) -> bool:
        """
        Check if a point is within screen boundaries.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if point is on screen
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def screenshot(self, filename: str = "screenshot.png") -> None:
        """
        Save a screenshot of the current screen.

        Args:
            filename: Path to save screenshot
        """
        pygame.image.save(self.screen, filename)

    def get_delta_time(self) -> float:
        """
        Get delta time (time since last frame) in seconds.

        Returns:
            Delta time in seconds
        """
        return self.dt

    def get_fps(self) -> float:
        """
        Get current frames per second.

        Returns:
            Current FPS
        """
        return self.clock.get_fps()

    def debug_info(self) -> dict:
        """
        Get debug information about the game state.

        Returns:
            Dictionary with debug information
        """
        return {
            "fps": self.get_fps(),
            "dt": self.dt,
            "running": self.running,
            "paused": self.paused,
            "sprite_count": len(self.all_sprites),
            "screen_size": (self.width, self.height),
            "background_color": self.background_color,
        }
