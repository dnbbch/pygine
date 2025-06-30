import pygame
import pygine as pg

# Создаем игру и спрайт
game = pg.Game(800, 600, "Тест движения")
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(2.0)

# Скорость движения
speed = 5  # пикселей в секунду


def update():
    # Обрабатываем движение
    if pg.key_pressed(pygame.K_LEFT):
        sprite.x -= speed
        sprite.mirror(True)  # Зеркалим влево

    if pg.key_pressed(pygame.K_RIGHT):
        sprite.x += speed
        sprite.mirror(False)  # Обычное направление

    if pg.key_pressed(pygame.K_UP):
        sprite.y -= speed

    if pg.key_pressed(pygame.K_DOWN):
        sprite.y += speed


def draw():
    # Показываем хитбокс для наглядности
    sprite.debug_draw(game.screen)

    # Координаты спрайта
    pg.Text(0, 0, f"X: {sprite.x:.1f}", size=18, color=(255, 255, 0)).draw(game.screen)
    pg.Text(0, 15, f"Y: {sprite.y:.1f}", size=18, color=(255, 255, 0)).draw(game.screen)


game.add_sprite(sprite)
game.run(update, draw)
