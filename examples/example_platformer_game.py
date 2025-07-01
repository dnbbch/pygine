"""
Игра с полным управлением персонажем и физикой.
Демонстрирует движение, прыжки, анимации и различные состояния игрока.
"""

import pygine as pg
import pygame

# Запускаем pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1000, 600
# Коэффициент спустя который анимация "stand" включается
IDLE_TO_STAND = 2.0
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Test Game 2 - Player Control")
clock = pygame.time.Clock()

# Создаём игрока и его анимации
player = pg.AnimatedSprite("./platformer_sprites.png", (64, 64))
player.add_animation("stance", [0, 1, 2, 3], fps=8, loop=True)
player.add_animation("run", [4, 5, 6, 7, 8, 9, 10, 11], fps=12, loop=True)
player.add_animation("walk", [32, 33, 34, 35, 36, 37, 38, 39], fps=8, loop=True)
player.add_animation("duck", [40, 41], fps=8, loop=True)
player.add_animation("jump", [42, 43, 44, 45, 46, 47], fps=10, loop=False)
player.add_animation("stand", [64], fps=1, loop=False)

player.set_scale(1.5)

# Ставим игрока на землю с учётом масштаба
initial_ground_y = HEIGHT - (player.frame_size[1] * player.scale) / 2
player.set_position(WIDTH // 2, initial_ground_y)
player.play_animation("stance")

# Скорости движения
speed = 200
run_speed = 400

# Параметры прыжка
jump_speed = 0
gravity = 1500
jump_power = -500

idle_timer = 0.0  # таймер покоя

# Главный цикл игры
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # Проверяем выход
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()

    # Вычисляем границу земли и половину ширины на каждый кадр – учитываем масштаб
    half_w = (player.frame_size[0] * player.scale) / 2
    half_h = (player.frame_size[1] * player.scale) / 2
    ground_y = HEIGHT - half_h

    # Стоим ли на земле?
    on_ground = player.y >= ground_y - 0.1

    # Приседаем
    if keys[pygame.K_s] and on_ground:
        player.play_animation("duck")
        player.set_collision_rect(64, 32, 0, 0)
    else:
        player.reset_collision_to_default()

        # Прыгаем
        if keys[pygame.K_SPACE] and on_ground:
            jump_speed = jump_power
            player.play_animation("jump")

        # Ходим или бегаем
        elif keys[pygame.K_a]:
            player.x -= (run_speed if keys[pygame.K_LSHIFT] else speed) * dt
            if on_ground:
                player.play_animation("run" if keys[pygame.K_LSHIFT] else "walk")
            player.mirror(True)
        elif keys[pygame.K_d]:
            player.x += (run_speed if keys[pygame.K_LSHIFT] else speed) * dt
            if on_ground:
                player.play_animation("run" if keys[pygame.K_LSHIFT] else "walk")
            player.mirror(False)

    # Логика покоя
    moving = keys[pygame.K_a] or keys[pygame.K_d]
    crouching = keys[pygame.K_s]
    jumping = not on_ground

    if not moving and not crouching and not jumping:
        idle_timer += dt
        if idle_timer < IDLE_TO_STAND and player.get_current_animation() != "stance":
            player.play_animation("stance")
        elif idle_timer >= IDLE_TO_STAND and player.get_current_animation() != "stand":
            player.play_animation("stand")
    else:
        idle_timer = 0.0

    # Применяем гравитацию
    jump_speed += gravity * dt
    player.y += jump_speed * dt

    # Не проваливаемся сквозь землю
    if player.y > ground_y:
        player.y = ground_y
        jump_speed = 0

    # Не выходим за пределы экрана
    if player.x < half_w:
        player.x = half_w
    elif player.x > WIDTH - half_w:
        player.x = WIDTH - half_w

    # Обновляем анимацию
    player.update(dt)

    # Рисуем кадр
    window.fill((50, 100, 150))
    window.blit(player.image, player.rect)
    # player.debug_draw(window)  # показать хитбокс

    instructions = pg.Text(10, 10, "A/D - шаг, Shift+A/D - бег, S - присесть, Space - прыжок", size=20)
    instructions.draw(window)

    pygame.display.update()

pygame.quit() 