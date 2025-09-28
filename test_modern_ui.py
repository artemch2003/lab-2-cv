"""
Тестовый файл для проверки современного интерфейса.
"""

import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Тестирует импорты."""
    try:
        print("🔍 Тестирование импортов...")
        
        # Базовые импорты
        import tkinter as tk
        print("✅ tkinter импортирован")
        
        from tkinter import ttk
        print("✅ ttk импортирован")
        
        # Наши модули
        from utils.logger import setup_logger
        print("✅ logger импортирован")
        
        from di.config import create_container
        print("✅ DI контейнер импортирован")
        
        # GUI компоненты
        from gui.components.animations import AnimationManager
        print("✅ AnimationManager импортирован")
        
        from gui.styles.modern_styles import ModernStyles
        print("✅ ModernStyles импортирован")
        
        from gui.components.modern_image_display import ModernImageDisplay
        print("✅ ModernImageDisplay импортирован")
        
        from gui.components.modern_transform_settings import ModernTransformSettings
        print("✅ ModernTransformSettings импортирован")
        
        from gui.components.modern_info_panel import ModernInfoPanel
        print("✅ ModernInfoPanel импортирован")
        
        from gui.modern_main_window import ModernMainWindow
        print("✅ ModernMainWindow импортирован")
        
        print("\n🎉 Все импорты успешны!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_functionality():
    """Тестирует базовую функциональность."""
    try:
        print("\n🔧 Тестирование базовой функциональности...")
        
        # Создаем корневое окно
        root = tk.Tk()
        root.withdraw()  # Скрываем окно
        
        # Тестируем стили
        styles = ModernStyles()
        print("✅ Стили созданы")
        
        # Тестируем анимации
        animation_manager = AnimationManager()
        print("✅ Менеджер анимаций создан")
        
        # Тестируем DI контейнер
        container = create_container()
        print("✅ DI контейнер создан")
        
        root.destroy()
        print("✅ Базовые тесты пройдены")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в базовых тестах: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Главная функция тестирования."""
    print("🚀 Тестирование современного интерфейса")
    print("=" * 50)
    
    # Тест импортов
    imports_ok = test_imports()
    
    if imports_ok:
        # Тест базовой функциональности
        functionality_ok = test_basic_functionality()
        
        if functionality_ok:
            print("\n🎉 Все тесты пройдены успешно!")
            print("✨ Современный интерфейс готов к использованию!")
        else:
            print("\n❌ Ошибки в базовой функциональности")
    else:
        print("\n❌ Ошибки в импортах")

if __name__ == "__main__":
    main()
