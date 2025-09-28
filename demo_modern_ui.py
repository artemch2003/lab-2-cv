"""
Демонстрация современного интерфейса приложения.
"""

import tkinter as tk
import logging
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.modern_main_window import ModernMainWindow
from di.config import create_container
from utils.logger import setup_logger

def main():
    """Главная функция демонстрации."""
    # Настройка логирования
    logger = setup_logger("demo_modern_ui")
    
    try:
        print("🚀 Запуск современного интерфейса Photo Editor Pro...")
        print("✨ Особенности нового интерфейса:")
        print("   • Современный дизайн в стиле фоторедактора")
        print("   • Удобное сравнение до/после")
        print("   • Анимации и визуальные эффекты")
        print("   • Темная тема с акцентными цветами")
        print("   • Улучшенная навигация и UX")
        print("   • Следование принципам SOLID")
        print()
        
        # Создание контейнера зависимостей
        container = create_container()
        
        # Создание главного окна
        root = tk.Tk()
        
        # Настройка стилей
        root.configure(bg="#2b2b2b")
        
        # Создание современного главного окна
        app = ModernMainWindow(root, container)
        
        logger.info("Современный интерфейс запущен успешно")
        print("✅ Современный интерфейс запущен!")
        print("📝 Инструкции по использованию:")
        print("   1. Нажмите '📁 Загрузить' для выбора изображения")
        print("   2. Выберите тип преобразования в панели справа")
        print("   3. Настройте параметры преобразования")
        print("   4. Нажмите '✨ Применить преобразование'")
        print("   5. Используйте режимы отображения для сравнения")
        print("   6. Сохраните результат с помощью '💾 Сохранить'")
        print()
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Ошибка при запуске современного интерфейса: {e}")
        print(f"❌ Ошибка при запуске современного интерфейса: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
