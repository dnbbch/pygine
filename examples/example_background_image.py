"""
Пример использования фоновых изображений в игре.
Демонстрирует автоматическое масштабирование фона под размеры окна.
"""

import pygame
import pygine as pg

# Инициализация игры с фоновым изображением
game = pg.Game(800, 600, "Фоновое изображение", background_image="background.png")

# Создание анимированного спрайта
sprite = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (400, 300))
sprite.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
sprite.play_animation("idle")
sprite.set_scale(3.0)


def update():
    # Управление фоном
    if pg.key_pressed(pygame.K_1):
        game.set_background_image("background.png")
    
    if pg.key_pressed(pygame.K_2):
        game.set_background_color((50, 50, 50))
    
    # Выход
    if pg.key_pressed(pygame.K_ESCAPE):
        pygame.quit()
        exit()


def draw():
    # Отрисовка спрайта
    game.screen.blit(sprite.image, sprite.rect)
    
    # Инструкции
    pg.Text(10, 10, "1 - фон картинка", size=20, color=(255, 255, 255)).draw(game.screen)
    pg.Text(10, 40, "2 - фон дефолтный", size=20, color=(255, 255, 255)).draw(game.screen)
    pg.Text(10, 70, "ESC - выход", size=20, color=(255, 255, 0)).draw(game.screen)


# Добавление спрайта в игру
game.add_sprite(sprite)

# Запуск игры
game.run(update, draw) 