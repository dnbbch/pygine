"""
Пример поворота спрайта в направлении курсора мыши.
Демонстрирует автоматическое слежение спрайта за положением мыши.
"""

import pygame
import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Поворот к мыши")

# Создание и настройка спрайта
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(2.0)


def update():
    # Автоматический поворот спрайта в направлении курсора мыши
    sprite.rotate_towards_mouse()


def draw():
    # Отображение инструкции
    pg.Text(10, 10, "Двигайте мышью - спрайт будет поворачиваться", 
            size=16, color=(255, 255, 255)).draw(game.screen)


# Добавление спрайта в игру
game.add_sprite(sprite)

# Запуск игры
game.run(update, draw)
