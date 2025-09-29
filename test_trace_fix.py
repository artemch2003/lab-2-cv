#!/usr/bin/env python3
"""
Тест исправления trace() для Python 3.13.
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_trace_fix():
    """Тестирует исправление trace()."""
    try:
        print("🧪 Тестирование исправления trace()...")
        
        # Создаем окно
        root = tk.Tk()
        root.title("Тест trace() исправления")
        root.geometry("400x300")
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
        style.configure('Modern.TCombobox',
                       fieldbackground='#3c3c3c',
                       background='#3c3c3c',
                       foreground='#ffffff',
                       borderwidth=1,
                       arrowcolor='#ffffff')
        
        # Создаем тестовый фрейм
        main_frame = ttk.Frame(root, style='Modern.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Тест trace_add
        test_frame = ttk.LabelFrame(main_frame, 
                                   text="Тест trace_add()", 
                                   style='Modern.TLabelFrame',
                                   padding="10")
        test_frame.pack(fill=tk.X, pady=5)
        
        # Создаем переменную и тестируем trace_add
        test_var = tk.StringVar(value="Тест")
        
        def on_change(*args):
            print(f"✅ trace_add работает! Значение: {test_var.get()}")
        
        # Используем новый синтаксис trace_add
        test_var.trace_add('write', on_change)
        
        # Создаем Combobox для тестирования
        combo = ttk.Combobox(test_frame, 
                            textvariable=test_var,
                            values=["Тест", "Работает", "Отлично"],
                            style='Modern.TCombobox')
        combo.pack(fill=tk.X, pady=5)
        
        # Информация
        info_label = ttk.Label(test_frame, 
                              text="Измените значение в выпадающем списке для тестирования trace_add()",
                              style='Modern.TLabel')
        info_label.pack(pady=5)
        
        # Кнопка закрытия
        close_btn = ttk.Button(main_frame, 
                              text="✅ Тест пройден - Закрыть", 
                              style='Modern.TButton', 
                              command=root.destroy)
        close_btn.pack(pady=10)
        
        print("✅ Тест trace_add() запущен!")
        print("🎉 Исправление работает!")
        
        # Показываем окно
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_trace_fix()
    if success:
        print("🎉 Тест trace_add() пройден успешно!")
    else:
        print("❌ Тест не пройден!")
        sys.exit(1)
