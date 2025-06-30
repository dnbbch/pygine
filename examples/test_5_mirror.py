import pygame
import pygine as pg

# Создаем игру и спрайт
game = pg.Game(800, 600, "Тест зеркалирования")
sprite = pg.AnimatedSprite("./platformer_sprites.png", (64, 64), (400, 300))
sprite.set_scale(2.0)

# Переменные для отслеживания состояния
last_left_state = False
last_right_state = False


def update():
    global last_left_state, last_right_state

    # Проверяем нажатие клавиш
    left_pressed = pg.key_pressed(pygame.K_LEFT)
    right_pressed = pg.key_pressed(pygame.K_RIGHT)

    # Обрабатываем только при изменении состояния (чтобы избежать спама)
    if left_pressed and not last_left_state:
        sprite.mirror(True)  # Зеркалим влево
        print("Зеркалирование ВЛЕВО")

    if right_pressed and not last_right_state:
        sprite.mirror(False)  # Обычное направление
        print("Зеркалирование ВПРАВО")

    # Обновляем состояние
    last_left_state = left_pressed
    last_right_state = right_pressed


def draw():
    # Показываем хитбокс для наглядности
    sprite.debug_draw(game.screen)

    # Инструкции
    pg.Text(
        10, 10, "Стрелка ВЛЕВО - зеркалировать", size=16, color=(255, 255, 255)
    ).draw(game.screen)
    pg.Text(
        10, 35, "Стрелка ВПРАВО - обычное направление", size=16, color=(255, 255, 255)
    ).draw(game.screen)

    # Статус
    status = "Зеркалирован" if sprite._mirrored else "Обычное"
    pg.Text(10, 60, f"Статус: {status}", size=18, color=(255, 255, 0)).draw(game.screen)

    # Отладочная информация
    pg.Text(
        10,
        90,
        "Смотрите в консоль для отладочной информации",
        size=14,
        color=(255, 200, 200),
    ).draw(game.screen)


game.add_sprite(sprite)
game.run(update, draw)
