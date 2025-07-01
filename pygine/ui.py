"""
Компоненты пользовательского интерфейса
"""

import pygame
from typing import Tuple, Optional, Callable
from abc import ABC, abstractmethod


def draw_rounded_rect(surface: pygame.Surface, color: Tuple[int, int, int], rect: pygame.Rect, border_radius: int) -> None:
    """
    Нарисовать прямоугольник со скругленными углами.
    
    Args:
        surface: Поверхность для рисования
        color: Цвет заливки
        rect: Прямоугольник для рисования
        border_radius: Радиус скругления углов
    """
    if border_radius <= 0:
        pygame.draw.rect(surface, color, rect)
        return
    
    # Ограничиваем радиус
    max_radius = min(rect.width, rect.height) // 2
    radius = min(border_radius, max_radius)
    
    if radius <= 0:
        pygame.draw.rect(surface, color, rect)
        return
    
    # Используем встроенную функцию pygame для скругленных прямоугольников
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def draw_rounded_rect_border(surface: pygame.Surface, color: Tuple[int, int, int], rect: pygame.Rect, border_radius: int, border_width: int = 1) -> None:
    """
    Нарисовать границу прямоугольника со скругленными углами.
    
    Args:
        surface: Поверхность для рисования
        color: Цвет границы
        rect: Прямоугольник для рисования
        border_radius: Радиус скругления углов
        border_width: Толщина границы
    """
    if border_radius <= 0 or border_width <= 0:
        if border_width > 0:
            pygame.draw.rect(surface, color, rect, border_width)
        return
    
    # Ограничиваем радиус
    max_radius = min(rect.width, rect.height) // 2
    radius = min(border_radius, max_radius)
    
    if radius <= 0:
        pygame.draw.rect(surface, color, rect, border_width)
        return
    
    # Используем встроенную функцию pygame для скругленных границ
    pygame.draw.rect(surface, color, rect, border_width, border_radius=radius)


class UIElement(ABC):
    """Базовый класс для всех элементов интерфейса."""

    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True

    @abstractmethod
    def update(self, dt: float) -> None:
        """Обновить элемент интерфейса."""
        pass

    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать элемент интерфейса."""
        pass

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обработать событие ввода. Возвращает True, если событие было обработано."""
        return False


