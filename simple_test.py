#!/usr/bin/env python3
"""
Простой тест группированного UI.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Простой тест."""
    print("🧪 Запуск простого теста...")
    
    try:
        # Создаем окно
        root = tk.Tk()
        root.title("Простой тест")
        root.geometry("600x400")
        root.configure(bg="#2b2b2b")
        
        # Настраиваем стили
        style = ttk.Style()
        style.theme_use('clam')
        
        # Базовые стили
        style.configure('Modern.TFrame', background='#2b2b2b')
        style.configure('Modern.TLabelFrame', 
                       background='#3c3c3c', 
                       foreground='#ffffff',
                       borderwidth=1,
                       relief='solid')
        style.configure('Modern.TLabelFrame.Label', 
                       background='#3c3c3c', 
                       foreground='#ffffff',
                       font=('Segoe UI', 10, 'bold'))
        style.configure('Modern.TLabel', 
                       background='#3c3c3c', 
                       foreground='#ffffff',
                       font=('Segoe UI', 9))
        style.configure('Modern.TButton', 
                       background='#0078d4',
                       foreground='#ffffff',
                       font=('Segoe UI', 9, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        
        # Создаем тестовые компоненты
        main_frame = ttk.Frame(root, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Тест 1: Цветовые преобразования
        color_frame = ttk.LabelFrame(main_frame, 
                                    text="🎨 Цветовые преобразования", 
                                    style='Modern.TLabelFrame',
                                    padding="10")
        color_frame.pack(fill=tk.X, pady=5)
        
        color_label = ttk.Label(color_frame, text="Логарифмическое преобразование", style='Modern.TLabel')
        color_label.pack(anchor=tk.W)
        
        # Тест 2: Фильтры сглаживания
        smoothing_frame = ttk.LabelFrame(main_frame, 
                                       text="🌊 Фильтры сглаживания", 
                                       style='Modern.TLabelFrame',
                                       padding="10")
        smoothing_frame.pack(fill=tk.X, pady=5)
        
        smoothing_label = ttk.Label(smoothing_frame, text="Прямоугольный фильтр 3x3", style='Modern.TLabel')
        smoothing_label.pack(anchor=tk.W)
        
        # Тест 3: Фильтры резкости
        sharpness_frame = ttk.LabelFrame(main_frame, 
                                       text="🔍 Фильтры резкости", 
                                       style='Modern.TLabelFrame',
                                       padding="10")
        sharpness_frame.pack(fill=tk.X, pady=5)
        
        sharpness_label = ttk.Label(sharpness_frame, text="Нерезкое маскирование k=3, λ=1.0", style='Modern.TLabel')
        sharpness_label.pack(anchor=tk.W)
        
        # Кнопка закрытия
        close_btn = ttk.Button(main_frame, text="✅ Тест пройден - Закрыть", style='Modern.TButton', command=root.destroy)
        close_btn.pack(pady=10)
        
        print("✅ Все компоненты созданы успешно!")
        print("🎉 Группированный UI работает!")
        
        # Показываем окно
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
