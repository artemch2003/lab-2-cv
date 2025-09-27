#!/usr/bin/env python3
"""
Главный модуль приложения для обработки изображений.
Содержит логарифмическое преобразование изображений.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from image_processing.image_processor import ImageProcessor
from utils.logger import setup_logger

def main():
    """Главная функция приложения."""
    # Настройка логирования
    logger = setup_logger()
    logger.info("Запуск приложения обработки изображений")
    
    try:
        # Создание главного окна
        root = tk.Tk()
        app = MainWindow(root)
        
        # Запуск приложения
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Ошибка при запуске приложения: {e}")
        messagebox.showerror("Ошибка", f"Произошла ошибка при запуске приложения: {e}")

if __name__ == "__main__":
    main()