class Button(UIElement):
    """Простой элемент кнопки интерфейса."""

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
        border_radius: int = 0,
    ):
        """
        Создать кнопку.
        
        Args:
            x, y: Позиция кнопки
            width, height: Размеры кнопки
            text: Текст на кнопке
            callback: Функция, вызываемая при нажатии
            font_size: Размер шрифта
            font_path: Путь к файлу шрифта (None для системного)
            color: Обычный цвет кнопки
            hover_color: Цвет при наведении
            text_color: Цвет текста
            border_color: Цвет границы
            border_radius: Радиус скругления углов (0 = острые углы)
        """
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font_size = font_size
        self.font_path = font_path
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.hovered = False
        self.pressed = False

        # Создаём шрифт
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, font_size)
            except:
                self.font = pygame.font.Font(None, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)

    def update(self, dt: float) -> None:
        """Обновить состояние кнопки."""
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать кнопку."""
        if not self.visible:
            return

        color = self.hover_color if self.hovered else self.color
        
        # Рисуем фон кнопки
        draw_rounded_rect(screen, color, self.rect, self.border_radius)
        
        # Рисуем границу кнопки
        draw_rounded_rect_border(screen, self.border_color, self.rect, self.border_radius, 2)

        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def set_font_size(self, size: int) -> None:
        """Изменить размер шрифта."""
        self.font_size = size
        if self.font_path:
            try:
                self.font = pygame.font.Font(self.font_path, size)
            except:
                self.font = pygame.font.Font(None, size)
        else:
            self.font = pygame.font.Font(None, size)

    def set_font(self, font_path: str) -> None:
        """Изменить файл шрифта."""
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
        """Изменить цвета кнопки."""
        if color is not None:
            self.color = color
        if hover_color is not None:
            self.hover_color = hover_color
        if text_color is not None:
            self.text_color = text_color
        if border_color is not None:
            self.border_color = border_color

    def set_border_radius(self, radius: int) -> None:
        """Установить радиус скругления углов."""
        self.border_radius = max(0, radius)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обработать события мыши."""
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
    """Элемент интерфейса полосы здоровья/прогресса."""

    def __init__(self, x: int, y: int, width: int, height: int, max_value: float = 100, border_radius: int = 0):
        """
        Создать полосу здоровья.
        
        Args:
            x, y: Позиция полосы
            width, height: Размеры полосы
            max_value: Максимальное значение
            border_radius: Радиус скругления углов (0 = острые углы)
        """
        super().__init__(x, y, width, height)
        self.max_value = max_value
        self.current_value = max_value
        self.background_color = (50, 50, 50)
        self.fill_color = (0, 255, 0)
        self.border_color = (255, 255, 255)
        self.border_radius = border_radius

    def update(self, dt: float) -> None:
        """Обновить полосу здоровья."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать полосу здоровья."""
        if not self.visible:
            return

        # Рисуем фон
        draw_rounded_rect(screen, self.background_color, self.rect, self.border_radius)

        # Рисуем заполнение
        if self.current_value > 0:
            fill_width = int((self.current_value / self.max_value) * self.rect.width)
            fill_rect = pygame.Rect(
                self.rect.x, self.rect.y, fill_width, self.rect.height
            )
            draw_rounded_rect(screen, self.fill_color, fill_rect, self.border_radius)

        # Рисуем границу
        draw_rounded_rect_border(screen, self.border_color, self.rect, self.border_radius, 2)

    def set_value(self, value: float) -> None:
        """Установить текущее значение."""
        self.current_value = max(0, min(self.max_value, value))

    def get_percentage(self) -> float:
        """Получить значение в процентах (0.0 до 1.0)."""
        return self.current_value / self.max_value if self.max_value > 0 else 0

    def set_colors(
        self,
        background_color: Tuple[int, int, int] = None,
        fill_color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
    ) -> None:
        """Изменить цвета полосы."""
        if background_color is not None:
            self.background_color = background_color
        if fill_color is not None:
            self.fill_color = fill_color
        if border_color is not None:
            self.border_color = border_color

    def set_border_radius(self, radius: int) -> None:
        """Установить радиус скругления углов."""
        self.border_radius = max(0, radius)


class ProgressBar(HealthBar):
    """Полоса прогресса (псевдоним для HealthBar)."""

    def __init__(self, x: int, y: int, width: int, height: int, max_value: float = 100, border_radius: int = 0):
        """
        Создать полосу прогресса.
        
        Args:
            x: Позиция X полосы
            y: Позиция Y полосы
            width: Ширина полосы
            height: Высота полосы
            max_value: Максимальное значение
            border_radius: Радиус скругления углов (0 = острые углы)
        """
        super().__init__(x, y, width, height, max_value, border_radius)
        self.fill_color = (0, 100, 255)


