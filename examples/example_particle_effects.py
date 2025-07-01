"""
Пример системы частиц и визуальных эффектов.
Демонстрирует создание различных эффектов: взрывов, дыма и искр.
"""

import pygame
import pygine as pg
from pygine.effects import create_explosion, create_smoke, create_sparkles, update_effects, draw_effects

# Инициализация игры
game = pg.Game(800, 600, "Система эффектов")

# Создание игрока
player = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (400, 300))
player.add_animation("idle", [0], fps=1)
player.play_animation("idle")
player.set_scale(2.0)

# Параметры автоматических эффектов
effect_timer = 0
effect_interval = 0.8


def update():
    global effect_timer
    
    # Перемещение игрока за мышью
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.set_position(mouse_x, mouse_y)
    
    # Обновление всех эффектов
    update_effects(game.get_delta_time())
    
    # Создание автоматических эффектов вокруг игрока
    effect_timer += game.get_delta_time()
    if effect_timer >= effect_interval:
        effect_timer = 0
        create_explosion(mouse_x + 50, mouse_y, 12)
        create_smoke(mouse_x - 50, mouse_y, 8)
        create_sparkles(mouse_x, mouse_y - 50, 10)


def draw():
    # Очистка экрана
    game.screen.fill((30, 30, 60))
    
    # Отрисовка игрока
    game.screen.blit(player.image, player.rect)
    
    # Отрисовка всех эффектов
    draw_effects(game.screen)
    
    # Инструкции для пользователя
    instructions = [
        "Двигайте мышью - автоматические эффекты",
        "ЛКМ - взрыв, ПКМ - дым, СКМ - искры"
    ]
    
    for i, text in enumerate(instructions):
        pg.Text(10, 10 + i * 25, text, size=16, color=(255, 255, 255)).draw(game.screen)


def handle_mouse_clicks(event):
    # Создание эффектов по клику мыши
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        if event.button == 1:  # Левая кнопка - взрыв
            create_explosion(mouse_x, mouse_y, 20)
        elif event.button == 3:  # Правая кнопка - дым
            create_smoke(mouse_x, mouse_y, 15)
        elif event.button == 2:  # Средняя кнопка - искры
            create_sparkles(mouse_x, mouse_y, 25)


# Подключение обработчика событий
game.add_event_callback(handle_mouse_clicks)

# Добавление спрайта в игру
game.add_sprite(player)

# Запуск игры
game.run(update, draw) 