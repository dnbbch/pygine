"""
Главный игровой класс, управляющий игровым циклом и окном.
"""

import pygame
import sys
from typing import Tuple, Optional, Callable, List
from .utils import update_input_state


class Game:
    """
    Главный игровой класс, который управляет окном, игровым циклом
    и базовой функциональностью.

    Класс предоставляет простой интерфейс для создания игр с автоматическим
    управлением игровым циклом, обработкой событий и контролем частоты кадров.

    Аргументы:
        width: Ширина окна в пикселях
        height: Высота окна в пикселях
        title: Заголовок окна
        fps: Целевая частота кадров
        background_color: Цвет фона в формате (R, G, B)
        *,
        create_display: bool = True,

    Пример:
        >>> game = Game(800, 600, "Моя Игра")
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
        # Инициализируем pygame
        if not pygame.get_init():
            pygame.init()

        # Свойства окна
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

        # Параметры игрового цикла
        self.clock = pygame.time.Clock()
        self.running = False
        self.paused = False

        # Отслеживание дельта-времени
        self.dt = 0.0
        self.last_time = 0.0

        # Колбэки событий
        self.update_callback: Optional[Callable] = None
        self.draw_callback: Optional[Callable] = None
        self.event_callbacks: List[Callable] = []

        # Группа спрайтов для автоматического управления
        self.all_sprites = pygame.sprite.Group()

        # Отладочная информация
        self.show_fps = False
        self.font = None

    def run(
        self,
        update_func: Optional[Callable] = None,
        draw_func: Optional[Callable] = None,
    ) -> None:
        """
        Запустить основной игровой цикл.

        Аргументы:
            update_func: Функция, вызываемая каждый кадр для логики игры
            draw_func: Функция, вызываемая каждый кадр для отрисовки

        Пример:
            >>> def update():
            ...     # Логика игры
            ...     pass
            ...
            >>> def draw():
            ...     # Отрисовка
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
        """Реализация основного игрового цикла."""
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
        """Обработка событий pygame."""
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
        """Обновить игровую логику."""
        # Update all sprites in the group
        self.all_sprites.update(self.dt)

        # Call custom update function
        if self.update_callback:
            self.update_callback()

    def _draw(self) -> None:
        """Отрисовать всё на экран."""
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
        """Отрисовать счётчик FPS."""
        if not self.font:
            self.font = pygame.font.Font(None, 36)

        fps_text = f"FPS: {int(self.clock.get_fps())}"
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        self.screen.blit(fps_surface, (10, 10))

    def add_sprite(self, sprite: pygame.sprite.Sprite) -> None:
        """
        Добавить спрайт в систему автоматического обновления и отрисовки.

        Аргументы:
            sprite: Спрайт, который нужно добавить
        """
        self.all_sprites.add(sprite)

    def remove_sprite(self, sprite: pygame.sprite.Sprite) -> None:
        """
        Удалить спрайт из системы автоматического управления.

        Аргументы:
            sprite: Спрайт, который нужно удалить
        """
        self.all_sprites.remove(sprite)

    def add_event_callback(self, callback: Callable) -> None:
        """
        Добавить пользовательский обработчик событий.

        Аргументы:
            callback: Функция, принимающая объект события pygame
        """
        self.event_callbacks.append(callback)

    def set_background_color(self, color: Tuple[int, int, int]) -> None:
        """
        Установить цвет фона.

        Аргументы:
            color: RGB-кортеж цвета (0–255)
        """
        self.background_color = color

    def set_title(self, title: str) -> None:
        """
        Изменить заголовок окна.

        Аргументы:
            title: Новый заголовок окна
        """
        self.title = title
        pygame.display.set_caption(title)

    def set_fps(self, fps: int) -> None:
        """
        Задать целевую частоту кадров.

        Аргументы:
            fps: Кадров в секунду
        """
        self.fps = max(1, fps)

    def toggle_fps_display(self) -> None:
        """Переключить отображение счётчика FPS."""
        self.show_fps = not self.show_fps

    def toggle_pause(self) -> None:
        """Переключить состояние паузы игры."""
        self.paused = not self.paused

    def pause(self) -> None:
        """Поставить игру на паузу."""
        self.paused = True

    def resume(self) -> None:
        """Возобновить игру."""
        self.paused = False

    def quit(self) -> None:
        """
        Завершить игру и очистить ресурсы.
        """
        self.running = False
        pygame.quit()
        sys.exit()

    def get_screen_rect(self) -> pygame.Rect:
        """
        Получить прямоугольник экрана для проверки границ.

        Возвращает:
            Объект Rect, представляющий границы экрана
        """
        return pygame.Rect(0, 0, self.width, self.height)

    def get_center(self) -> Tuple[int, int]:
        """
        Получить центр экрана.

        Возвращает:
            Координаты центра (x, y)
        """
        return (self.width // 2, self.height // 2)

    def is_point_on_screen(self, x: int, y: int) -> bool:
        """
        Проверить, находится ли точка внутри границ экрана.

        Аргументы:
            x: Координата X
            y: Координата Y

        Возвращает:
            True — если точка на экране
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def screenshot(self, filename: str = "screenshot.png") -> None:
        """
        Сохранить скриншот текущего экрана.

        Аргументы:
            filename: Путь к файлу скриншота
        """
        pygame.image.save(self.screen, filename)

    def get_delta_time(self) -> float:
        """
        Получить дельта-время (время с прошлого кадра) в секундах.

        Возвращает:
            Дельта-время в секундах
        """
        return self.dt

    def get_fps(self) -> float:
        """
        Получить текущую частоту кадров.

        Возвращает:
            Текущее значение FPS
        """
        return self.clock.get_fps()

    def debug_info(self) -> dict:
        """
        Получить отладочную информацию о состоянии игры.

        Возвращает:
            Словарь с отладочной информацией
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
