"""
Пример скругленных элементов интерфейса.
Демонстрирует все UI элементы с разными радиусами скругления.
"""

import pygame
import sys
import os

# Добавляем путь к модулю pygine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygine as pg

# Инициализация игры
game = pg.Game(900, 700, "Скругленные элементы UI")

# Заголовок
title = pg.Text(450, 30, "Скругленные элементы интерфейса", size=32, color=(255, 255, 255))
title.rect.centerx = 450

# Кнопки с разным скруглением
sharp_button = pg.Button(50, 100, 150, 50, "Острые углы", border_radius=0, font_size=18)
round_button = pg.Button(220, 100, 150, 50, "Скругленные", border_radius=10, font_size=18)
very_round_button = pg.Button(390, 100, 150, 50, "Очень круглые", border_radius=25, font_size=18)

# Полосы здоровья с разным скруглением
pg.Text(50, 180, "Полосы прогресса:", size=20, color=(200, 200, 200)).draw = lambda s: None
sharp_health = pg.HealthBar(50, 210, 200, 30, border_radius=0)
sharp_health.set_value(80)

round_health = pg.HealthBar(50, 250, 200, 30, border_radius=8)
round_health.set_value(60)
round_health.set_colors(fill_color=(255, 165, 0))

very_round_health = pg.HealthBar(50, 290, 200, 30, border_radius=15)
very_round_health.set_value(40)
very_round_health.set_colors(fill_color=(255, 100, 100))

# Полосы прогресса
sharp_progress = pg.ProgressBar(280, 210, 200, 30, border_radius=0)
sharp_progress.set_value(70)

round_progress = pg.ProgressBar(280, 250, 200, 30, border_radius=8)
round_progress.set_value(50)

very_round_progress = pg.ProgressBar(280, 290, 200, 30, border_radius=15)
very_round_progress.set_value(30)

# Поля ввода с разным скруглением
input_label = pg.Text(50, 340, "Поля ввода:", size=20, color=(200, 200, 200))

sharp_input = pg.TextInput(50, 370, 200, 40, placeholder="Острые углы", border_radius=0)
round_input = pg.TextInput(280, 370, 200, 40, placeholder="Скругленные", border_radius=8)
very_round_input = pg.TextInput(510, 370, 200, 40, placeholder="Очень круглые", border_radius=20)

# Панели с разным скруглением
panel_label = pg.Text(50, 440, "Панели:", size=20, color=(200, 200, 200))

sharp_panel = pg.Panel(50, 470, 150, 100, color=(80, 80, 120), border_color=(150, 150, 200), border_radius=0)
round_panel = pg.Panel(220, 470, 150, 100, color=(80, 120, 80), border_color=(150, 200, 150), border_radius=15)
very_round_panel = pg.Panel(390, 470, 150, 100, color=(120, 80, 80), border_color=(200, 150, 150), border_radius=30)

# Тексты на панелях
sharp_text = pg.Text(125, 510, "Острые", size=16, color=(255, 255, 255))
sharp_text.rect.centerx = 125

round_text = pg.Text(295, 510, "Скругл.", size=16, color=(255, 255, 255))
round_text.rect.centerx = 295

very_round_text = pg.Text(465, 510, "Круглые", size=16, color=(255, 255, 255))
very_round_text.rect.centerx = 465

# Список всех UI элементов для обработки
ui_elements = [
    sharp_button, round_button, very_round_button,
    sharp_health, round_health, very_round_health,
    sharp_progress, round_progress, very_round_progress,
    sharp_input, round_input, very_round_input,
    sharp_panel, round_panel, very_round_panel
]

# Инструкция
instruction = pg.Text(450, 600, "Все элементы поддерживают параметр border_radius", size=18, color=(180, 180, 180))
instruction.rect.centerx = 450

instruction2 = pg.Text(450, 630, "0 = острые углы, больше = более скругленные", size=16, color=(150, 150, 150))
instruction2.rect.centerx = 450


def button_click():
    """Функция для демонстрации работы кнопок."""
    print("Кнопка нажата!")


# Привязываем функции к кнопкам
sharp_button.callback = button_click
round_button.callback = button_click
very_round_button.callback = button_click


def update():
    # Обновление всех элементов
    for element in ui_elements:
        element.update(game.get_delta_time())
    
    # Выход
    if pg.key_pressed(pygame.K_ESCAPE):
        pygame.quit()
        exit()


def draw():
    # Отрисовка заголовка
    title.draw(game.screen)
    
    # Отрисовка меток
    pg.Text(50, 180, "Полосы здоровья:", size=20, color=(200, 200, 200)).draw(game.screen)
    pg.Text(280, 180, "Полосы прогресса:", size=20, color=(200, 200, 200)).draw(game.screen)
    input_label.draw(game.screen)
    panel_label.draw(game.screen)
    
    # Отрисовка всех UI элементов
    for element in ui_elements:
        element.draw(game.screen)
    
    # Отрисовка текстов на панелях
    sharp_text.draw(game.screen)
    round_text.draw(game.screen)
    very_round_text.draw(game.screen)
    
    # Отрисовка инструкций
    instruction.draw(game.screen)
    instruction2.draw(game.screen)


def handle_event(event):
    """Обработка событий для UI элементов."""
    for element in ui_elements:
        element.handle_event(event)


# Добавляем обработчик событий
game.add_event_callback(handle_event)

# Запуск игры
game.run(update, draw) 