"""
Инструменты для работы со спрайтшитами.
Демонстрирует функции визуализации и создания новых спрайтшитов.
"""

import pygame
from pygine.spritesheet_tools import visualize_spritesheet, create_spritesheet_from_frames

pygame.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

# 1. Создание PNG файла с сеткой и номерами кадров
visualize_spritesheet("platformer_sprites.png", (64, 64))

# 2. Создание нового спрайтшита из выбранных кадров
create_spritesheet_from_frames("platformer_sprites.png", (64, 64), [4, 5, 6, 7, 8, 9, 10, 11])

pygame.quit()
