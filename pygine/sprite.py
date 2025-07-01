"""
Основной функционал спрайтов с поддержкой анимации
"""

import pygame
import math
from typing import List, Dict, Tuple, Optional, Union
from pathlib import Path
from .animation import Animation, AnimationManager


class AnimatedSprite(pygame.sprite.Sprite):
    """
    Расширенный спрайт pygame с встроенной поддержкой анимации,
    трансформаций и удобных утилит.

    Класс наследует `pygame.sprite.Sprite`, предоставляя простое управление
    анимациями, работу со спрайтшитом, трансформации и распространённые
    функции игрового объекта.

    Аргументы:
        image_path: Путь к изображению спрайтшита
        frame_size: Размер кадра (width, height) в пикселях
        position: Начальная позиция (x, y). По умолчанию (0, 0)

    Пример:
        >>> player = AnimatedSprite("player.png", (32, 32), (100, 100))
        >>> player.add_animation("walk", [0, 1, 2, 3], fps=10)
        >>> player.play_animation("walk")
    """

    def __init__(
        self,
        image_path: Union[str, Path],
        frame_size: Tuple[int, int],
        position: Tuple[int, int] = (0, 0),
    ):
        super().__init__()

        # Основные свойства
        self.original_image = pygame.image.load(str(image_path)).convert_alpha()
        self.frame_size = frame_size
        self._position = list(position)

        # Вычисляем размеры спрайтшита
        self.sheet_width = self.original_image.get_width()
        self.sheet_height = self.original_image.get_height()
        self.frames_per_row = self.sheet_width // frame_size[0]
        self.frames_per_col = self.sheet_height // frame_size[1]
        self.total_frames = self.frames_per_row * self.frames_per_col

        # Извлекаем все кадры из спрайтшита
        self.frames = self._extract_frames()

        # Система анимации
        self.animation_manager = AnimationManager()
        self.current_frame = 0

        # Свойства трансформации
        self.rotation = 0.0
        self.scale = 1.0
        self.flip_x = False
        self.flip_y = False
        self._mirrored = False

        # Физические свойства
        self.velocity = [0.0, 0.0]
        self.acceleration = [0.0, 0.0]

        # Инициализируем свойства pygame спрайта
        self.image = self.frames[0] if self.frames else pygame.Surface(frame_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        # Свойства коллизий
        self.collision_rect = self.rect.copy()
        self.collision_offset = (0, 0)

        # Пользовательские свойства хитбокса
        self.custom_hitbox_size = None  # (width, height) or None for default
        self.hitbox_shape = "rect"  # "rect" or "circle"
        self.hitbox_radius = None  # для круглых хитбоксов

    def _extract_frames(self) -> List[pygame.Surface]:
        """Извлечь все отдельные кадры из спрайтшита."""
        frames = []
        frame_width, frame_height = self.frame_size

        for row in range(self.frames_per_col):
            for col in range(self.frames_per_row):
                x = col * frame_width
                y = row * frame_height

                frame = pygame.Surface(self.frame_size, pygame.SRCALPHA)
                frame.blit(
                    self.original_image,
                    (0, 0),
                    pygame.Rect(x, y, frame_width, frame_height),
                )
                frames.append(frame)

        return frames

    def add_animation(
        self, name: str, frames: List[int], fps: float = 10, loop: bool = True
    ) -> None:
        """
        Добавить новую анимацию этому спрайту.

        Аргументы:
            name: Уникальное имя анимации
            frames: Список индексов кадров из спрайтшита
            fps: Скорость анимации (кадров в секунду)
            loop: Зацикливать ли анимацию

        Пример:
            >>> sprite.add_animation("walk", [0, 1, 2, 3], fps=8)
            >>> sprite.add_animation("jump", [4, 5, 6], fps=12, loop=False)
        """
        # Проверяем индексы кадров
        valid_frames = [f for f in frames if 0 <= f < len(self.frames)]
        if len(valid_frames) != len(frames):
            invalid = [f for f in frames if f not in valid_frames]
            print(
                f"Warning: Invalid frame indices {invalid} for sprite with {len(self.frames)} frames"
            )

        animation = Animation(name, valid_frames, fps, loop)
        self.animation_manager.add_animation(animation)

    def play_animation(
        self, name: str, restart: bool = False, mirror: Optional[bool] = None
    ) -> bool:
        """
        Запустить указанную анимацию.

        Аргументы:
            name: Имя анимации
            restart: Перезапустить, если анимация уже играет
            mirror: Переопределить состояние зеркалирования для этой анимации

        Возвращает:
            True — если анимация успешно запущена, False — если не найдена
        """
        if mirror is not None:
            self._mirrored = mirror

        return self.animation_manager.play_animation(name, restart)

    def stop_animation(self) -> None:
        """Остановить текущую анимацию."""
        self.animation_manager.stop()

    def pause_animation(self) -> None:
        """Приостановить текущую анимацию."""
        self.animation_manager.pause()

    def resume_animation(self) -> None:
        """Возобновить приостановленную анимацию."""
        self.animation_manager.resume()

    def is_animation_finished(self) -> bool:
        """Проверить, завершилась ли текущая анимация (для незцикленных анимаций)."""
        return self.animation_manager.is_finished()

    def get_current_animation(self) -> Optional[str]:
        """Получить имя текущей воспроизводимой анимации."""
        return self.animation_manager.current_animation_name

    def get_animation_frame(self) -> int:
        """Получить индекс текущего кадра в анимации."""
        return self.animation_manager.get_current_frame_index()

    def update(self, dt: float = 1 / 60) -> None:
        """
        Обновить анимацию и физику спрайта.

        Аргументы:
            dt: Дельта-время в секундах
        """
        # Обновляем анимацию
        self.animation_manager.update(dt)
        current_animation = self.animation_manager.get_current_animation()

        if current_animation:
            frame_index = self.animation_manager.get_current_frame_index()
            if 0 <= frame_index < len(current_animation.frames):
                sprite_frame_index = current_animation.frames[frame_index]
                if 0 <= sprite_frame_index < len(self.frames):
                    self.current_frame = sprite_frame_index

        # Обновляем физику
        self.velocity[0] += self.acceleration[0] * dt
        self.velocity[1] += self.acceleration[1] * dt

        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt

        # Обновляем изображение с текущими трансформациями
        self._update_image()

        # Обновляем позицию rect
        self.rect.center = (int(self._position[0]), int(self._position[1]))

        # Обновляем rect коллизии
        self.collision_rect.center = (
            self.rect.centerx + self.collision_offset[0],
            self.rect.centery + self.collision_offset[1],
        )

    def _update_image(self) -> None:
        """Обновить изображение с учётом текущих трансформаций."""
        if not self.frames:
            return

        # Начинаем с текущего кадра
        image = self.frames[self.current_frame].copy()

        # Применяем масштабирование
        if self.scale != 1.0:
            new_size = (
                int(image.get_width() * self.scale),
                int(image.get_height() * self.scale),
            )
            image = pygame.transform.scale(image, new_size)

        # Применяем отражение/зеркалирование
        flip_x = self.flip_x or self._mirrored
        if flip_x or self.flip_y:
            image = pygame.transform.flip(image, flip_x, self.flip_y)

        # Применяем поворот
        if self.rotation != 0:
            image = pygame.transform.rotate(image, self.rotation)

        # Обновляем изображение и создаём новый rect.
        # Координаты центра установит вызывающий метод update(),
        # чтобы избежать двойного пересчёта за один кадр.
        self.image = image
        self.rect = self.image.get_rect()

    # Методы позиционирования и движения
    def set_position(self, x: float, y: float) -> None:
        """Установить позицию спрайта."""
        self._position = [float(x), float(y)]

    def get_position(self) -> Tuple[float, float]:
        """Получить текущую позицию спрайта."""
        return tuple(self._position)

    @property
    def x(self) -> float:
        """Координата X центра спрайта (чтение/запись)."""
        return self._position[0]

    @x.setter
    def x(self, value: float) -> None:
        self._position[0] = float(value)
        # Синхронизируем rect и collision rect немедленно
        self.rect.centerx = int(value)
        self.collision_rect.centerx = int(value) + self.collision_offset[0]

    @property
    def y(self) -> float:
        """Координата Y центра спрайта (чтение/запись)."""
        return self._position[1]

    @y.setter
    def y(self, value: float) -> None:
        self._position[1] = float(value)
        # Синхронизируем rect и collision rect немедленно
        self.rect.centery = int(value)
        self.collision_rect.centery = int(value) + self.collision_offset[1]

    # -------------------------------------------------------------------------------

    def move(self, dx: float, dy: float) -> None:
        """Переместить спрайт на смещение."""
        self._position[0] += dx
        self._position[1] += dy

    def move_to(self, x: float, y: float, speed: float = None) -> None:
        """Переместить спрайт к заданной позиции."""
        if speed is None:
            self.set_position(x, y)
        else:
            dx = x - self._position[0]
            dy = y - self._position[1]
            distance = math.sqrt(dx**2 + dy**2)

            if distance > 0:
                dx_norm = dx / distance
                dy_norm = dy / distance
                self.velocity[0] = dx_norm * speed
                self.velocity[1] = dy_norm * speed

    # Методы трансформации
    def set_rotation(self, angle: float) -> None:
        """Задать угол поворота в градусах."""
        self.rotation = angle % 360

    def rotate(self, angle: float) -> None:
        """Повернуть на угол в градусах."""
        self.rotation = (self.rotation + angle) % 360

    def rotate_towards(self, x: float, y: float) -> None:
        """Повернуть спрайт в сторону точки."""
        dx = x - self._position[0]
        dy = y - self._position[1]
        angle = math.degrees(math.atan2(-dy, dx))
        self.set_rotation(angle)

    def rotate_towards_mouse(self) -> None:
        """Повернуть спрайт к курсору мыши."""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rotate_towards(mouse_x, mouse_y)

    def set_scale(self, scale: float) -> None:
        """Установить масштаб спрайта (1.0 = оригинальный размер)."""
        self.scale = max(0.1, scale)  # Предотвращаем отрицательный или нулевой масштаб

    def set_flip(self, flip_x: bool = False, flip_y: bool = False) -> None:
        """Установить отражение спрайта."""
        self.flip_x = flip_x
        self.flip_y = flip_y

    def mirror(self, mirrored: bool = True) -> None:
        """Отразить спрайт по горизонтали (полезно для движения влево/вправо)."""
        self._mirrored = mirrored

    # Методы коллизий
    def set_collision_rect(
        self, width: int, height: int, offset_x: int = 0, offset_y: int = 0
    ) -> None:
        """Задать пользовательский прямоугольник коллизии, корректный с учётом поворота."""
        self.collision_rect = pygame.Rect(0, 0, width, height)
        self.collision_offset = (offset_x, offset_y)
        self.custom_hitbox_size = (width, height)
        self.hitbox_shape = "rect"

    def set_collision_circle(
        self, radius: float, offset_x: int = 0, offset_y: int = 0
    ) -> None:
        """Задать круговую область коллизии."""
        self.hitbox_shape = "circle"
        self.hitbox_radius = radius
        self.collision_offset = (offset_x, offset_y)
        # Still set rect for compatibility
        size = int(radius * 2)
        self.collision_rect = pygame.Rect(0, 0, size, size)
        # Всё равно устанавливаем rect для совместимости

    def reset_collision_to_default(self) -> None:
        """Сбросить область коллизии к размеру спрайта."""
        self.custom_hitbox_size = None
        self.hitbox_shape = "rect"
        self.hitbox_radius = None
        self.collision_offset = (0, 0)

    def collides_with(self, other: "AnimatedSprite") -> bool:
        """Проверить столкновение с другим спрайтом (поддерживает поворот и разные формы)."""
        # Столкновение окружности с окружностью
        if self.hitbox_shape == "circle" and other.hitbox_shape == "circle":
            return self._check_circle_collision(other)

        # Столкновение окружности с прямоугольником
        if self.hitbox_shape == "circle" or other.hitbox_shape == "circle":
            return self._check_circle_rect_collision(other)

        # ВСЕГДА используем ту же коллизию по углам, что показывает debug_draw
        return self._check_precise_rect_collision(other)

    def _check_precise_rect_collision(self, other: "AnimatedSprite") -> bool:
        """Точное столкновение прямоугольников, использующее те же координаты, что и debug_draw."""
        corners_a = self._get_corners()
        corners_b = other._get_corners()

        # Используем SAT (теорема о разделяющих осях) для точной коллизии
        return self._separating_axis_test(corners_a, corners_b)

    def _separating_axis_test(self, corners_a, corners_b):
        """Проверка столкновения многоугольников методом теоремы о разделяющих осях."""
        # Получаем все рёбра обоих многоугольников
        all_corners = [corners_a, corners_b]

        for corners in all_corners:
            for i in range(len(corners)):
                # Получаем вектор ребра
                p1 = corners[i]
                p2 = corners[(i + 1) % len(corners)]
                edge = (p2[0] - p1[0], p2[1] - p1[1])

                # Получаем перпендикулярный (нормальный) вектор
                normal = (-edge[1], edge[0])

                # Нормализуем
                length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
                if length == 0:
                    continue
                normal = (normal[0] / length, normal[1] / length)

                # Проецируем оба многоугольника на эту ось
                proj_a = [
                    corner[0] * normal[0] + corner[1] * normal[1]
                    for corner in corners_a
                ]
                proj_b = [
                    corner[0] * normal[0] + corner[1] * normal[1]
                    for corner in corners_b
                ]

                min_a, max_a = min(proj_a), max(proj_a)
                min_b, max_b = min(proj_b), max(proj_b)

                # Проверяем разделение
                if max_a < min_b or max_b < min_a:
                    return False  # Найдено разделение — коллизии нет
        return True  # Разделение не найдено — коллизия обнаружена

    def _check_obb_collision(self, other: "AnimatedSprite") -> bool:
        """УСТАРЕЛО: Используйте _check_precise_rect_collision instead."""
        return self._check_precise_rect_collision(other)

    def _get_corners(self):
        """Получить четыре угла хитбокса спрайта — ТОЧНО как в debug_draw."""
        # Используем пользовательский размер, если задан, иначе размер кадра с масштабом
        if self.custom_hitbox_size:
            width, height = self.custom_hitbox_size
            # Пользовательские размеры не масштабируются автоматически
        else:
            width = self.frame_size[0] * self.scale
            height = self.frame_size[1] * self.scale

        # ВАЖНО: Используем то же округление, что и в методе update() для согласованности
        center_x = int(self._position[0]) + self.collision_offset[0]
        center_y = int(self._position[1]) + self.collision_offset[1]

        # Вычисляем углы относительно центра
        half_w = width / 2
        half_h = height / 2

        corners = [
            (-half_w, -half_h),  # Верхний левый
            (half_w, -half_h),  # Верхний правый
            (half_w, half_h),  # Нижний правый
            (-half_w, half_h),  # Нижний левый
        ]

        # Применяем поворот при необходимости
        if self.rotation != 0:
            # Инвертируем угол для соответствия направлению pygame.transform.rotate
            # pygame поворачивает против часовой стрелки с положительными углами, но ось Y направлена вниз
            angle_rad = math.radians(-self.rotation)
            cos_a = math.cos(angle_rad)
            sin_a = math.sin(angle_rad)

            rotated_corners = []
            for x, y in corners:
                new_x = x * cos_a - y * sin_a
                new_y = x * sin_a + y * cos_a
                rotated_corners.append((new_x, new_y))
            corners = rotated_corners

        # Переводим в мировые координаты
        world_corners = [(center_x + x, center_y + y) for x, y in corners]
        return world_corners

    def _check_circle_collision(self, other: "AnimatedSprite") -> bool:
        """Проверить столкновение двух окружностей."""
        # Используем то же округление, что и везде
        center1 = (
            int(self._position[0]) + self.collision_offset[0],
            int(self._position[1]) + self.collision_offset[1],
        )
        center2 = (
            int(other._position[0]) + other.collision_offset[0],
            int(other._position[1]) + other.collision_offset[1],
        )

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]
        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= (self.hitbox_radius + other.hitbox_radius)
        # Используем согласованное позиционирование как в коллизиях

    def _check_circle_rect_collision(self, other: "AnimatedSprite") -> bool:
        """Точное столкновение между окружностью и прямоугольником с использованием корректного алгоритма."""
        if self.hitbox_shape == "circle":
            circle_sprite = self
            rect_sprite = other
        else:
            circle_sprite = other
            rect_sprite = self

        # Получаем центр окружности с согласованным округлением
        circle_center = (
            int(circle_sprite._position[0]) + circle_sprite.collision_offset[0],
            int(circle_sprite._position[1]) + circle_sprite.collision_offset[1],
        )

        # Для повернутых прямоугольников используем коллизию многоугольника с окружностью
        if rect_sprite.rotation != 0 or rect_sprite.custom_hitbox_size:
            return self._check_polygon_circle_collision(circle_sprite, rect_sprite)

        # Простой случай: прямоугольник, выровненный по осям
        # Получаем границы прямоугольника
        rect_width = rect_sprite.frame_size[0] * rect_sprite.scale
        rect_height = rect_sprite.frame_size[1] * rect_sprite.scale

        rect_center_x = int(rect_sprite._position[0]) + rect_sprite.collision_offset[0]
        rect_center_y = int(rect_sprite._position[1]) + rect_sprite.collision_offset[1]

        rect_left = rect_center_x - rect_width / 2
        rect_right = rect_center_x + rect_width / 2
        rect_top = rect_center_y - rect_height / 2
        rect_bottom = rect_center_y + rect_height / 2

        # Находим ближайшую точку на прямоугольнике к центру окружности
        closest_x = max(rect_left, min(circle_center[0], rect_right))
        closest_y = max(rect_top, min(circle_center[1], rect_bottom))

        # Вычисляем расстояние от центра окружности до ближайшей точки
        dx = circle_center[0] - closest_x
        dy = circle_center[1] - closest_y
        distance = math.sqrt(dx * dx + dy * dy)

        return distance <= circle_sprite.hitbox_radius
        # Используем согласованное позиционирование как в коллизиях

    def _check_polygon_circle_collision(
        self, circle_sprite: "AnimatedSprite", rect_sprite: "AnimatedSprite"
    ) -> bool:
        """Точное столкновение между окружностью и повернутым многоугольником с использованием корректного алгоритма."""
        circle_center = (
            int(circle_sprite._position[0]) + circle_sprite.collision_offset[0],
            int(circle_sprite._position[1]) + circle_sprite.collision_offset[1],
        )

        # Получаем углы многоугольника
        polygon_corners = rect_sprite._get_corners()

        # Проверяем, находится ли центр окружности внутри многоугольника
        inside = self._point_in_polygon(circle_center, polygon_corners)
        if inside:
            return True

        # Проверяем расстояние от центра окружности до каждого ребра многоугольника
        for i in range(len(polygon_corners)):
            p1 = polygon_corners[i]
            p2 = polygon_corners[(i + 1) % len(polygon_corners)]

            # Расстояние от центра окружности до отрезка
            distance = self._point_to_line_distance(circle_center, p1, p2)
            if distance <= circle_sprite.hitbox_radius:
                return True

        return False

    def _point_in_polygon(self, point, polygon):
        """Проверить, находится ли точка внутри многоугольника (алгоритм лучевого броска)."""
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def _point_to_line_distance(self, point, line_p1, line_p2):
        """Вычислить минимальное расстояние от точки до отрезка."""
        px, py = point
        x1, y1 = line_p1
        x2, y2 = line_p2

        # Вектор от начала линии к концу
        line_vec = (x2 - x1, y2 - y1)
        # Вектор от начала линии к точке
        point_vec = (px - x1, py - y1)

        # Квадрат длины линии
        line_len_sq = line_vec[0] * line_vec[0] + line_vec[1] * line_vec[1]

        if line_len_sq == 0:
            # Линия на самом деле является точкой
            return math.sqrt((px - x1) * (px - x1) + (py - y1) * (py - y1))

        # Проецируем точку на линию
        dot_product = point_vec[0] * line_vec[0] + point_vec[1] * line_vec[1]
        t = max(0, min(1, dot_product / line_len_sq))

        # Находим ближайшую точку на отрезке
        closest_x = x1 + t * line_vec[0]
        closest_y = y1 + t * line_vec[1]

        # Расстояние от точки до ближайшей точки на линии
        dx = px - closest_x
        dy = py - closest_y
        return math.sqrt(dx * dx + dy * dy)

    def collides_with_group(self, group: pygame.sprite.Group) -> List["AnimatedSprite"]:
        """Проверить столкновение со всеми спрайтами в группе."""
        collisions = []
        for sprite in group:
            if isinstance(sprite, AnimatedSprite) and sprite != self:
                if self.collides_with(sprite):
                    collisions.append(sprite)
        return collisions

    # Утилитарные методы
    def distance_to(self, other: Union["AnimatedSprite", Tuple[float, float]]) -> float:
        """Вычислить расстояние до другого спрайта или точки с учётом согласованных координат."""
        if isinstance(other, AnimatedSprite):
            # Используем согласованное позиционирование как в коллизиях
            other_pos = (int(other._position[0]), int(other._position[1]))
        else:
            other_pos = other

        # Используем согласованное позиционирование
        self_pos = (int(self._position[0]), int(self._position[1]))

        dx = other_pos[0] - self_pos[0]
        dy = other_pos[1] - self_pos[1]
        return math.sqrt(dx**2 + dy**2)

    def angle_to(self, other: Union["AnimatedSprite", Tuple[float, float]]) -> float:
        """Вычислить угол до другого спрайта или точки с учётом согласованных координат."""
        if isinstance(other, AnimatedSprite):
            # Используем согласованное позиционирование как в коллизиях
            other_pos = (int(other._position[0]), int(other._position[1]))
        else:
            other_pos = other

        # Используем согласованное позиционирование
        self_pos = (int(self._position[0]), int(self._position[1]))

        dx = other_pos[0] - self_pos[0]
        dy = other_pos[1] - self_pos[1]
        return math.degrees(math.atan2(-dy, dx))

    def is_on_screen(self, screen_rect: pygame.Rect) -> bool:
        """Проверить, виден ли спрайт на экране."""
        return self.rect.colliderect(screen_rect)

    def wrap_screen(self, screen_rect: pygame.Rect) -> None:
        """Переместить спрайт на противоположный край экрана (обтекание)."""
        if self.rect.right < 0:
            self.rect.left = screen_rect.right
        elif self.rect.left > screen_rect.right:
            self.rect.right = 0

        if self.rect.bottom < 0:
            self.rect.top = screen_rect.bottom
        elif self.rect.top > screen_rect.bottom:
            self.rect.bottom = 0

        self._position[0] = self.rect.centerx
        self._position[1] = self.rect.centery

    def debug_draw(self, screen: pygame.Surface) -> None:
        """Нарисовать хитбокс (точно ту же область, что используется для проверки коллизий)."""
        if self.hitbox_shape == "circle":
            # Рисуем круглый хитбокс с тем же округлением
            center = (
                int(self._position[0]) + self.collision_offset[0],
                int(self._position[1]) + self.collision_offset[1],
            )
            radius = int(self.hitbox_radius)
            pygame.draw.circle(screen, (0, 255, 0), center, radius, 2)
        else:
            # Рисуем прямоугольный хитбокс — ТОЧНО те же углы, что используются в коллизии
            corners = self._get_corners()
            # Конвертируем в целые числа для отрисовки
            int_corners = [(int(x), int(y)) for x, y in corners]
            pygame.draw.polygon(screen, (0, 255, 0), int_corners, 2)

    def debug_info(self) -> Dict:
        """Получить отладочную информацию о спрайте."""
        return {
            "position": self.get_position(),
            "velocity": self.velocity.copy(),
            "rotation": self.rotation,
            "scale": self.scale,
            "current_frame": self.current_frame,
            "animation": self.get_current_animation(),
            "animation_frame": self.get_animation_frame(),
            "total_frames": len(self.frames),
            "rect": (self.rect.x, self.rect.y, self.rect.width, self.rect.height),
        }
