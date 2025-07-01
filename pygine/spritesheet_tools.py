"""
Инструменты для работы со спрайтшитами и визуализации макетов кадров
"""

import pygame
from typing import Tuple, Optional
from pathlib import Path


def visualize_spritesheet(
    image_path: str,
    frame_size: Tuple[int, int],
    output_path: Optional[str] = None,
    grid_color: Tuple[int, int, int] = (0, 255, 0),
    text_color: Tuple[int, int, int] = (255, 255, 255),
    text_bg_color: Tuple[int, int, int] = (0, 0, 0),
    font_size: int = 20,
) -> str:
    """
    Создать визуализацию спрайтшита с номерами кадров и наложением сетки.
    
    Args:
        image_path: Путь к файлу спрайтшита
        frame_size: Размер кадра (ширина, высота)
        output_path: Путь для сохранения визуализации (опционально)
        grid_color: Цвет сетки в формате RGB
        text_color: Цвет текста номеров кадров
        text_bg_color: Цвет фона под текстом
        font_size: Размер шрифта для номеров кадров
        
    Returns:
        Путь к сохранённому файлу визуализации
    """
    # Инициализируем pygame, если ещё не сделано
    if not pygame.get_init():
        pygame.init()

    # Инициализируем дисплей, если ещё не сделано (требуется для операций со шрифтами)
    if not pygame.display.get_init():
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

    # Загружаем спрайтшит
    original_image = pygame.image.load(image_path).convert_alpha()
    sheet_width = original_image.get_width()
    sheet_height = original_image.get_height()

    frame_width, frame_height = frame_size
    frames_per_row = sheet_width // frame_width
    frames_per_col = sheet_height // frame_height
    total_frames = frames_per_row * frames_per_col

    # Создаём высоту информационного заголовка
    info_height = 60

    # Создаём новое изображение с информационным заголовком
    viz_width = sheet_width
    viz_height = sheet_height + info_height
    viz_image = pygame.Surface((viz_width, viz_height), pygame.SRCALPHA)
    viz_image.fill((40, 40, 40))  # Тёмный фон для заголовка

    # Рисуем информационный заголовок
    font_big = pygame.font.Font(None, 24)
    font_small = pygame.font.Font(None, 18)

    # Основная информация
    info_text = font_big.render(
        f"Size: {sheet_width}x{sheet_height} | Frame: {frame_width}x{frame_height}",
        True,
        (255, 255, 255),
    )
    viz_image.blit(info_text, (10, 5))

    # Информация о сетке
    grid_text = font_small.render(
        f"Grid: {frames_per_row} cols x {frames_per_col} rows = {total_frames} frames",
        True,
        (200, 200, 200),
    )
    viz_image.blit(grid_text, (10, 30))

    # Рисуем оригинальный спрайтшит под заголовком
    viz_image.blit(original_image, (0, info_height))

    # Создаём шрифт для номеров кадров
    font = pygame.font.Font(None, font_size)

    # Рисуем сетку и номера кадров (со смещением на высоту заголовка)
    for row in range(frames_per_col):
        for col in range(frames_per_row):
            frame_index = row * frames_per_row + col

            # Вычисляем позицию кадра (со смещением на заголовок)
            x = col * frame_width
            y = row * frame_height + info_height

            # Рисуем линии сетки
            frame_rect = pygame.Rect(x, y, frame_width, frame_height)
            pygame.draw.rect(viz_image, grid_color, frame_rect, 2)

            # Рисуем номер кадра
            text_surface = font.render(str(frame_index), True, text_color)
            text_rect = text_surface.get_rect()

            # Позиционируем текст в углу кадра
            text_x = x + 2
            text_y = y + 2

            # Рисуем фон текста для лучшей читаемости
            bg_rect = pygame.Rect(
                text_x - 1, text_y - 1, text_rect.width + 2, text_rect.height + 2
            )
            pygame.draw.rect(viz_image, text_bg_color, bg_rect)

            # Рисуем текст
            viz_image.blit(text_surface, (text_x, text_y))

    # Определяем путь вывода
    if output_path is None:
        path_obj = Path(image_path)
        output_path = str(path_obj.parent / f"{path_obj.stem}_grid{path_obj.suffix}")

    # Сохраняем визуализацию
    pygame.image.save(viz_image, output_path)

    print(f"Визуализация спрайтшита сохранена в: {output_path}")
    print(f"Всего кадров: {total_frames} ({frames_per_row}x{frames_per_col})")
    print(f"Размер кадра: {frame_width}x{frame_height}")

    return output_path


def create_spritesheet_from_frames(
    source_sheet_path: str,
    frame_size: Tuple[int, int],
    frame_indices: list,
    output_path: Optional[str] = None,
    frames_per_row: int = None,
) -> str:
    """
    Создать новый компактный спрайтшит из выбранных кадров другого спрайтшита.

    Args:
        source_sheet_path: Путь к исходному спрайтшиту
        frame_size: (ширина, высота) каждого кадра
        frame_indices: Список индексов кадров для включения
        output_path: Где сохранить новый спрайтшит (опционально)
        frames_per_row: Сколько кадров в ряду (автоматически, если None)

    Returns:
        Путь к созданному файлу спрайтшита
    """
    if not pygame.get_init():
        pygame.init()

    # Инициализируем дисплей, если ещё не сделано
    if not pygame.display.get_init():
        pygame.display.set_mode((1, 1), pygame.HIDDEN)

    # Загружаем исходный спрайтшит
    source_sheet = pygame.image.load(source_sheet_path).convert_alpha()
    source_width = source_sheet.get_width()
    frame_width, frame_height = frame_size
    source_frames_per_row = source_width // frame_width

    # Извлекаем кадры из источника
    frames = []
    for frame_index in frame_indices:
        row = frame_index // source_frames_per_row
        col = frame_index % source_frames_per_row

        x = col * frame_width
        y = row * frame_height

        frame = pygame.Surface(frame_size, pygame.SRCALPHA)
        frame.blit(source_sheet, (0, 0), pygame.Rect(x, y, frame_width, frame_height))
        frames.append(frame)

    # Вычисляем размеры нового спрайтшита
    total_frames = len(frames)
    if frames_per_row is None:
        # Автоматически вычисляем оптимальную раскладку
        if total_frames <= 4:
            frames_per_row = total_frames
        elif total_frames <= 8:
            frames_per_row = 4
        else:
            frames_per_row = 8

    rows = (total_frames + frames_per_row - 1) // frames_per_row
    new_width = frames_per_row * frame_width
    new_height = rows * frame_height

    # Создаём новый компактный спрайтшит
    new_sheet = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
    new_sheet.fill((0, 0, 0, 0))  # Прозрачный фон

    # Размещаем кадры в новом листе
    for i, frame in enumerate(frames):
        row = i // frames_per_row
        col = i % frames_per_row

        x = col * frame_width
        y = row * frame_height

        new_sheet.blit(frame, (x, y))

    # Сохраняем новый спрайтшит
    if output_path is None:
        path_obj = Path(source_sheet_path)
        output_path = str(path_obj.parent / f"{path_obj.stem}_custom.png")

    pygame.image.save(new_sheet, output_path)

    print(f"Новый спрайтшит сохранён в: {output_path}")
    print(f"Кадры: {total_frames} ({frames_per_row}x{rows})")
    print(f"Размер: {new_width}x{new_height}")

    return output_path
