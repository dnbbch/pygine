"""
Тест 13: Сцены
Демонстрирует систему управления сценами
"""

import pygame
import pygine as pg
from pygine.scene import Scene, SceneManager

# Инициализация
pygame.init()
game = pg.Game(800, 600, "Тест 13: Сцены")

# Менеджер сцен
scene_manager = SceneManager()

# Сцена 1: Главное меню
class MenuScene(Scene):
    def __init__(self):
        super().__init__("menu")
        self.title_text = "ГЛАВНОЕ МЕНЮ"
        self.instruction_text = "Нажмите ПРОБЕЛ для перехода в игру"
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            scene_manager.switch_to("game")
    
    def draw(self, screen):
        # Очищаем экран
        screen.fill((100, 50, 100))
        
        # Рисуем текст
        font = pygame.font.Font(None, 48)
        title = font.render(self.title_text, True, (255, 255, 0))
        instruction = font.render(self.instruction_text, True, (255, 255, 255))
        
        # Центрируем текст
        title_rect = title.get_rect(center=(400, 200))
        instruction_rect = instruction.get_rect(center=(400, 300))
        
        screen.blit(title, title_rect)
        screen.blit(instruction, instruction_rect)

# Сцена 2: Игровая сцена
class GameScene(Scene):
    def __init__(self):
        super().__init__("game")
        self.player = pg.AnimatedSprite("platformer_sprites_custom.png", (32, 32), (400, 300))
        self.player.add_animation("idle", [0], fps=1)
        self.player.play_animation("idle")
        self.instruction_text = "Нажмите ESC для возврата в меню"
    
    def update(self, dt):
        # Движение игрока за мышью
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.player.x = mouse_x
        self.player.y = mouse_y
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            scene_manager.switch_to("menu")
    
    def draw(self, screen):
        # Очищаем экран
        screen.fill((50, 100, 50))
        
        # Рисуем игрока
        screen.blit(self.player.image, self.player.rect)
        
        # Рисуем инструкцию
        font = pygame.font.Font(None, 24)
        instruction = font.render(self.instruction_text, True, (255, 255, 255))
        screen.blit(instruction, (10, 10))

# Создаем сцены
menu_scene = MenuScene()
game_scene = GameScene()

# Добавляем сцены в менеджер
scene_manager.add_scene(menu_scene)
scene_manager.add_scene(game_scene)

# Начинаем с главного меню
scene_manager.switch_to("menu")

def update():
    """Обновление игры"""
    dt = game.get_delta_time()
    scene_manager.update(dt)

def draw():
    """Отрисовка игры"""
    scene_manager.draw(game.screen)

# Запуск игры
print("ЗАПУСК: Начинаем тест сцен")
game.run(update, draw)
print("ЗАВЕРШЕНИЕ: Тест сцен завершен") 