import pygame
from pygine.spritesheet_tools import *

# Инициализация pygame
pygame.init()
pygame.display.set_mode((1, 1), pygame.HIDDEN)

# 1. Создать PNG файл с сеткой и номерами кадров - чтобы видеть какой кадр какой номер имеет
visualize_spritesheet("platformer_sprites_custom.png", (64, 64))

# 2. Создать новый спрайт-лист из выбранных кадров - например для анимации ходьбы
# create_spritesheet_from_frames("platformer_sprites.png", (64, 64), [10, 29, 45, 18])
