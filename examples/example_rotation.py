"""
Пример поворота спрайта с отображением хитбокса.
Демонстрирует автоматический поворот спрайта и визуализацию области коллизий.
"""

import os
import pygine as pg

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")


# Инициализация игры
game = pg.Game(800, 600, "Поворот спрайта")

# Создание и настройка спрайта
sprite = pg.AnimatedSprite(os.path.join(_ASSETS_DIR, "platformer_sprites.png"), (64, 64), (400, 300))
sprite.set_scale(2.0)


def update():
    # Постоянный поворот спрайта на 2 градуса за кадр
    sprite.rotate(2)


def draw():
    # Отображение хитбокса для демонстрации поворота
    sprite.debug_draw(game.screen)


# Добавление спрайта в игру
game.add_sprite(sprite)

# Запуск игры с пользовательскими функциями обновления и отрисовки
game.run(update, draw)
