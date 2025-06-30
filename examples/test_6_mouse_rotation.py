import pygame
import pygine as pg

# Создаем игру и спрайт
game = pg.Game(800, 600, "Тест поворота к мыши")
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(2.0)


def update():
    sprite.rotate_towards_mouse()  # Поворачиваем к курсору мыши


game.add_sprite(sprite)
game.run(update)
