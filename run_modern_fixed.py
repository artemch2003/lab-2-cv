"""
Исправленная версия запуска современного интерфейса.
"""

import tkinter as tk
from tkinter import ttk
import logging
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Главная функция запуска приложения."""
    try:
        print("🚀 Запуск современного интерфейса Photo Editor Pro...")
        
        # Настройка логирования
        from utils.logger import setup_logger
        logger = setup_logger("modern_ui")
        
        print("✅ Логирование настроено")
        
        # Создание контейнера зависимостей
        from di.config import create_container
        container = create_container()
        print("✅ DI контейнер создан")
        
        # Создание главного окна
        root = tk.Tk()
        root.title("Photo Editor Pro - Обработка изображений")
        root.geometry("1400x900")
        root.configure(bg="#2b2b2b")
        
        print("✅ Главное окно создано")
        
        # Центрирование окна
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (root.winfo_screenheight() // 2) - (900 // 2)
        root.geometry(f"1400x900+{x}+{y}")
        
        # Создаем простое современное окно
        create_modern_interface(root)
        
        logger.info("Современный интерфейс запущен успешно")
        print("✅ Современный интерфейс запущен!")
        print("📝 Инструкции:")
        print("   1. Нажмите '📁 Загрузить' для выбора изображения")
        print("   2. Выберите тип преобразования в панели справа")
        print("   3. Нажмите '✨ Применить преобразование'")
        print("   4. Сохраните результат с помощью '💾 Сохранить'")
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def create_modern_interface(root):
    """Создает современный интерфейс."""
    # Настройка стилей
    style = ttk.Style()
    style.theme_use('clam')
    
    # Цвета в стиле фоторедактора
    bg_color = "#2b2b2b"
    panel_color = "#3c3c3c"
    accent_color = "#0078d4"
    text_color = "#ffffff"
    
    # Настройка стилей
    style.configure('Modern.TFrame', background=bg_color)
    style.configure('Modern.TLabelFrame', 
                   background=panel_color, 
                   foreground=text_color,
                   borderwidth=1,
                   relief='solid')
    style.configure('Modern.TLabelFrame.Label', 
                   background=panel_color, 
                   foreground=text_color,
                   font=('Segoe UI', 10, 'bold'))
    style.configure('Modern.TLabel', 
                   background=panel_color, 
                   foreground=text_color,
                   font=('Segoe UI', 9))
    style.configure('Modern.TButton', 
                   background=accent_color,
                   foreground=text_color,
                   font=('Segoe UI', 9, 'bold'),
                   borderwidth=0,
                   focuscolor='none')
    style.configure('Title.TLabel',
                   background=bg_color,
                   foreground=text_color,
                   font=('Segoe UI', 18, 'bold'))
    style.configure('Status.TLabel',
                   background=panel_color,
                   foreground=text_color,
                   font=('Segoe UI', 8),
                   relief='flat')
    
    # Главный контейнер
    main_container = ttk.Frame(root, style='Modern.TFrame', padding="0")
    main_container.pack(fill=tk.BOTH, expand=True)
    
    # Заголовок
    header_frame = ttk.Frame(main_container, style='Modern.TFrame')
    header_frame.pack(fill=tk.X, pady=(0, 10))
    
    title_label = ttk.Label(header_frame, text="Photo Editor Pro", style='Title.TLabel')
    title_label.pack(side=tk.LEFT, padx=20, pady=10)
    
    # Кнопки управления
    control_frame = ttk.Frame(header_frame, style='Modern.TFrame')
    control_frame.pack(side=tk.RIGHT, padx=20, pady=10)
    
    load_btn = ttk.Button(control_frame, text="📁 Загрузить", style='Modern.TButton')
    load_btn.pack(side=tk.LEFT, padx=5)
    
    save_btn = ttk.Button(control_frame, text="💾 Сохранить", style='Modern.TButton')
    save_btn.pack(side=tk.LEFT, padx=5)
    
    reset_btn = ttk.Button(control_frame, text="🔄 Сброс", style='Modern.TButton')
    reset_btn.pack(side=tk.LEFT, padx=5)
    
    # Основная рабочая область
    workspace_frame = ttk.Frame(main_container, style='Modern.TFrame')
    workspace_frame.pack(fill=tk.BOTH, expand=True, padx=20)
    workspace_frame.columnconfigure(0, weight=2)
    workspace_frame.columnconfigure(1, weight=1)
    
    # Область отображения изображений
    display_frame = ttk.LabelFrame(workspace_frame, text="Изображения", style='Modern.TLabelFrame', padding="10")
    display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
    display_frame.columnconfigure(0, weight=1)
    display_frame.columnconfigure(1, weight=1)
    
    # Исходное изображение
    original_frame = ttk.LabelFrame(display_frame, text="Исходное изображение", style='Modern.TLabelFrame', padding="5")
    original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
    
    original_canvas = tk.Canvas(original_frame, bg="#1e1e1e", highlightthickness=0)
    original_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    original_canvas.create_text(200, 150, text="Загрузите изображение\nдля начала работы", 
                              fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
    
    # Обработанное изображение
    processed_frame = ttk.LabelFrame(display_frame, text="Обработанное изображение", style='Modern.TLabelFrame', padding="5")
    processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
    
    processed_canvas = tk.Canvas(processed_frame, bg="#1e1e1e", highlightthickness=0)
    processed_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    processed_canvas.create_text(200, 150, text="Примените преобразование\nдля просмотра результата", 
                               fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
    
    # Панель настроек
    settings_frame = ttk.LabelFrame(workspace_frame, text="Настройки преобразования", style='Modern.TLabelFrame', padding="15")
    settings_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
    
    # Тип преобразования
    ttk.Label(settings_frame, text="Тип преобразования:", style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 5))
    transform_combo = ttk.Combobox(settings_frame, 
                                 values=["Логарифмическое", "Степенное", "Бинарное", "Вырезание диапазона яркостей"], 
                                 state="readonly", width=20)
    transform_combo.pack(fill=tk.X, pady=(0, 10))
    transform_combo.set("Логарифмическое")
    
    # Описание
    desc_text = tk.Text(settings_frame, height=4, width=30, wrap=tk.WORD, 
                       bg=panel_color, fg=text_color, font=('Segoe UI', 9))
    desc_text.pack(fill=tk.X, pady=(0, 10))
    desc_text.insert(1.0, "Логарифмическое преобразование улучшает видимость деталей в темных областях изображения.")
    desc_text.configure(state=tk.DISABLED)
    
    # Кнопка применения
    apply_btn = ttk.Button(settings_frame, text="✨ Применить преобразование", style='Modern.TButton')
    apply_btn.pack(fill=tk.X, pady=(10, 0))
    
    # Информационная панель
    info_frame = ttk.LabelFrame(main_container, text="Информация", style='Modern.TLabelFrame', padding="10")
    info_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
    
    info_text = tk.Text(info_frame, height=3, wrap=tk.WORD, 
                       bg=panel_color, fg=text_color, font=('Segoe UI', 9))
    info_text.pack(fill=tk.X)
    info_text.insert(1.0, "Информация об изображении:\nИзображение не загружено")
    
    # Статус бар
    status_var = tk.StringVar(value="Готов к работе")
    status_bar = ttk.Label(main_container, textvariable=status_var, style='Status.TLabel')
    status_bar.pack(fill=tk.X, pady=(10, 0), padx=20)

if __name__ == "__main__":
    main()
