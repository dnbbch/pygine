import pygine as pg

# Простой тест коллизий
game = pg.Game(800, 600, "Тест коллизий")

# Игрок (управляется мышкой)
player = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (100, 100))
player.set_scale(2.0)

# Несколько простых целей
target1 = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (300, 200))
target1.set_scale(1.5)

target2 = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (500, 200))
target2.set_collision_circle(30)  # круглая коллизия

target3 = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 400))
target3.set_rotation(45)  # повернутый спрайт

def update():
    # Движение игрока за мышкой
    mouse_x, mouse_y = pg.get_mouse_pos()
    player.x = mouse_x
    player.y = mouse_y

def draw():
    # Рисуем хитбоксы
    player.debug_draw(game.screen)
    target1.debug_draw(game.screen)
    target2.debug_draw(game.screen)
    target3.debug_draw(game.screen)
    
    # Проверяем коллизии
    collision_text = "Нет коллизий"
    collision_color = (0, 255, 0)  # зеленый
    
    if player.collides_with(target1):
        collision_text = "КОЛЛИЗИЯ: Цель 1"
        collision_color = (255, 0, 0)  # красный
    elif player.collides_with(target2):
        collision_text = "КОЛЛИЗИЯ: Цель 2"
        collision_color = (255, 0, 0)  # красный
    elif player.collides_with(target3):
        collision_text = "КОЛЛИЗИЯ: Цель 3"
        collision_color = (255, 0, 0)  # красный
    
    # Показываем результат
    pg.Text(10, 10, collision_text, size=24, color=collision_color).draw(game.screen)
    
    # Инструкции
    pg.Text(10, 50, "Двигайте мышкой для проверки коллизий", 
            size=16, color=(255, 255, 255)).draw(game.screen)

# Добавляем спрайты в игру
game.add_sprite(player)
game.add_sprite(target1)
game.add_sprite(target2)
game.add_sprite(target3)

game.run(update, draw)
