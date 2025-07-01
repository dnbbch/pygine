# pygine

**Упрощённая библиотека разработки игр на основе pygame**

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://python.org)
[![pygame Version](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://pygame.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Описание

**pygine** — это высокоуровневая библиотека для разработки 2D игр, построенная поверх pygame. Библиотека предоставляет упрощённый API для быстрого создания игр, абстрагируя сложности pygame и предлагая готовые решения для типичных игровых задач.

### Ключевые особенности

- **Упрощённый игровой цикл** с автоматическим управлением кадрами и событиями
- **Продвинутая система спрайтов** с поддержкой анимации из спрайтшитов
- **Гибкая система коллизий** с поддержкой прямоугольных и круглых хитбоксов
- **Комплексная система эффектов** включая частицы и тряску экрана
- **Готовые UI компоненты** с поддержкой скруглённых углов
- **Система управления сценами** для организации игровых состояний
- **Встроенная камера** с возможностями следования и ограничений
- **Базовая физическая система** для симуляции движения
- **Утилиты для работы со спрайтшитами** включая визуализацию и создание

## Требования

- Python 3.7+
- pygame 2.6.1

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Скопируйте папку `pygine` в корень вашего проекта.

3. Импортируйте библиотеку:
```python
import pygine as pg
```

## Структура проекта

При использовании библиотеки рекомендуется следующая структура:

```
your_game/
├── pygine/              # Библиотека pygine
├── assets/              # Ресурсы (изображения, звуки)
├── your_game.py         # Основной файл игры
└── requirements.txt     # Зависимости
```

⚠️ **Важно**: Все примеры в папке `examples/` должны запускаться из корневой директории проекта, так как пути к модулям и ресурсам настроены относительно корня.

## Архитектура библиотеки

### Основные модули

| Модуль | Описание |
|--------|----------|
| `game.py` | Главный игровой класс с управлением циклом и окном |
| `sprite.py` | Расширенные спрайты с анимацией и коллизиями |
| `animation.py` | Система управления анимациями |
| `effects.py` | Частицы, тряска экрана и визуальные эффекты |
| `ui.py` | Компоненты пользовательского интерфейса |
| `camera.py` | Система камеры для больших игровых миров |
| `scene.py` | Управление игровыми сценами и состояниями |
| `physics.py` | Базовая физическая система |
| `utils.py` | Утилитарные функции и обработка ввода |
| `spritesheet_tools.py` | Инструменты для работы со спрайтшитами |

## Быстрый старт

### Минимальная игра

```python
import pygine as pg

# Создание игры
game = pg.Game(800, 600, "Моя игра")

# Создание спрайта
player = pg.AnimatedSprite("player.png", (32, 32))
player.set_position(400, 300)

# Добавление спрайта в систему автоматического управления
game.add_sprite(player)

# Запуск игры (спрайт будет автоматически обновляться и отрисовываться)
game.run()

# Альтернативный способ с пользовательскими функциями:
# def update():
#     player.update()
# 
# def draw():
#     game.screen.blit(player.image, player.rect)
# 
# game.run(update, draw)
```

### Игра с анимацией

```python
import pygame
import pygine as pg

game = pg.Game(800, 600, "Анимированная игра")

# Создание анимированного спрайта
player = pg.AnimatedSprite("spritesheet.png", (64, 64))
player.add_animation("idle", [0, 1, 2, 3], fps=8, loop=True)
player.add_animation("walk", [4, 5, 6, 7], fps=12, loop=True)
player.play_animation("idle")

def update():
    # Переключение анимаций в зависимости от ввода
    if pg.key_pressed(pygame.K_LEFT) or pg.key_pressed(pygame.K_RIGHT):
        player.play_animation("walk")
    else:
        player.play_animation("idle")
    
    player.update()

def draw():
    game.screen.blit(player.image, player.rect)

game.run(update, draw)
```

## API Reference

### Класс Game

Основной класс для управления игрой.

```python
game = pg.Game(
    width=800,                          # Ширина окна
    height=600,                         # Высота окна
    title="Заголовок",                  # Заголовок окна
    fps=60,                             # Целевой FPS
    background_color=(50, 50, 50),      # Цвет фона
    background_image="background.png"   # Фоновое изображение (опционально)
)
```

**Основные методы:**
- `run(update_func, draw_func)` — запустить игровой цикл
- `add_sprite(sprite)` — добавить спрайт для автоматического управления
- `set_background_image(path)` — установить фоновое изображение
- `set_background_color(color)` — установить цвет фона
- `quit()` — завершить игру

### Класс AnimatedSprite

Расширенный спрайт с поддержкой анимации.

```python
sprite = pg.AnimatedSprite(
    "spritesheet.png",    # Путь к спрайтшиту
    (64, 64),             # Размер кадра
    (100, 100)            # Начальная позиция (опционально)
)
```

**Анимация:**
- `add_animation(name, frames, fps, loop)` — добавить анимацию
- `play_animation(name, restart, mirror)` — воспроизвести анимацию
- `stop_animation()` — остановить анимацию
- `pause_animation()` / `resume_animation()` — пауза/возобновление

**Трансформации:**
- `set_position(x, y)` — установить позицию
- `set_rotation(angle)` — установить поворот в градусах
- `set_scale(scale)` — установить масштаб
- `set_flip(flip_x, flip_y)` — отразить по осям
- `mirror(enabled)` — зеркалирование

**Коллизии:**
- `collides_with(other_sprite)` — проверка коллизии
- `set_collision_rect(w, h, offset_x, offset_y)` — прямоугольный хитбокс
- `set_collision_circle(radius, offset_x, offset_y)` — круглый хитбокс

### Система эффектов

```python
# Частицы
pg.create_explosion(x, y, size=20)     # Эффект взрыва
pg.create_smoke(x, y, amount=10)       # Эффект дыма
pg.create_sparkles(x, y, amount=15)    # Искры

# Тряска экрана
pg.start_screen_shake(intensity=5, duration=0.5, frequency=30)
```

### UI компоненты

```python
# Кнопка
button = pg.Button(x, y, width, height, text="Нажми меня")
button.set_border_radius(10)  # Скруглённые углы

# Полоса здоровья
health_bar = pg.HealthBar(x, y, width, height, max_value=100)
health_bar.set_value(75)

# Панель
panel = pg.Panel(x, y, width, height, color=(100, 100, 100))
panel.set_border_radius(15)

# Поле ввода
text_input = pg.TextInput(x, y, width, height, placeholder="Введите текст")
text_input.set_border_radius(5)
```

### Управление сценами

```python
# Создание сцены
class MenuScene(pg.Scene):
    def __init__(self):
        super().__init__("menu")
    
    def update(self, dt):
        pass
    
    def draw(self, screen):
        pass

# Менеджер сцен
scene_manager = pg.SceneManager()
scene_manager.add_scene(MenuScene())
scene_manager.switch_to("menu")
```

### Система камеры

```python
camera = pg.Camera(screen_width, screen_height)
camera.follow(player_sprite)              # Следовать за спрайтом
camera.update(dt)                         # Обновление камеры

# Получение смещения для отрисовки
camera_offset = camera.get_offset()
adjusted_x = sprite.rect.x + camera_offset[0]
adjusted_y = sprite.rect.y + camera_offset[1]
```

### Утилитарные функции

```python
# Ввод
pg.key_pressed(pygame.K_SPACE)          # Проверка нажатой клавиши
pg.key_just_pressed(pygame.K_ENTER)     # Проверка однократного нажатия
pg.key_just_released(pygame.K_ESCAPE)   # Проверка отпускания клавиши
pg.get_mouse_pos()                       # Позиция мыши
pg.get_mouse_pressed()                   # Состояние кнопок мыши

# Математика
pg.normalize_vector(vector)              # Нормализация вектора
pg.lerp(a, b, t)                        # Линейная интерполяция
pg.clamp(value, min_val, max_val)       # Ограничение значения

# Ожидание
pg.wait(seconds)                        # Ожидание времени
pg.wait_for_key()                       # Ожидание нажатия клавиши
pg.wait_for_click()                     # Ожидание клика мыши
pg.wait_for_animation(sprite)           # Ожидание завершения анимации

# Эффекты (для ручного управления)
# from pygine.effects import update_effects, draw_effects
# update_effects(dt)                     # Обновление частиц и тряски
# draw_effects(screen)                   # Отрисовка эффектов
```

## Примеры использования

В папке `examples/` находятся готовые примеры, демонстрирующие различные возможности библиотеки:

### Базовые примеры
- `example_basic_sprite.py` — основы работы со спрайтами
- `example_animations.py` — система анимации
- `example_scaling.py` — масштабирование спрайтов
- `example_rotation.py` — поворот спрайтов
- `example_mirroring.py` — отражение спрайтов

### Интерактивность
- `example_keyboard_input.py` — обработка клавиатуры
- `example_mouse_tracking.py` — отслеживание мыши
- `example_collision_detection.py` — детекция коллизий

### Эффекты и UI
- `example_particle_effects.py` — система частиц
- `example_screen_shake.py` — тряска экрана
- `example_user_interface.py` — элементы интерфейса
- `example_rounded_ui.py` — скруглённые элементы UI
- `example_text_input.py` — поля ввода текста

### Продвинутые возможности
- `example_camera_system.py` — система камеры
- `example_scene_management.py` — управление сценами
- `example_physics_simulation.py` — физическая симуляция
- `example_background_image.py` — фоновые изображения

### Комплексные примеры
- `example_platformer_game.py` — простой платформер
- `example_explosion_game.py` — игра со взрывами и эффектами
- `example_simple_game.py` — минимальная игра

### Утилиты
- `example_spritesheet_utilities.py` — работа со спрайтшитами
- `example_all_animations.py` — демонстрация всех анимаций

## Лицензия

Проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## Поддержка

При возникновении вопросов или проблем:

1. Проверьте примеры в папке `examples/`
2. Изучите документацию в комментариях к коду
3. Создайте issue в репозитории проекта
