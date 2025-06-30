"""
Utility functions for simplified game development
"""

import pygame
import time
from typing import Tuple, Set, Any


# Global state for input tracking
_pressed_keys: Set[int] = set()
_just_pressed_keys: Set[int] = set()
_just_released_keys: Set[int] = set()
_mouse_pressed: Tuple[bool, bool, bool] = (False, False, False)
_mouse_just_pressed: Tuple[bool, bool, bool] = (False, False, False)
_mouse_just_released: Tuple[bool, bool, bool] = (False, False, False)
_mouse_pos: Tuple[int, int] = (0, 0)


def update_input_state() -> None:
    """
    Update input state tracking. Should be called once per frame.
    This function is automatically called by the Game class.
    """
    global _pressed_keys, _just_pressed_keys, _just_released_keys
    global _mouse_pressed, _mouse_just_pressed, _mouse_just_released, _mouse_pos

    # Clear just-pressed states from previous frame
    _just_pressed_keys.clear()
    _just_released_keys.clear()
    _mouse_just_pressed = (False, False, False)
    _mouse_just_released = (False, False, False)

    # Get current states
    current_keys = set()
    keys = pygame.key.get_pressed()

    # Check specific keys we care about
    key_codes_to_check = [
        pygame.K_LEFT,
        pygame.K_RIGHT,
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_SPACE,
        pygame.K_RETURN,
        pygame.K_ESCAPE,
        pygame.K_LSHIFT,
        pygame.K_LCTRL,
        pygame.K_LALT,
        pygame.K_F1,
        pygame.K_F2,
        pygame.K_F3,
        pygame.K_F4,
        pygame.K_F5,
        pygame.K_F6,
        pygame.K_F7,
        pygame.K_F8,
        pygame.K_F9,
        pygame.K_F10,
        pygame.K_F11,
        pygame.K_F12,
        pygame.K_TAB,
        pygame.K_BACKSPACE,
    ]

    # Add letter keys (a-z)
    for i in range(ord("a"), ord("z") + 1):
        key_codes_to_check.append(getattr(pygame, f"K_{chr(i)}"))

    # Add number keys (0-9)
    for i in range(10):
        key_codes_to_check.append(getattr(pygame, f"K_{i}"))

    # Check if each key is pressed
    for key_code in key_codes_to_check:
        if keys[key_code]:
            current_keys.add(key_code)

    # Determine just pressed and just released keys
    _just_pressed_keys = current_keys - _pressed_keys
    _just_released_keys = _pressed_keys - current_keys
    _pressed_keys = current_keys

    # Update mouse state
    current_mouse = pygame.mouse.get_pressed()
    _mouse_just_pressed = tuple(
        current_mouse[i] and not _mouse_pressed[i] for i in range(3)
    )
    _mouse_just_released = tuple(
        not current_mouse[i] and _mouse_pressed[i] for i in range(3)
    )
    _mouse_pressed = current_mouse
    _mouse_pos = pygame.mouse.get_pos()


def key_pressed(key_code: int) -> bool:
    """
    Check if a key is currently being held down.

    Args:
        key_code: Pygame key code (e.g., pygame.K_LEFT, pygame.K_SPACE, pygame.K_a)

    Returns:
        True if key is currently pressed

    Example:
        >>> if key_pressed(pygame.K_LEFT):
        ...     player.move_left()
        >>> if key_pressed(pygame.K_SPACE):
        ...     player.jump()
    """
    return key_code in _pressed_keys


def key_just_pressed(key_code: int) -> bool:
    """
    Check if a key was just pressed this frame.

    Args:
        key_code: Pygame key code (e.g., pygame.K_LEFT, pygame.K_SPACE, pygame.K_a)

    Returns:
        True if key was pressed this frame

    Example:
        >>> if key_just_pressed(pygame.K_SPACE):
        ...     player.jump()
    """
    return key_code in _just_pressed_keys


