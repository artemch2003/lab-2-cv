"""
Упрощенный тест современного интерфейса.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_simple_modern_window():
    """Создает простое современное окно для тестирования."""
    root = tk.Tk()
    root.title("Photo Editor Pro - Тест")
    root.geometry("800x600")
    root.configure(bg="#2b2b2b")
    
    # Создаем стиль
    style = ttk.Style()
    style.theme_use('clam')
    
    # Настраиваем цвета
    style.configure('Modern.TFrame', background="#2b2b2b")
    style.configure('Modern.TLabel', background="#3c3c3c", foreground="#ffffff", font=('Segoe UI', 12))
    style.configure('Modern.TButton', background="#0078d4", foreground="#ffffff", font=('Segoe UI', 10, 'bold'))
    
    # Главный контейнер
    main_frame = ttk.Frame(root, style='Modern.TFrame', padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Заголовок
    title_label = ttk.Label(main_frame, text="Photo Editor Pro", style='Modern.TLabel')
    title_label.pack(pady=20)
    
    # Описание
    desc_label = ttk.Label(main_frame, text="Современный интерфейс для обработки изображений", style='Modern.TLabel')
    desc_label.pack(pady=10)
    
    # Кнопки
    button_frame = ttk.Frame(main_frame, style='Modern.TFrame')
    button_frame.pack(pady=20)
    
    load_btn = ttk.Button(button_frame, text="📁 Загрузить изображение", style='Modern.TButton')
    load_btn.pack(side=tk.LEFT, padx=10)
    
    save_btn = ttk.Button(button_frame, text="💾 Сохранить результат", style='Modern.TButton')
    save_btn.pack(side=tk.LEFT, padx=10)
    
    # Область для изображений
    image_frame = ttk.Frame(main_frame, style='Modern.TFrame')
    image_frame.pack(fill=tk.BOTH, expand=True, pady=20)
    
    # Исходное изображение
    original_frame = ttk.LabelFrame(image_frame, text="Исходное изображение", padding="10")
    original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
    
    original_canvas = tk.Canvas(original_frame, bg="#1e1e1e", height=300)
    original_canvas.pack(fill=tk.BOTH, expand=True)
    original_canvas.create_text(150, 150, text="Загрузите изображение\nдля начала работы", 
                              fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
    
    # Обработанное изображение
    processed_frame = ttk.LabelFrame(image_frame, text="Обработанное изображение", padding="10")
    processed_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
    
    processed_canvas = tk.Canvas(processed_frame, bg="#1e1e1e", height=300)
    processed_canvas.pack(fill=tk.BOTH, expand=True)
    processed_canvas.create_text(150, 150, text="Примените преобразование\nдля просмотра результата", 
                               fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
    
    # Статус
    status_label = ttk.Label(main_frame, text="Готов к работе", style='Modern.TLabel')
    status_label.pack(pady=10)
    
    return root

def main():
    """Главная функция."""
    print("🚀 Запуск упрощенного теста современного интерфейса...")
    
    try:
        root = create_simple_modern_window()
        print("✅ Окно создано успешно!")
        print("✨ Особенности:")
        print("   • Темная тема")
        print("   • Современные цвета")
        print("   • Стильные компоненты")
        print("   • Удобное сравнение до/после")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
