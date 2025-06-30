"""
Тест 10: Эффекты (частицы)
Демонстрирует систему частиц и визуальных эффектов
"""

import pygame
import pygine as pg
from pygine.effects import create_explosion, create_smoke, create_sparkles, update_effects, draw_effects
import traceback
import sys

print("=== НАЧАЛО ТЕСТА 10 - ЭФФЕКТЫ ===")

try:
    print("1. Импорты успешны")
    
    # Тест эффектов
    print("2. Создаем игру...")
    game = pg.Game(800, 600, "Тест 10: Эффекты")
    print("3. Игра создана успешно")
    
    # Игрок (управляется мышкой)
    print("4. Создаем игрока...")
    player = pg.AnimatedSprite("platformer_sprites_custom.png", (32, 32), (400, 300))
    player.add_animation("idle", [0], fps=1)
    player.play_animation("idle")
    print("5. Игрок создан")
    player.set_scale(2.0)
    print("6. Масштаб игрока установлен")
    
    print("7. Определяем функции update и draw...")
    
    # Переменные для эффектов
    effect_timer = 0
    effect_interval = 0.5  # секунды между эффектами
    
    def update():
        """Обновление игры"""
        print("UPDATE: Начало функции update")
        
        # Получаем позицию мыши
        print("UPDATE: Получаем позицию мыши...")
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print(f"UPDATE: Позиция мыши: {mouse_x}, {mouse_y}")
        
        # Устанавливаем позицию игрока
        print("UPDATE: Устанавливаем позицию игрока...")
        player.set_position(mouse_x, mouse_y)
        print("UPDATE: Позиция игрока установлена")
        
        # Обновляем эффекты
        print("UPDATE: Обновляем эффекты...")
        try:
            update_effects(game.get_delta_time())
            print("UPDATE: Эффекты обновлены успешно")
        except Exception as e:
            print(f"ОШИБКА В UPDATE: {e}")
        
        # Создаем эффекты по таймеру
        global effect_timer
        effect_timer += game.get_delta_time()
        
        if effect_timer >= effect_interval:
            effect_timer = 0
            
            # Создаем разные эффекты в разных местах
            create_explosion(mouse_x + 50, mouse_y, 15)
            create_smoke(mouse_x - 50, mouse_y, 8)
            create_sparkles(mouse_x, mouse_y - 50, 12)
            print("UPDATE: Созданы новые эффекты")
    
    def draw():
        """Отрисовка игры"""
        print("DRAW: Начало функции draw")
        
        # Очищаем экран
        game.screen.fill((50, 50, 100))
        
        # Рисуем игрока
        print("DRAW: Рисуем игрока...")
        try:
            game.screen.blit(player.image, player.rect)
            print("DRAW: Игрок нарисован успешно")
        except Exception as e:
            print(f"ОШИБКА В DRAW: {e}")
        
        # Рисуем эффекты
        print("DRAW: Рисуем эффекты...")
        try:
            draw_effects(game.screen)
            print("DRAW: Эффекты нарисованы успешно")
        except Exception as e:
            print(f"ОШИБКА В DRAW ЭФФЕКТОВ: {e}")
        
        # Рисуем текст
        font = pygame.font.Font(None, 36)
        text = font.render("Двигайте мышью для создания эффектов", True, (255, 255, 255))
        game.screen.blit(text, (50, 50))
        
        print("DRAW: Функция draw завершена")
    
    print("8. Функции определены")
    
    # Обработка кликов мыши
    print("9. Определяем обработчик кликов...")
    
    def handle_mouse_clicks(event):
        print(f"MOUSE EVENT: Тип события: {event.type}, кнопка: {getattr(event, 'button', 'N/A')}")
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSE EVENT: Обрабатываем клик мыши")
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(f"MOUSE EVENT: Позиция клика: {mouse_x}, {mouse_y}")
                
                if event.button == 1:  # левая кнопка
                    print("MOUSE EVENT: Создаем взрыв")
                    # Создаем взрыв
                    create_explosion(mouse_x, mouse_y, 25)
                    print("MOUSE EVENT: Взрыв создан")
                    
                elif event.button == 3:  # правая кнопка
                    print("MOUSE EVENT: Создаем дым")
                    # Создаем дым
                    create_smoke(mouse_x, mouse_y, 15)
                    print("MOUSE EVENT: Дым создан")
                    
                elif event.button == 2:  # средняя кнопка
                    print("MOUSE EVENT: Создаем искры")
                    # Создаем искры
                    create_sparkles(mouse_x, mouse_y, 25)
                    print("MOUSE EVENT: Искры созданы")
        except Exception as e:
            print(f"ОШИБКА В MOUSE EVENT: {e}")
            traceback.print_exc()
    
    print("10. Обработчик кликов определен")
    
    print("11. Добавляем обработчик событий...")
    game.add_event_callback(handle_mouse_clicks)
    print("12. Обработчик событий добавлен")
    
    print("13. Добавляем спрайт в игру...")
    game.add_sprite(player)
    print("14. Спрайт добавлен")
    
    print("15. Запускаем игру...")
    game.run(update, draw)
    print("16. Игра завершена")
    
except Exception as e:
    print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
    print("Полный стек ошибки:")
    traceback.print_exc()
    print("=== КОНЕЦ ТЕСТА 10 ===")
    sys.exit(1)

print("=== КОНЕЦ ТЕСТА 10 - УСПЕШНО ===") 