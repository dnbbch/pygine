"""
Пример эффекта тряски экрана.
Демонстрирует различные варианты тряски при взрывах и других эффектах.
"""

import pygame
import pygine as pg
from pygine.effects import start_screen_shake, create_explosion, update_effects, draw_effects

# Инициализация игры
game = pg.Game(800, 600, "Эффект тряски экрана")

# Создание анимированного спрайта
sprite = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (400, 300))
sprite.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
sprite.play_animation("idle")
sprite.set_scale(3.0)

# Создание текстовых инструкций
text1 = pg.Text(10, 10, "1 - лёгкая тряска", size=18, color=(255, 255, 255))
text2 = pg.Text(10, 35, "2 - средняя тряска", size=18, color=(255, 255, 255))
text3 = pg.Text(10, 60, "3 - сильная тряска", size=18, color=(255, 255, 255))
text4 = pg.Text(10, 85, "4 - очень сильная тряска", size=18, color=(255, 255, 255))
text_exit = pg.Text(10, 110, "ESC - выход", size=18, color=(255, 255, 0))


def update():
    # Обновление эффектов (включая тряску)
    update_effects(game.get_delta_time())
    
    # Различные эффекты тряски
    if pg.key_pressed(pygame.K_1):
        # Лёгкая тряска
        start_screen_shake(2, 0.3)
        create_explosion(400, 300, 10)
    
    if pg.key_pressed(pygame.K_2):
        # Средняя тряска
        start_screen_shake(5, 0.5)
        create_explosion(400, 300, 15)
    
    if pg.key_pressed(pygame.K_3):
        # Сильная тряска
        start_screen_shake(8, 0.8)
        create_explosion(400, 300, 20)
    
    if pg.key_pressed(pygame.K_4):
        # Очень сильная тряска
        start_screen_shake(12, 1.0, 20)
        create_explosion(400, 300, 25)
    
    # Выход
    if pg.key_pressed(pygame.K_ESCAPE):
        pygame.quit()
        exit()


def draw():
    # Отрисовка спрайта
    game.screen.blit(sprite.image, sprite.rect)
    
    # Отрисовка эффектов (частицы)
    draw_effects(game.screen)
    
    # Отрисовка инструкций
    text1.draw(game.screen)
    text2.draw(game.screen)
    text3.draw(game.screen)
    text4.draw(game.screen)
    text_exit.draw(game.screen)


# Добавление спрайта в игру
game.add_sprite(sprite)

# Запуск игры
game.run(update, draw) 