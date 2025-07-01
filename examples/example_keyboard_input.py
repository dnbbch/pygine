"""
Пример управления движением спрайта с клавиатуры.
Демонстрирует базовое перемещение с помощью стрелок и зеркалирование при смене направления.
"""

import pygame
import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Движение спрайта")

# Создание и настройка спрайта
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(2.0)

# Параметры движения
speed = 5


def update():
    # Горизонтальное движение
    if pg.key_pressed(pygame.K_LEFT):
        sprite.x -= speed
        sprite.mirror(True)  # Зеркалирование при движении влево
        
    if pg.key_pressed(pygame.K_RIGHT):
        sprite.x += speed
        sprite.mirror(False)  # Обычное направление при движении вправо
    
    # Вертикальное движение
    if pg.key_pressed(pygame.K_UP):
        sprite.y -= speed
        
    if pg.key_pressed(pygame.K_DOWN):
        sprite.y += speed


def draw():
    # Отображение хитбокса
    sprite.debug_draw(game.screen)
    
    # Инструкции управления
    instructions = [
        "Используйте стрелки для движения",
        f"Позиция: X={sprite.x:.1f}, Y={sprite.y:.1f}"
    ]
    
    for i, text in enumerate(instructions):
        color = (255, 255, 255) if i == 0 else (255, 255, 0)
        pg.Text(10, 10 + i * 20, text, size=16, color=color).draw(game.screen)


# Добавление спрайта в игру
game.add_sprite(sprite)

# Запуск игры
game.run(update, draw)
