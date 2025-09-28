#!/usr/bin/env python
"""
Демонстрационное приложение с фильтрами сглаживания.
Запускает современный интерфейс с отдельной вкладкой для сглаживания.
"""

import tkinter as tk
import logging
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.modern_main_window_with_tabs import ModernMainWindowWithTabs
from di.config import create_container
from utils.logger import setup_logger

def main():
    """Главная функция приложения."""
    # Настройка логирования
    setup_logger("smoothing_app")
    logger = logging.getLogger(__name__)
    
    try:
        # Создаем контейнер зависимостей
        container = create_container()
        
        # Создаем главное окно
        root = tk.Tk()
        
        # Создаем приложение с вкладками
        app = ModernMainWindowWithTabs(root, container)
        
        logger.info("Приложение с фильтрами сглаживания запущено")
        
        # Запускаем главный цикл
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
