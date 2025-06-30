import pygine as pg

# Окно
game = pg.Game(800, 600, "UI Demo")

# Элементы UI
health = pg.HealthBar(50, 60, 700, 25)
progress = pg.ProgressBar(50, 110, 700, 25)
info = pg.Text(50, 160, "", size=24, color=(255, 255, 0))
panel = pg.Panel(40, 40, 720, 400, color=(30, 30, 30), border_color=(200, 200, 200))


def damage():
    health.set_value(health.current_value - 10)


def heal():
    health.set_value(health.current_value + 10)


def add_progress():
    progress.set_value(progress.current_value + 10)


def reset():
    health.set_value(100)
    progress.set_value(0)


# Кнопки с базовой кастомизацией
btn_damage = pg.Button(
    50, 500, 150, 40, "Урон -10", damage, color=(150, 50, 50), hover_color=(200, 80, 80), font_size=20
)

btn_heal = pg.Button(
    220,
    500,
    150,
    40,
    "Лечить +10",
    heal,
    color=(50, 150, 50),
    hover_color=(80, 200, 80), font_size=20
)

btn_prog = pg.Button(
    390,
    500,
    150,
    40,
    "Прогресс +10",
    add_progress,
    color=(50, 50, 150),
    hover_color=(80, 80, 200), font_size=20
)

btn_reset = pg.Button(560, 500, 150, 40, "Сброс", reset, font_size=20)

ui = [panel, health, progress, info, btn_damage, btn_heal, btn_prog, btn_reset]


# Обработка кликов мышкой
def handle_mouse_clicks(event):
    # Проверяем каждую кнопку
    for button in [btn_damage, btn_heal, btn_prog, btn_reset]:
        if button.handle_event(event) == True:
            return  # Если кнопка обработала клик, останавливаемся

# Подключаем обработчик к игре
game.add_event_callback(handle_mouse_clicks)


# Игровой цикл
def update():
    dt = game.get_delta_time()
    for element in ui:
        element.update(dt)

    info.set_text(
        f"Здоровье: {health.current_value:.0f}/{health.max_value}   "
        f"Прогресс: {progress.current_value:.0f}%"
    )


def draw():
    for element in ui:
        element.draw(game.screen)


game.run(update, draw)
