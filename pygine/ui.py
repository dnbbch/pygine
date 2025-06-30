"""
User interface components
"""

import pygame
from typing import Tuple, Optional, Callable
from abc import ABC, abstractmethod


class UIElement(ABC):
    """Base class for all UI elements."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True

    @abstractmethod
    def update(self, dt: float) -> None:
        """Update UI element."""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Draw UI element."""
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input event. Return True if event was consumed."""
        return False


class Button(UIElement):
    """Simple button UI element."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str = "",
        callback: Optional[Callable] = None,
        font_size: int = 36,
        font_path: Optional[str] = None,
        color: Tuple[int, int, int] = (100, 100, 100),
        hover_color: Tuple[int, int, int] = (150, 150, 150),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        border_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font_size = font_size
        self.font_path = font_path
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.hovered = False
        self.pressed = False

        # Create font
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, font_size)
            except:
                self.font = pygame.font.Font(None, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)

    def update(self, dt: float) -> None:
        """Update button state."""
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw button."""
        if not self.visible:
            return

        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def set_font_size(self, size: int) -> None:
        """Change font size."""
        self.font_size = size
        if self.font_path:
            try:
                self.font = pygame.font.Font(self.font_path, size)
            except:
                self.font = pygame.font.Font(None, size)
        else:
            self.font = pygame.font.Font(None, size)

    def set_font(self, font_path: str) -> None:
        """Change font file."""
        self.font_path = font_path
        try:
            self.font = pygame.font.Font(font_path, self.font_size)
        except:
            self.font = pygame.font.Font(None, self.font_size)

    def set_colors(
        self,
        color: Tuple[int, int, int] = None,
        hover_color: Tuple[int, int, int] = None,
        text_color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
    ) -> None:
        """Change button colors."""
        if color is not None:
            self.color = color
        if hover_color is not None:
            self.hover_color = hover_color
        if text_color is not None:
            self.text_color = text_color
        if border_color is not None:
            self.border_color = border_color

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events."""
        if not self.enabled or not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed and self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                self.pressed = False
                return True
            # Отпустили кнопку вне области – просто сбросим состояние
            self.pressed = False

        # Если мышь уходит за пределы кнопки во время удержания – сбросим флаг pressed
        elif event.type == pygame.MOUSEMOTION:
            if self.pressed and not self.rect.collidepoint(event.pos):
                self.pressed = False

        return False


class HealthBar(UIElement):
    """Health/progress bar UI element."""

    def __init__(self, x: int, y: int, width: int, height: int, max_value: float = 100):
        super().__init__(x, y, width, height)
        self.max_value = max_value
        self.current_value = max_value
        self.background_color = (50, 50, 50)
        self.fill_color = (0, 255, 0)
        self.border_color = (255, 255, 255)

    def update(self, dt: float) -> None:
        """Update health bar."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw health bar."""
        if not self.visible:
            return

        # Draw background
        pygame.draw.rect(screen, self.background_color, self.rect)

        # Draw fill
        if self.current_value > 0:
            fill_width = int((self.current_value / self.max_value) * self.rect.width)
            fill_rect = pygame.Rect(
                self.rect.x, self.rect.y, fill_width, self.rect.height
            )
            pygame.draw.rect(screen, self.fill_color, fill_rect)

        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

    def set_value(self, value: float) -> None:
        """Set current value."""
        self.current_value = max(0, min(self.max_value, value))

    def get_percentage(self) -> float:
        """Get value as percentage (0.0 to 1.0)."""
        return self.current_value / self.max_value if self.max_value > 0 else 0

    def set_colors(
        self,
        background_color: Tuple[int, int, int] = None,
        fill_color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
    ) -> None:
        """Change bar colors."""
        if background_color is not None:
            self.background_color = background_color
        if fill_color is not None:
            self.fill_color = fill_color
        if border_color is not None:
            self.border_color = border_color


class ProgressBar(HealthBar):
    """Progress bar (alias for HealthBar)."""

    def __init__(self, x: int, y: int, width: int, height: int, max_value: float = 100):
        super().__init__(x, y, width, height, max_value)
        self.fill_color = (0, 100, 255)


class Text(UIElement):
    """Text display UI element."""

    def __init__(
        self,
        x: int,
        y: int,
        text: str = "",
        size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        font_path: Optional[str] = None,
    ):
        self.text = text
        self.size = size
        self.color = color
        self.font_path = font_path

        # Create font
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, size)
            except:
                self.font = pygame.font.Font(None, size)
        else:
            self.font = pygame.font.Font(None, size)

        # Calculate size based on text
        text_surface = self.font.render(text or " ", True, color)
        super().__init__(x, y, text_surface.get_width(), text_surface.get_height())

    def update(self, dt: float) -> None:
        """Update text."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw text."""
        if not self.visible or not self.text:
            return

        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.rect.topleft)

    def set_text(self, text: str) -> None:
        """Set text content."""
        self.text = text
        text_surface = self.font.render(text or " ", True, self.color)
        self.rect.width = text_surface.get_width()
        self.rect.height = text_surface.get_height()

    def set_color(self, color: Tuple[int, int, int]) -> None:
        """Change text color."""
        self.color = color

    def set_font_size(self, size: int) -> None:
        """Change font size."""
        self.size = size
        if self.font_path:
            try:
                self.font = pygame.font.Font(self.font_path, size)
            except:
                self.font = pygame.font.Font(None, size)
        else:
            self.font = pygame.font.Font(None, size)

        # Recalculate size
        text_surface = self.font.render(self.text or " ", True, self.color)
        self.rect.width = text_surface.get_width()
        self.rect.height = text_surface.get_height()

    def set_font(self, font_path: str) -> None:
        """Change font file."""
        self.font_path = font_path
        try:
            self.font = pygame.font.Font(font_path, self.size)
        except:
            self.font = pygame.font.Font(None, self.size)

        # Recalculate size
        text_surface = self.font.render(self.text or " ", True, self.color)
        self.rect.width = text_surface.get_width()
        self.rect.height = text_surface.get_height()


class Panel(UIElement):
    """Simple panel/container UI element."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Optional[Tuple[int, int, int]] = None,
    ):
        super().__init__(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_width = 2 if border_color else 0

    def update(self, dt: float) -> None:
        """Update panel."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Draw panel."""
        if not self.visible:
            return

        pygame.draw.rect(screen, self.color, self.rect)

        if self.border_color:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)

    def set_colors(
        self,
        color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
    ) -> None:
        """Change panel colors."""
        if color is not None:
            self.color = color
        if border_color is not None:
            self.border_color = border_color
            self.border_width = 2 if border_color else 0
