"""
Пример масштабирования спрайтов.
Демонстрирует изменение размера спрайта с помощью функции масштабирования.
"""

import os
import pygine as pg

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# Инициализация игры
game = pg.Game(800, 600, "Масштабирование спрайта")

# Создание спрайта с базовым размером
sprite = pg.AnimatedSprite(os.path.join(_ASSETS_DIR, "platformer_sprites.png"), (64, 64), (400, 300))

# Применение масштабирования
# Значение 3.0 увеличивает спрайт в 3 раза от оригинального размера
sprite.set_scale(3.0)

# Добавление спрайта в игру
game.add_sprite(sprite)

# Запуск игрового цикла
game.run()
