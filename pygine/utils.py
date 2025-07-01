"""
Утилитарные функции для упрощения разработки игр
"""

import pygame
import time
from typing import Tuple, Set, Any


# Глобальное состояние для отслеживания ввода
_pressed_keys: Set[int] = set()
_just_pressed_keys: Set[int] = set()
_just_released_keys: Set[int] = set()
_mouse_pressed: Tuple[bool, bool, bool] = (False, False, False)
_mouse_just_pressed: Tuple[bool, bool, bool] = (False, False, False)
_mouse_just_released: Tuple[bool, bool, bool] = (False, False, False)
_mouse_pos: Tuple[int, int] = (0, 0)


def update_input_state() -> None:
    """
    Обновить отслеживание состояния ввода. Должна вызываться один раз за кадр.
    Эта функция автоматически вызывается классом Game.
    """
    global _pressed_keys, _just_pressed_keys, _just_released_keys
    global _mouse_pressed, _mouse_just_pressed, _mouse_just_released, _mouse_pos

    # Очищаем состояния "только что нажато" с предыдущего кадра
    _just_pressed_keys.clear()
    _just_released_keys.clear()
    _mouse_just_pressed = (False, False, False)
    _mouse_just_released = (False, False, False)

    # Получаем текущие состояния
    current_keys = set()
    keys = pygame.key.get_pressed()

    # Проверяем конкретные клавиши, которые нас интересуют
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

    # Добавляем буквенные клавиши (a-z)
    for i in range(ord("a"), ord("z") + 1):
        key_codes_to_check.append(getattr(pygame, f"K_{chr(i)}"))

    # Добавляем цифровые клавиши (0-9)
    for i in range(10):
        key_codes_to_check.append(getattr(pygame, f"K_{i}"))

    # Проверяем, нажата ли каждая клавиша
    for key_code in key_codes_to_check:
        if keys[key_code]:
            current_keys.add(key_code)

    # Определяем только что нажатые и только что отпущенные клавиши
    _just_pressed_keys = current_keys - _pressed_keys
    _just_released_keys = _pressed_keys - current_keys
    _pressed_keys = current_keys

    # Обновляем состояние мыши
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
    Проверить, удерживается ли клавиша в данный момент.

    Args:
        key_code: Код клавиши pygame (например, pygame.K_LEFT, pygame.K_SPACE, pygame.K_a)

    Returns:
        True, если клавиша сейчас нажата

    Example:
        >>> if key_pressed(pygame.K_LEFT):
        ...     player.move_left()
        >>> if key_pressed(pygame.K_SPACE):
        ...     player.jump()
    """
    return key_code in _pressed_keys


def key_just_pressed(key_code: int) -> bool:
    """
    Проверить, была ли клавиша только что нажата в этом кадре.

    Args:
        key_code: Код клавиши pygame (например, pygame.K_LEFT, pygame.K_SPACE, pygame.K_a)

    Returns:
        True, если клавиша была нажата в этом кадре

    Example:
        >>> if key_just_pressed(pygame.K_SPACE):
        ...     player.jump()
    """
    return key_code in _just_pressed_keys


def key_just_released(key_code: int) -> bool:
    """
    Проверить, была ли клавиша только что отпущена в этом кадре.

    Args:
        key_code: Код клавиши pygame (например, pygame.K_LEFT, pygame.K_SPACE, pygame.K_a)

    Returns:
        True, если клавиша была отпущена в этом кадре

    Example:
        >>> if key_just_released(pygame.K_SPACE):
        ...     player.stop_jump()
    """
    return key_code in _just_released_keys


def get_mouse_pos() -> Tuple[int, int]:
    """
    Получить текущую позицию мыши.

    Returns:
        Кортеж координат мыши (x, y)
    """
    return _mouse_pos


def get_mouse_pressed() -> Tuple[bool, bool, bool]:
    """
    Получить текущие состояния кнопок мыши.

    Returns:
        Кортеж состояний кнопок (левая, средняя, правая)
    """
    return _mouse_pressed


def mouse_just_pressed(button: int = 0) -> bool:
    """
    Проверить, была ли кнопка мыши только что нажата в этом кадре.

    Args:
        button: Кнопка мыши (0=левая, 1=средняя, 2=правая)

    Returns:
        True, если кнопка была нажата в этом кадре
    """
    return _mouse_just_pressed[button] if 0 <= button < 3 else False


def mouse_just_released(button: int = 0) -> bool:
    """
    Проверить, была ли кнопка мыши только что отпущена в этом кадре.

    Args:
        button: Кнопка мыши (0=левая, 1=средняя, 2=правая)

    Returns:
        True, если кнопка была отпущена в этом кадре
    """
    return _mouse_just_released[button] if 0 <= button < 3 else False


def wait(seconds: float) -> None:
    """
    Ожидать указанное количество секунд.

    Args:
        seconds: Время ожидания в секундах

    Example:
        >>> wait(2.5)  # Ждать 2.5 секунды
    """
    time.sleep(seconds)


def wait_for_key(key_code: int = None) -> int:
    """
    Ожидать, пока не будет нажата клавиша.

    Args:
        key_code: Конкретный код клавиши pygame для ожидания (опционально)

    Returns:
        Код клавиши pygame, которая была нажата

    Example:
        >>> wait_for_key(pygame.K_SPACE)  # Ждать пробел
        >>> pressed = wait_for_key()  # Ждать любую клавишу
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

        time.sleep(0.01)  # Небольшая задержка для предотвращения активного ожидания


def wait_for_click(button: int = 0) -> Tuple[int, int]:
    """
    Ожидать, пока не будет нажата кнопка мыши.

    Args:
        button: Кнопка мыши для ожидания (0=левая, 1=средняя, 2=правая)

    Returns:
        Позиция, где была нажата мышь

    Example:
        >>> pos = wait_for_click()  # Ждать левый клик
        >>> pos = wait_for_click(2)  # Ждать правый клик
    """
    pygame.event.clear()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == button + 1:  # pygame использует индексацию с 1
                    return event.pos

        time.sleep(0.01)


def wait_for_animation(sprite: Any) -> None:
    """
    Ожидать, пока не завершится текущая анимация спрайта.

    Args:
        sprite: Экземпляр AnimatedSprite

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
    Вычислить расстояние между двумя точками.

    Args:
        pos1: Первая позиция (x, y)
        pos2: Вторая позиция (x, y)

    Returns:
        Расстояние между точками
    """
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return (dx**2 + dy**2) ** 0.5


def normalize_vector(vector: Tuple[float, float]) -> Tuple[float, float]:
    """
    Нормализовать 2D вектор до единичной длины.

    Args:
        vector: Вектор для нормализации (x, y)

    Returns:
        Нормализованный вектор
    """
    x, y = vector
    length = (x**2 + y**2) ** 0.5

    if length == 0:
        return (0.0, 0.0)

    return (x / length, y / length)


def lerp(start: float, end: float, t: float) -> float:
    """
    Линейная интерполяция между двумя значениями.

    Args:
        start: Начальное значение
        end: Конечное значение
        t: Фактор интерполяции (0.0 до 1.0)

    Returns:
        Интерполированное значение
    """
    return start + (end - start) * max(0.0, min(1.0, t))


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Ограничить значение между минимумом и максимумом.

    Args:
        value: Значение для ограничения
        min_val: Минимально допустимое значение
        max_val: Максимально допустимое значение

    Returns:
        Ограниченное значение
    """
    return max(min_val, min(max_val, value))
