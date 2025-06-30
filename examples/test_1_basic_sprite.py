import pygame
import pygine as pg

# Создаем игру и спрайт
game = pg.Game(800, 600, "Тест создания спрайта")
sprite = pg.AnimatedSprite("./platformer_sprites_custom.png", (64, 64), (400, 300))
game.add_sprite(sprite)

# Запускаем игру
game.run()
