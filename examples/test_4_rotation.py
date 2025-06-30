import pygine as pg

# Создаем игру и спрайт
game = pg.Game(800, 600, "Тест поворота с хитбоксами")
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(2.0)


def update():
    sprite.rotate(2)


def draw():
    sprite.debug_draw(game.screen)


game.add_sprite(sprite)
game.run(update, draw)
