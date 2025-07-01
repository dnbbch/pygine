# Быстрый старт

Добро пожаловать в pygine! Эта страница поможет вам быстро начать создавать игры.

## 🛠️ Установка

1. **Убедитесь, что у вас установлен Python 3.7+**
   
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Скопируйте папку `pygine` в корень вашего проекта**

## 🎮 Ваша первая игра

### Минимальный пример

```python
import pygine as pg

# Создание игры
game = pg.Game(800, 600, "Моя первая игра")

# Создание спрайта
player = pg.AnimatedSprite("player.png", (32, 32))
player.set_position(400, 300)

# Добавление спрайта в систему автоматического управления
game.add_sprite(player)

# Запуск игры
game.run()
```

### С анимацией

```python
import pygame
import pygine as pg

game = pg.Game(800, 600, "Игра с анимацией")

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

## 📁 Структура проекта

```
your_game/
├── pygine/              # Библиотека pygine
├── assets/              # Ресурсы (изображения, звуки)
├── your_game.py         # Основной файл игры
└── requirements.txt     # Зависимости
```

## 🎯 Следующие шаги

1. **Изучите [примеры](examples/index.md)** — готовые примеры различной сложности
2. **Посмотрите [API Reference](api/index.md)** — полная документация
3. **Экспериментируйте!** — создавайте свои игры

## ⚠️ Важные замечания

- Все примеры должны запускаться из корневой директории проекта
- Пути к ресурсам указываются относительно корня проекта
- Библиотека автоматически управляет игровым циклом и обновлением спрайтов

## 🔗 Полезные ссылки

- [Документация pygame](https://www.pygame.org/docs/)
- [Примеры кода](examples/index.md)
- [API Reference](api/index.md)
