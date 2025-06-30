"""
Тест 11: Камера
Демонстрирует систему камеры, которая следует за игроком
"""

import pygame
import pygine as pg

# Инициализация
pygame.init()
game = pg.Game(800, 600, "Тест 11: Камера")
camera = pg.Camera(800, 600)

# Игрок (управляется стрелками)
player = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (400, 300))
player.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
player.play_animation("idle")
player.set_scale(3.0)

# Несколько объектов на карте
object1 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (100, 100))
object1.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
object1.play_animation("idle")

object2 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (700, 200))
object2.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
object2.play_animation("idle")

object3 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (300, 500))
object3.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
object3.play_animation("idle")

object4 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (900, 400))
object4.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
object4.play_animation("idle")

game.add_sprite(player)
game.add_sprite(object1)
game.add_sprite(object2)
game.add_sprite(object3)
game.add_sprite(object4)


# Скорость движения
speed = 200


def update():
    """Обновление игры"""
    dt = game.get_delta_time()
    
    # Движение игрока стрелками
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed * dt
    if keys[pygame.K_RIGHT]:
        player.x += speed * dt
    if keys[pygame.K_UP]:
        player.y -= speed * dt
    if keys[pygame.K_DOWN]:
        player.y += speed * dt
    
    # Камера следует за игроком
    camera.follow(player)
    
    # Обновляем камеру
    camera.update(dt)

def draw():
    """Отрисовка игры"""
    # Очищаем экран
    game.screen.fill((50, 100, 50))
    
    # Получаем смещение камеры
    camera_offset = camera.get_offset()
    
    # Рисуем все объекты с учетом камеры
    objects = [player, object1, object2, object3, object4]
    for obj in objects:
        # Применяем смещение камеры к позиции объекта
        screen_x = obj.rect.x + camera_offset[0]
        screen_y = obj.rect.y + camera_offset[1]
        game.screen.blit(obj.image, (screen_x, screen_y))
    
    # Инструкции (не двигаются с камерой)
    font = pygame.font.Font(None, 36)
    text1 = font.render("Стрелки - движение игрока", True, (255, 255, 255))
    text2 = font.render("Камера следует за игроком", True, (255, 255, 255))
    text3 = font.render(f"Позиция: {player.x:.0f}, {player.y:.0f}", True, (255, 255, 0))
    
    game.screen.blit(text1, (10, 10))
    game.screen.blit(text2, (10, 35))
    game.screen.blit(text3, (10, 60))

# Запуск игры
print("ЗАПУСК: Начинаем тест камеры")
game.run(update, draw)
print("ЗАВЕРШЕНИЕ: Тест камеры завершен") 