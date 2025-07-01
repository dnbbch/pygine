"""
Пример зеркалирования спрайта.
Демонстрирует управление направлением спрайта с помощью клавиш.
"""

import pygame
import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Зеркалирование спрайта")

# Создание и настройка спрайта
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(2.0)


def update():
    # Управление зеркалированием с помощью стрелок
    if pg.key_just_pressed(pygame.K_LEFT):
        sprite.mirror(True)  # Зеркалирование влево
        
    if pg.key_just_pressed(pygame.K_RIGHT):
        sprite.mirror(False)  # Обычное направление


def draw():
    # Отображение хитбокса
    sprite.debug_draw(game.screen)
    
    # Инструкции для пользователя
    instructions = [
        "Стрелка ВЛЕВО - зеркалировать",
        "Стрелка ВПРАВО - обычное направление"
    ]
    
    for i, text in enumerate(instructions):
        pg.Text(10, 10 + i * 25, text, size=16, color=(255, 255, 255)).draw(game.screen)
    
    # Текущий статус
    status = "Зеркалирован" if sprite._mirrored else "Обычное"
    pg.Text(10, 70, f"Статус: {status}", size=18, color=(255, 255, 0)).draw(game.screen)


# Добавление спрайта в игру
game.add_sprite(sprite)

# Запуск игры
game.run(update, draw)