class Text(UIElement):
    """Элемент интерфейса для отображения текста."""

    def __init__(
        self,
        x: int,
        y: int,
        text: str = "",
        size: int = 24,
        color: Tuple[int, int, int] = (255, 255, 255),
        font_path: Optional[str] = None,
    ):
        """
        Создать текстовый элемент.
        
        Args:
            x: Позиция X текста
            y: Позиция Y текста
            text: Отображаемый текст
            size: Размер шрифта
            color: Цвет текста
            font_path: Путь к файлу шрифта (None для системного)
        """
        self.text = text
        self.size = size
        self.color = color
        self.font_path = font_path

        # Создаём шрифт
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, size)
            except:
                self.font = pygame.font.Font(None, size)
        else:
            self.font = pygame.font.Font(None, size)

        # Вычисляем размер на основе текста
        text_surface = self.font.render(text or " ", True, color)
        super().__init__(x, y, text_surface.get_width(), text_surface.get_height())

    def update(self, dt: float) -> None:
        """Обновить текст."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать текст."""
        if not self.visible or not self.text:
            return

        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.rect.topleft)

    def set_text(self, text: str) -> None:
        """Установить содержимое текста."""
        self.text = text
        text_surface = self.font.render(text or " ", True, self.color)
        self.rect.width = text_surface.get_width()
        self.rect.height = text_surface.get_height()

    def set_color(self, color: Tuple[int, int, int]) -> None:
        """Изменить цвет текста."""
        self.color = color

    def set_font_size(self, size: int) -> None:
        """Изменить размер шрифта."""
        self.size = size
        if self.font_path:
            try:
                self.font = pygame.font.Font(self.font_path, size)
            except:
                self.font = pygame.font.Font(None, size)
        else:
            self.font = pygame.font.Font(None, size)

        # Пересчитываем размер
        text_surface = self.font.render(self.text or " ", True, self.color)
        self.rect.width = text_surface.get_width()
        self.rect.height = text_surface.get_height()

    def set_font(self, font_path: str) -> None:
        """Изменить файл шрифта."""
        self.font_path = font_path
        try:
            self.font = pygame.font.Font(font_path, self.size)
        except:
            self.font = pygame.font.Font(None, self.size)

        # Пересчитываем размер
        text_surface = self.font.render(self.text or " ", True, self.color)
        self.rect.width = text_surface.get_width()
        self.rect.height = text_surface.get_height()


class Panel(UIElement):
    """Простой элемент панели/контейнера интерфейса."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int] = (50, 50, 50),
        border_color: Optional[Tuple[int, int, int]] = None,
        border_radius: int = 0,
    ):
        """
        Создать панель.
        
        Args:
            x, y: Позиция панели
            width, height: Размеры панели
            color: Цвет панели
            border_color: Цвет границы (None для отсутствия границы)
            border_radius: Радиус скругления углов (0 = острые углы)
        """
        super().__init__(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_radius = border_radius
        self.border_width = 2 if border_color else 0

    def update(self, dt: float) -> None:
        """Обновить панель."""
        pass

    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать панель."""
        if not self.visible:
            return

        draw_rounded_rect(screen, self.color, self.rect, self.border_radius)

        if self.border_color:
            draw_rounded_rect_border(screen, self.border_color, self.rect, self.border_radius, self.border_width)

    def set_colors(
        self,
        color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
    ) -> None:
        """Изменить цвета панели."""
        if color is not None:
            self.color = color
        if border_color is not None:
            self.border_color = border_color

    def set_border_radius(self, radius: int) -> None:
        """Установить радиус скругления углов."""
        self.border_radius = max(0, radius)


