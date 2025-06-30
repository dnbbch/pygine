import pygine as pg

# Создаем игру и анимированный спрайт
game = pg.Game(800, 600, "Тест анимации")
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.add_animation("walk", [0, 1, 2, 3], fps=5, loop=True)
sprite.play_animation("walk")
sprite.set_scale(3.0)
game.add_sprite(sprite)
game.run()
