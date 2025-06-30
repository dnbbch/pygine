import pygine as pg

# Создаем игру и спрайт
game = pg.Game(800, 600, "Тест масштабирования")
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(3.0)  # Увеличиваем в 3 раза
game.add_sprite(sprite)
game.run()
