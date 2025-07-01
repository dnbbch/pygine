"""
Простая игра с взрывом.
Нажми на прямоугольник или жди 5 секунд, чтобы увидеть взрыв!
"""

import pygame
import sys
import os

# Добавляем путь к модулю pygine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pygine as pg

# Инициализация игры
game = pg.Game(800, 600, "Игра с взрывом")

# Состояние игры
game_state = "menu"  # menu, playing, exploded
timer = 5.0

# Создание прямоугольника-цели
target_rect = pygame.Rect(350, 250, 100, 100)
target_color = (245, 222, 179)  # Бежевый цвет

# Анимация взрыва
explosion_sprite = None

# Текстовые элементы
menu_title = pg.Text(400, 200, "ИГРА С ВЗРЫВОМ", size=48, color=(255, 255, 0))
menu_title.rect.centerx = 400

menu_instruction = pg.Text(400, 300, "Нажми ПРОБЕЛ для начала", size=24, color=(255, 255, 255))
menu_instruction.rect.centerx = 400

timer_text = pg.Text(400, 50, "", size=32, color=(255, 255, 255))
timer_text.rect.centerx = 400

game_over_text = pg.Text(400, 100, "БУМ! Нажми R для повтора", size=36, color=(255, 100, 100))
game_over_text.rect.centerx = 400


def update():
    global game_state, timer, explosion_sprite, target_color
    
    # Обновление эффектов
    from pygine.effects import update_effects
    update_effects(game.get_delta_time())
    
    # Обновление анимации взрыва
    if explosion_sprite:
        explosion_sprite.update(game.get_delta_time())
    
    if game_state == "menu":
        # Запуск игры
        if pg.key_pressed(pygame.K_SPACE):
            game_state = "playing"
            timer = 5.0
            target_color = (245, 222, 179)  # Возвращаем бежевый цвет
            explosion_sprite = None
            
    elif game_state == "playing":
        # Обновление таймера
        timer -= game.get_delta_time()
        
        # Проверка клика по прямоугольнику
        mouse_pos = pg.get_mouse_pos()
        mouse_clicked = pg.get_mouse_pressed()[0]
        
        if mouse_clicked and target_rect.collidepoint(mouse_pos):
            explode()
            
        # Взрыв по таймеру
        if timer <= 0:
            explode()
            
    elif game_state == "exploded":
        # Перезапуск игры
        if pg.key_pressed(pygame.K_r):
            game_state = "menu"
    
    # Выход из игры
    if pg.key_pressed(pygame.K_ESCAPE):
        pygame.quit()
        exit()


def explode():
    global game_state, explosion_sprite, target_color
    
    # Создание анимации взрыва
    explosion_sprite = pg.AnimatedSprite("explosion_sprites.png", (130, 130), (400, 300))
    explosion_sprite.add_animation("explode", list(range(25)), fps=15, loop=False)
    explosion_sprite.play_animation("explode")
    
    # Эффекты
    pg.start_screen_shake(8, 1.0)  # Сильная тряска на 1 секунду
    pg.create_explosion(400, 300, 30)  # Частицы взрыва
    
    # Меняем цвет прямоугольника на чёрный
    target_color = (0, 0, 0)
    
    game_state = "exploded"


def draw():
    from pygine.effects import draw_effects
    
    if game_state == "menu":
        # Отрисовка меню
        menu_title.draw(game.screen)
        menu_instruction.draw(game.screen)
        
    elif game_state == "playing":
        # Отрисовка таймера
        timer_text.text = f"Таймер: {timer:.1f}"
        timer_text.draw(game.screen)
        
        # Отрисовка прямоугольника
        pygame.draw.rect(game.screen, target_color, target_rect)
        pygame.draw.rect(game.screen, (255, 255, 255), target_rect, 3)  # Белая рамка
        
    elif game_state == "exploded":
        # Отрисовка взорванного прямоугольника
        pygame.draw.rect(game.screen, target_color, target_rect)
        pygame.draw.rect(game.screen, (100, 100, 100), target_rect, 3)  # Серая рамка
        
        # Анимация взрыва
        if explosion_sprite:
            game.screen.blit(explosion_sprite.image, explosion_sprite.rect)
            
            # Добавляем дым в конце анимации
            if explosion_sprite.current_frame >= 20:
                pg.create_smoke(400, 300, 5)
        
        # Текст окончания игры
        game_over_text.draw(game.screen)
    
    # Отрисовка эффектов (частицы и дым)
    draw_effects(game.screen)


# Запуск игры
game.run(update, draw) 