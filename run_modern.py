"""
Запуск приложения с современным интерфейсом.
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
    """Главная функция запуска приложения."""
    # Настройка логирования
    logger = setup_logger("modern_ui")
    
    try:
        # Создание контейнера зависимостей
        container = create_container()
        
        # Создание главного окна
        root = tk.Tk()
        
        # Настройка стилей
        root.configure(bg="#2b2b2b")
        
        # Создание современного главного окна
        app = ModernMainWindow(root, container)
        
        logger.info("Приложение запущено с современным интерфейсом")
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
        print(f"Ошибка при запуске приложения: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
