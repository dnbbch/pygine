"""
Пример системы камеры, которая следует за игроком.
Демонстрирует работу камеры и смещение объектов при её движении.
"""

import pygame
import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Система камеры")
camera = pg.Camera(800, 600)

# Создание игрока с анимацией
player = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (400, 300))
player.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
player.play_animation("idle")
player.set_scale(3.0)

# Создание объектов для демонстрации движения камеры
objects = []

# Объект 1 - левый верх
obj1 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (100, 100))
obj1.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
obj1.play_animation("idle")
objects.append(obj1)

# Объект 2 - правый верх
obj2 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (700, 200))
obj2.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
obj2.play_animation("idle")
objects.append(obj2)

# Объект 3 - левый низ
obj3 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (300, 500))
obj3.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
obj3.play_animation("idle")
objects.append(obj3)

# Объект 4 - правый низ
obj4 = pg.AnimatedSprite("platformer_sprites.png", (64, 64), (900, 400))
obj4.add_animation("idle", [0, 1, 2, 3], fps=5, loop=True)
obj4.play_animation("idle")
objects.append(obj4)

# Добавление всех спрайтов в игру
game.add_sprite(player)
for obj in objects:
    game.add_sprite(obj)

# Скорость перемещения игрока
speed = 200


def update():
    dt = game.get_delta_time()
    
    # Управление игроком стрелками
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= speed * dt
    if keys[pygame.K_RIGHT]:
        player.x += speed * dt
    if keys[pygame.K_UP]:
        player.y -= speed * dt
    if keys[pygame.K_DOWN]:
        player.y += speed * dt
    
    # Настройка камеры для следования за игроком
    camera.follow(player)
    camera.update(dt)


def draw():
    # Очистка экрана
    game.screen.fill((50, 100, 50))
    
    # Получение смещения камеры
    camera_offset = camera.get_offset()
    
    # Отрисовка всех объектов с учётом смещения камеры
    all_sprites = [player] + objects
    for sprite in all_sprites:
        screen_x = sprite.rect.x + camera_offset[0]
        screen_y = sprite.rect.y + camera_offset[1]
        game.screen.blit(sprite.image, (screen_x, screen_y))
    
    # Отображение информации (фиксировано на экране)
    info_lines = [
        "Стрелки - движение игрока",
        "Камера следует за игроком",
        f"Позиция: {player.x:.0f}, {player.y:.0f}"
    ]
    
    for i, line in enumerate(info_lines):
        color = (255, 255, 0) if i == 2 else (255, 255, 255)
        pg.Text(10, 10 + i * 25, line, size=18, color=color).draw(game.screen)


# Запуск игры
game.run(update, draw) 