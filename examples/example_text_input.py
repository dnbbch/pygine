"""
Пример использования поля ввода текста.
Демонстрирует простое поле ввода имени.
"""

import pygame
import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Поле ввода текста")

# Создание элементов интерфейса
title = pg.Text(400, 100, "Введи своё имя", size=36, color=(255, 255, 255))
title.rect.centerx = 400

# Поле ввода имени
name_input = pg.TextInput(250, 200, 300, 50, placeholder="Твоё имя", max_length=20, font_size=24, border_radius=12)

# Кнопка
submit_button = pg.Button(300, 300, 200, 60, "Привет!", font_size=28, border_radius=15)

# Текст результата
result_text = pg.Text(400, 400, "", size=24, color=(0, 255, 0))
result_text.rect.centerx = 400

# Инструкция
instruction = pg.Text(400, 500, "Кликни по полю, введи имя и нажми кнопку", size=18, color=(200, 200, 200))
instruction.rect.centerx = 400


def say_hello():
    """Поздороваться с пользователем."""
    name = name_input.get_text()
    if name:
        result_text.set_text(f"Привет, {name}!")
        result_text.rect.centerx = 400
    else:
        result_text.set_text("Сначала введи имя!")
        result_text.set_color((255, 100, 100))
        result_text.rect.centerx = 400


# Привязываем функцию к кнопке
submit_button.callback = say_hello


def update():
    # Обновление элементов
    name_input.update(game.get_delta_time())
    submit_button.update(game.get_delta_time())
    
    # Выход
    if pg.key_pressed(pygame.K_ESCAPE):
        pygame.quit()
        exit()


def draw():
    # Отрисовка всех элементов
    title.draw(game.screen)
    name_input.draw(game.screen)
    submit_button.draw(game.screen)
    result_text.draw(game.screen)
    instruction.draw(game.screen)


def handle_event(event):
    """Обработка событий для поля ввода и кнопки."""
    name_input.handle_event(event)
    submit_button.handle_event(event)


# Добавляем обработчик событий
game.add_event_callback(handle_event)

# Запуск игры
game.run(update, draw) 