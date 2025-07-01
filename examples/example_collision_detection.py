"""
Пример системы коллизий между спрайтами.
Демонстрирует различные типы коллизий: прямоугольные, круглые и повернутые.
"""

import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Система коллизий")

# Создание игрока (управляется мышью)
player = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (100, 100))
player.set_scale(2.0)

# Создание целей с разными типами коллизий
target1 = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (300, 200))
target1.set_scale(1.5)

target2 = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (500, 200))
target2.set_collision_circle(30)  # Круглая область коллизии

target3 = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 400))
target3.set_rotation(45)  # Повернутый спрайт


def update():
    # Перемещение игрока за курсором мыши
    mouse_x, mouse_y = pg.get_mouse_pos()
    player.x = mouse_x
    player.y = mouse_y


def draw():
    # Отображение всех хитбоксов для наглядности
    player.debug_draw(game.screen)
    target1.debug_draw(game.screen)
    target2.debug_draw(game.screen)
    target3.debug_draw(game.screen)
    
    # Проверка коллизий и отображение результата
    collision_detected = False
    collision_text = "Нет коллизий"
    
    if player.collides_with(target1):
        collision_text = "КОЛЛИЗИЯ: Цель 1 (прямоугольная)"
        collision_detected = True
    elif player.collides_with(target2):
        collision_text = "КОЛЛИЗИЯ: Цель 2 (круглая)"
        collision_detected = True
    elif player.collides_with(target3):
        collision_text = "КОЛЛИЗИЯ: Цель 3 (повернутая)"
        collision_detected = True
    
    # Цвет текста зависит от наличия коллизии
    color = (255, 0, 0) if collision_detected else (0, 255, 0)
    pg.Text(10, 10, collision_text, size=20, color=color).draw(game.screen)
    
    # Инструкции и описание целей
    instructions = [
        "Двигайте мышью для проверки коллизий",
        "Цель 1: Обычная прямоугольная коллизия",
        "Цель 2: Круглая коллизия",
        "Цель 3: Повернутая коллизия"
    ]
    
    for i, text in enumerate(instructions):
        pg.Text(10, 50 + i * 20, text, size=14, color=(255, 255, 255)).draw(game.screen)


# Добавление всех спрайтов в игру
sprites = [player, target1, target2, target3]
for sprite in sprites:
    game.add_sprite(sprite)

# Запуск игры
game.run(update, draw)
