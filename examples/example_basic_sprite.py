"""
Базовый пример создания и отображения спрайта.
Демонстрирует основы загрузки спрайта из файла и его добавления в игру.
"""

import os
import pygine as pg

_ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# Инициализация игры с размером окна и заголовком
game = pg.Game(800, 600, "Базовый спрайт")

# Создание спрайта из файла спрайтшита
# Параметры: путь к файлу, размер кадра (ширина, высота), позиция (x, y)
sprite = pg.AnimatedSprite(os.path.join(_ASSETS_DIR, "platformer_sprites.png"), (64, 64), (400, 300))

# Добавление спрайта в игру для отображения
game.add_sprite(sprite)

# Запуск основного игрового цикла
game.run()