def key_just_released(key_code: int) -> bool:
    """
    Check if a key was just released this frame.

    Args:
        key_code: Pygame key code (e.g., pygame.K_LEFT, pygame.K_SPACE, pygame.K_a)

    Returns:
        True if key was released this frame

    Example:
        >>> if key_just_released(pygame.K_SPACE):
        ...     player.stop_jump()
    """
    return key_code in _just_released_keys


def get_mouse_pos() -> Tuple[int, int]:
    """
    Get current mouse position.

    Returns:
        Tuple of (x, y) mouse coordinates
    """
    return _mouse_pos


def get_mouse_pressed() -> Tuple[bool, bool, bool]:
    """
    Get current mouse button states.

    Returns:
        Tuple of (left, middle, right) button states
    """
    return _mouse_pressed


def mouse_just_pressed(button: int = 0) -> bool:
    """
    Check if mouse button was just pressed this frame.

    Args:
        button: Mouse button (0=left, 1=middle, 2=right)

    Returns:
        True if button was pressed this frame
    """
    return _mouse_just_pressed[button] if 0 <= button < 3 else False


def mouse_just_released(button: int = 0) -> bool:
    """
    Check if mouse button was just released this frame.

    Args:
        button: Mouse button (0=left, 1=middle, 2=right)

    Returns:
        True if button was released this frame
    """
    return _mouse_just_released[button] if 0 <= button < 3 else False


def wait(seconds: float) -> None:
    """
    Wait for a specified number of seconds.

    Args:
        seconds: Time to wait in seconds

    Example:
        >>> wait(2.5)  # Wait for 2.5 seconds
    """
    time.sleep(seconds)


def wait_for_key(key_code: int = None) -> int:
    """
    Wait until a key is pressed.

    Args:
        key_code: Specific pygame key code to wait for (optional)

    Returns:
        Pygame key code of the key that was pressed

    Example:
        >>> wait_for_key(pygame.K_SPACE)  # Wait for spacebar
        >>> pressed = wait_for_key()  # Wait for any key
    """
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if key_code is None or event.key == key_code:
                    return event.key

        time.sleep(0.01)  # Small delay to prevent busy waiting


def wait_for_click(button: int = 0) -> Tuple[int, int]:
    """
    Wait until mouse button is clicked.

    Args:
        button: Mouse button to wait for (0=left, 1=middle, 2=right)

    Returns:
        Position where mouse was clicked

    Example:
        >>> pos = wait_for_click()  # Wait for left click
        >>> pos = wait_for_click(2)  # Wait for right click
    """
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == button + 1:  # pygame uses 1-based indexing
                    return event.pos

        time.sleep(0.01)


def wait_for_animation(sprite: Any) -> None:
    """
    Wait until sprite's current animation finishes.

    Args:
        sprite: AnimatedSprite instance

    Example:
        >>> player.play_animation('attack', loop=False)
        >>> wait_for_animation(player)
    """
    from .sprite import AnimatedSprite

    if not isinstance(sprite, AnimatedSprite):
        return

    while not sprite.is_animation_finished():
        sprite.update()
        time.sleep(0.01)


def distance(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    """
    Calculate distance between two points.

    Args:
        pos1: First position (x, y)
        pos2: Second position (x, y)

    Returns:
        Distance between points
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return (dx**2 + dy**2) ** 0.5


def normalize_vector(vector: Tuple[float, float]) -> Tuple[float, float]:
    """
    Normalize a 2D vector to unit length.

    Args:
        vector: Vector to normalize (x, y)

    Returns:
        Normalized vector
    """
    x, y = vector
    length = (x**2 + y**2) ** 0.5

    if length == 0:
        return (0.0, 0.0)

    return (x / length, y / length)


def lerp(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between two values.

    Args:
        start: Start value
        end: End value
        t: Interpolation factor (0.0 to 1.0)

    Returns:
        Interpolated value
    """
    return start + (end - start) * max(0.0, min(1.0, t))


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp value between minimum and maximum.

    Args:
        value: Value to clamp
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        Clamped value
    """
    return max(min_val, min(max_val, value))
