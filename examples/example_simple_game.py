"""
Простая игра с анимированным персонажем.
Демонстрирует базовое использование игрового движка pygine.
"""

import pygine as pg
import pygame

# Инициализация pygame
pygame.init()

WIDTH, HEIGHT = 800, 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game 1 - Native pygame loop")
clock = pygame.time.Clock()

player = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
player.add_animation("walk", [0, 1, 2, 3], fps=5, loop=True)
player.add_animation("run", [4, 5, 6, 7, 8, 9, 10, 11], fps=30, loop=True)

offset_y = 10
player.set_position(WIDTH // 2, HEIGHT - player.frame_size[1] // 2 - offset_y)

# Нативный игровой цикл pygame
running = True
while running:
    dt = clock.tick(60) / 1000.0  # delta time в секундах
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    player.play_animation("run")
    player.update(dt)  # используем метод из pygine
    
    window.fill((30, 30, 60))  # фон
    window.blit(player.image, (player.rect.x, player.rect.y))  # рисуем спрайт напрямую
    
    pygame.display.update()

# Завершение
pygame.quit()
