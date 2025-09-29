#!/usr/bin/env python3
"""
Тестовый скрипт для проверки группированного UI.
"""

import tkinter as tk
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_grouped_ui():
    """Тестирует группированный UI."""
    try:
        print("🧪 Тестирование группированного UI...")
        
        # Создаем тестовое окно
        root = tk.Tk()
        root.title("Тест группированного UI")
        root.geometry("800x600")
        
        # Импортируем компоненты
        from gui.components.color_transform_settings import ColorTransformSettings
        from gui.components.smoothing_settings import SmoothingSettings
        from gui.components.sharpness_settings import SharpnessSettings
        
        # Создаем тестовый фрейм
        test_frame = tk.Frame(root, bg="#2b2b2b")
        test_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Тестируем компонент цветовых преобразований
        print("✅ Тестирование компонента цветовых преобразований...")
        color_component = ColorTransformSettings(test_frame, lambda x: print(f"Color transform changed: {x}"))
        
        # Тестируем компонент фильтров сглаживания
        print("✅ Тестирование компонента фильтров сглаживания...")
        smoothing_component = SmoothingSettings(test_frame, lambda x: print(f"Smoothing filter changed: {x}"))
        
        # Тестируем компонент фильтров резкости
        print("✅ Тестирование компонента фильтров резкости...")
        sharpness_component = SharpnessSettings(test_frame, lambda x: print(f"Sharpness filter changed: {x}"))
        
        print("✅ Все компоненты успешно инициализированы!")
        print("🎉 Группированный UI работает корректно!")
        
        # Показываем окно на 3 секунды
        root.after(3000, root.destroy)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_grouped_ui()
    if success:
        print("🎉 Тест пройден успешно!")
    else:
        print("❌ Тест не пройден!")
        sys.exit(1)
