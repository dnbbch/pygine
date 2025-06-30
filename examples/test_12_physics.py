import pygame
import pygine as pg

# Создаем игру
game = pg.Game(800, 600, "Простая физика")

# Создаем физику
physics = pg.PhysicsBody(gravity=500.0)
physics.set_bounce_factor(0.9)  # Насколько хорошо мяч отскакивает

# Мяч
ball_x = 400  # Начальная позиция X
ball_y = 100  # Начальная позиция Y
ball_radius = 30  # Размер мяча
ball_color = (255, 0, 0)  # Красный цвет

# Земля
ground_level = 500  # Уровень земли

# Функция обновления (вызывается каждый кадр)
def update():
    global ball_x, ball_y
    
    # Обновляем физику
    dx, dy = physics.update(1/60)
    ball_x += dx
    ball_y += dy
    
    # Проверяем столкновение с землей
    if ball_y + ball_radius > ground_level:
        ball_y = ground_level - ball_radius
        physics.bounce((0, -1))  # Отскок от земли
    
    # Прыжок при нажатии пробела
    if pg.key_pressed(pygame.K_SPACE) and ball_y + ball_radius >= ground_level - 5:
        physics.velocity[1] = -400  # Отрицательная скорость = движение вверх

# Функция рисования (вызывается каждый кадр)
def draw():
    # Рисуем мяч
    pygame.draw.circle(game.screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)
    
    # Рисуем землю
    pygame.draw.rect(game.screen, (101, 67, 33), (0, ground_level, 800, 100))
    
    # Показываем инструкцию
    font = pygame.font.Font(None, 36)
    text = font.render("ПРОБЕЛ: прыжок", True, (255, 255, 255))
    game.screen.blit(text, (10, 10))

# Запускаем игру
game.run(update, draw)
