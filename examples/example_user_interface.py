"""
Пример создания пользовательского интерфейса.
Демонстрирует работу с кнопками, полосами здоровья и прогресса, текстом и панелями.
"""

import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Интерфейс пользователя")

# Создание элементов интерфейса
panel = pg.Panel(40, 40, 720, 400, color=(30, 30, 30), border_color=(200, 200, 200))
health_bar = pg.HealthBar(60, 80, 680, 30)
progress_bar = pg.ProgressBar(60, 130, 680, 30)
info_text = pg.Text(60, 180, "", size=20, color=(255, 255, 0))

# Функции для кнопок
def damage_player():
    current_hp = health_bar.current_value - 15
    health_bar.set_value(current_hp)

def heal_player():
    current_hp = health_bar.current_value + 15
    health_bar.set_value(current_hp)

def add_progress():
    current_progress = progress_bar.current_value + 20
    progress_bar.set_value(current_progress)

def reset_values():
    health_bar.set_value(100)
    progress_bar.set_value(0)

# Создание кнопок
buttons = [
    pg.Button(60, 480, 120, 35, "Урон", damage_player, 
              color=(150, 50, 50), hover_color=(200, 80, 80)),
    pg.Button(200, 480, 120, 35, "Лечение", heal_player,
              color=(50, 150, 50), hover_color=(80, 200, 80)),
    pg.Button(340, 480, 120, 35, "Прогресс", add_progress,
              color=(50, 50, 150), hover_color=(80, 80, 200)),
    pg.Button(480, 480, 120, 35, "Сброс", reset_values,
              color=(100, 100, 100), hover_color=(150, 150, 150))
]

# Список всех элементов интерфейса
ui_elements = [panel, health_bar, progress_bar, info_text] + buttons


def handle_events(event):
    # Обработка кликов по кнопкам
    for button in buttons:
        if button.handle_event(event):
            break


def update():
    # Обновление элементов интерфейса
    dt = game.get_delta_time()
    for element in ui_elements:
        element.update(dt)
    
    # Обновление информационного текста
    health_percent = (health_bar.current_value / health_bar.max_value) * 100
    info_text.set_text(f"Здоровье: {health_bar.current_value:.0f}/100 ({health_percent:.0f}%)  "
                      f"Прогресс: {progress_bar.current_value:.0f}%")


def draw():
    # Отрисовка всех элементов интерфейса
    for element in ui_elements:
        element.draw(game.screen)
    
    # Инструкции
    pg.Text(60, 220, "Нажимайте кнопки для взаимодействия с интерфейсом", 
            size=16, color=(200, 200, 200)).draw(game.screen)


# Подключение обработчика событий
game.add_event_callback(handle_events)

# Запуск игры
game.run(update, draw)
