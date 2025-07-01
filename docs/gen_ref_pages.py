"""
Генерация API документации из исходного кода
"""

from pathlib import Path
import mkdocs_gen_files

# Навигация для API
nav = mkdocs_gen_files.Nav()

# Модули для документирования
modules = {
    "game": "Основной игровой класс",
    "sprite": "Система спрайтов и анимации", 
    "animation": "Управление анимациями",
    "effects": "Частицы и визуальные эффекты",
    "ui": "Компоненты пользовательского интерфейса",
    "camera": "Система камеры",
    "scene": "Управление сценами",
    "physics": "Базовая физическая система",
    "utils": "Утилитарные функции",
    "spritesheet_tools": "Инструменты для работы со спрайтшитами"
}

# Генерируем страницы для каждого модуля
for module_name, description in modules.items():
    module_path = f"pygine.{module_name}"
    doc_path = f"api/{module_name}.md"
    
    with mkdocs_gen_files.open(doc_path, "w") as f:
        f.write(f"# {description}\n\n")
        f.write(f"::: {module_path}\n")
    
    nav[module_name] = doc_path

# Создаём индексную страницу API
with mkdocs_gen_files.open("api/index.md", "w") as f:
    f.write("""# API Reference

Полная документация всех классов, методов и функций библиотеки pygine.

## Структура API

### Основные классы
- **[Game](game.md)** — главный игровой класс
- **[AnimatedSprite](sprite.md)** — система спрайтов с анимацией  
- **[Animation](animation.md)** — управление анимациями

### Системы и компоненты
- **[Эффекты](effects.md)** — частицы, тряска экрана
- **[UI компоненты](ui.md)** — кнопки, панели, поля ввода
- **[Камера](camera.md)** — система камеры для больших миров
- **[Сцены](scene.md)** — управление игровыми состояниями
- **[Физика](physics.md)** — базовая физическая система

### Утилиты
- **[Общие функции](utils.md)** — ввод, математика, ожидание
- **[Инструменты спрайтшитов](spritesheet_tools.md)** — работа со спрайтшитами

## Соглашения по документации

Все функции и классы документированы с использованием docstring'ов в стиле Google.
Примеры кода показывают типичное использование каждого компонента.
""")

# Записываем навигацию
with mkdocs_gen_files.open("api/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
