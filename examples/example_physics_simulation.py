"""
Пример простой физической системы с гравитацией и отскоком.
Демонстрирует движение мяча под действием гравитации и прыжки.
"""

import pygame
import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Простая физика")

# Создание физического тела с гравитацией
physics = pg.PhysicsBody(gravity=500.0)
physics.set_bounce_factor(0.9)  # Коэффициент отскока мяча

# Параметры мяча
ball_x = 400  # Начальная позиция по X
ball_y = 100  # Начальная позиция по Y
ball_radius = 30  # Радиус мяча
ball_color = (255, 50, 50)  # Красный цвет

# Параметры земли
ground_level = 500  # Уровень поверхности земли
ground_color = (101, 67, 33)  # Коричневый цвет земли

# Функция обновления (вызывается каждый кадр)
def update():
    global ball_x, ball_y
    
    # Обновление физики (60 FPS)
    dx, dy = physics.update(1/60)
    ball_x += dx
    ball_y += dy
    
    # Проверка столкновения с землёй
    if ball_y + ball_radius > ground_level:
        ball_y = ground_level - ball_radius
        physics.bounce((0, -1))  # Вектор нормали поверхности
    
    # Прыжок при нажатии пробела (только когда мяч на земле)
    if pg.key_pressed(pygame.K_SPACE) and ball_y + ball_radius >= ground_level - 5:
        physics.velocity[1] = -400  # Импульс прыжка вверх

# Функция рисования (вызывается каждый кадр)
def draw():
    # Очистка экрана
    game.screen.fill((135, 206, 235))  # Голубой фон неба
    
    # Отрисовка мяча
    pygame.draw.circle(game.screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)
    
    # Отрисовка земли
    pygame.draw.rect(game.screen, ground_color, (0, ground_level, 800, 100))
    
    # Отображение инструкций
    pg.Text(10, 10, "ПРОБЕЛ - прыжок", size=20, color=(255, 255, 255)).draw(game.screen)
    
    # Отображение информации о физике
    info_text = f"Скорость Y: {physics.velocity[1]:.1f}"
    pg.Text(10, 40, info_text, size=16, color=(255, 255, 255)).draw(game.screen)

# Запуск игры
game.run(update, draw)