class TextInput(UIElement):
    """Поле ввода текста."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        placeholder: str = "",
        max_length: int = 50,
        font_size: int = 24,
        font_path: Optional[str] = None,
        background_color: Tuple[int, int, int] = (255, 255, 255),
        text_color: Tuple[int, int, int] = (0, 0, 0),
        placeholder_color: Tuple[int, int, int] = (128, 128, 128),
        border_color: Tuple[int, int, int] = (100, 100, 100),
        active_border_color: Tuple[int, int, int] = (0, 120, 215),
        cursor_color: Tuple[int, int, int] = (0, 0, 0),
        border_radius: int = 0,
    ):
        """
        Создать поле ввода текста.
        
        Args:
            x: Позиция X поля
            y: Позиция Y поля
            width: Ширина поля
            height: Высота поля
            placeholder: Текст-подсказка
            max_length: Максимальная длина текста
            font_size: Размер шрифта
            font_path: Путь к файлу шрифта (None для системного)
            background_color: Цвет фона
            text_color: Цвет текста
            placeholder_color: Цвет текста-подсказки
            border_color: Цвет границы
            active_border_color: Цвет границы при фокусе
            cursor_color: Цвет курсора
            border_radius: Радиус скругления углов (0 = острые углы)
        """
        super().__init__(x, y, width, height)
        self.text = ""
        self.placeholder = placeholder
        self.max_length = max_length
        self.font_size = font_size
        self.font_path = font_path
        self.background_color = background_color
        self.text_color = text_color
        self.placeholder_color = placeholder_color
        self.border_color = border_color
        self.active_border_color = active_border_color
        self.cursor_color = cursor_color
        self.border_radius = border_radius
        
        # Состояние поля
        self.active = False
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0.0
        self.cursor_blink_rate = 0.5  # Моргание курсора каждые 0.5 секунд
        
        # Создаём шрифт
        if font_path:
            try:
                self.font = pygame.font.Font(font_path, font_size)
            except:
                self.font = pygame.font.Font(None, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)
    
    def update(self, dt: float) -> None:
        """Обновить состояние поля ввода."""
        if self.active:
            # Обновление моргания курсора
            self.cursor_timer += dt
            if self.cursor_timer >= self.cursor_blink_rate:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0.0
    
    def draw(self, screen: pygame.Surface) -> None:
        """Нарисовать поле ввода."""
        if not self.visible:
            return
        
        # Рисуем фон
        draw_rounded_rect(screen, self.background_color, self.rect, self.border_radius)
        
        # Рисуем границу
        border_color = self.active_border_color if self.active else self.border_color
        draw_rounded_rect_border(screen, border_color, self.rect, self.border_radius, 2)
        
        # Подготавливаем текст для отображения
        display_text = self.text if self.text else self.placeholder
        text_color = self.text_color if self.text else self.placeholder_color
        
        if display_text:
            # Обрезаем текст, если он не помещается
            text_surface = self.font.render(display_text, True, text_color)
            text_width = text_surface.get_width()
            
            # Если текст слишком длинный, обрезаем его слева
            if text_width > self.rect.width - 10:
                # Находим позицию, с которой начинать отображение
                chars_to_show = len(display_text)
                while chars_to_show > 0:
                    test_text = display_text[-chars_to_show:]
                    test_surface = self.font.render(test_text, True, text_color)
                    if test_surface.get_width() <= self.rect.width - 10:
                        break
                    chars_to_show -= 1
                
                if chars_to_show > 0:
                    display_text = display_text[-chars_to_show:]
                    text_surface = self.font.render(display_text, True, text_color)
            
            # Позиционируем текст
            text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
            screen.blit(text_surface, (self.rect.x + 5, text_y))
        
        # Рисуем курсор
        if self.active and self.cursor_visible and self.text:
            # Вычисляем позицию курсора
            cursor_text = self.text[:self.cursor_pos]
            cursor_width = self.font.size(cursor_text)[0] if cursor_text else 0
            
            # Учитываем обрезку текста
            text_surface_width = self.font.size(display_text)[0] if display_text else 0
            text_offset = max(0, text_surface_width - (self.rect.width - 10))
            
            cursor_x = self.rect.x + 5 + cursor_width - text_offset
            cursor_y = self.rect.y + 3
            cursor_height = self.rect.height - 6
            
            # Рисуем курсор только если он виден
            if cursor_x >= self.rect.x + 5 and cursor_x <= self.rect.x + self.rect.width - 5:
                pygame.draw.line(screen, self.cursor_color, 
                               (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Обработать события ввода."""
        if not self.enabled or not self.visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                if self.rect.collidepoint(event.pos):
                    self.activate()
                    # Позиционируем курсор по клику
                    self._position_cursor_at_click(event.pos)
                    return True
                else:
                    self.deactivate()
                    return False
        
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                return True
            
            elif event.key == pygame.K_DELETE:
                if self.cursor_pos < len(self.text):
                    self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                return True
            
            elif event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
                return True
            
            elif event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                return True
            
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
                return True
            
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
                return True
            
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self.deactivate()
                return True
            
            elif event.key == pygame.K_ESCAPE:
                self.deactivate()
                return True
        
        elif event.type == pygame.TEXTINPUT and self.active:
            # Добавляем введённый текст
            if len(self.text) < self.max_length:
                char = event.text
                # Фильтруем недопустимые символы
                if char.isprintable() and char != '\r' and char != '\n':
                    self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                    self.cursor_pos += 1
            return True
        
        return False
    
    def _position_cursor_at_click(self, pos: Tuple[int, int]) -> None:
        """Позиционировать курсор по позиции клика."""
        click_x = pos[0] - self.rect.x - 5
        
        # Находим ближайшую позицию курсора
        best_pos = 0
        best_distance = float('inf')
        
        for i in range(len(self.text) + 1):
            text_to_cursor = self.text[:i]
            cursor_x = self.font.size(text_to_cursor)[0] if text_to_cursor else 0
            distance = abs(cursor_x - click_x)
            
            if distance < best_distance:
                best_distance = distance
                best_pos = i
        
        self.cursor_pos = best_pos
    
    def activate(self) -> None:
        """Активировать поле ввода (установить фокус)."""
        self.active = True
        self.cursor_visible = True
        self.cursor_timer = 0.0
        pygame.key.set_repeat(500, 50)  # Включаем повтор клавиш
    
    def deactivate(self) -> None:
        """Деактивировать поле ввода (убрать фокус)."""
        self.active = False
        self.cursor_visible = False
        pygame.key.set_repeat()  # Отключаем повтор клавиш
    
    def get_text(self) -> str:
        """Получить текущий текст в поле."""
        return self.text
    
    def set_text(self, text: str) -> None:
        """Установить текст в поле."""
        self.text = text[:self.max_length]  # Обрезаем до максимальной длины
        self.cursor_pos = min(self.cursor_pos, len(self.text))
    
    def clear(self) -> None:
        """Очистить поле ввода."""
        self.text = ""
        self.cursor_pos = 0
    
    def set_placeholder(self, placeholder: str) -> None:
        """Установить текст-подсказку."""
        self.placeholder = placeholder
    
    def set_max_length(self, max_length: int) -> None:
        """Установить максимальную длину текста."""
        self.max_length = max_length
        if len(self.text) > max_length:
            self.text = self.text[:max_length]
            self.cursor_pos = min(self.cursor_pos, len(self.text))
    
    def set_font_size(self, size: int) -> None:
        """Изменить размер шрифта."""
        self.font_size = size
        if self.font_path:
            try:
                self.font = pygame.font.Font(self.font_path, size)
            except:
                self.font = pygame.font.Font(None, size)
        else:
            self.font = pygame.font.Font(None, size)
    
    def set_colors(
        self,
        background_color: Tuple[int, int, int] = None,
        text_color: Tuple[int, int, int] = None,
        placeholder_color: Tuple[int, int, int] = None,
        border_color: Tuple[int, int, int] = None,
        active_border_color: Tuple[int, int, int] = None,
        cursor_color: Tuple[int, int, int] = None,
    ) -> None:
        """Изменить цвета поля ввода."""
        if background_color is not None:
            self.background_color = background_color
        if text_color is not None:
            self.text_color = text_color
        if placeholder_color is not None:
            self.placeholder_color = placeholder_color
        if border_color is not None:
            self.border_color = border_color
        if active_border_color is not None:
            self.active_border_color = active_border_color
        if cursor_color is not None:
            self.cursor_color = cursor_color

    def set_border_radius(self, radius: int) -> None:
        """Установить радиус скругления углов."""
        self.border_radius = max(0, radius)
