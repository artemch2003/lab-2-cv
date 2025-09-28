#!/usr/bin/env python3
"""
Простой запуск приложения с фильтрами сглаживания.
"""

import tkinter as tk
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Главная функция приложения."""
    try:
        # Создаем контейнер зависимостей
        from di.config import create_container
        container = create_container()
        
        # Создаем главное окно
        root = tk.Tk()
        root.title("Photo Editor Pro - Сглаживание")
        root.geometry("1200x800")
        
        # Простой интерфейс для тестирования
        from gui.components.modern_smoothing_settings import ModernSmoothingSettings
        
        # Создаем фрейм для настроек
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Создаем настройки сглаживания
        def on_filter_change(filter_type):
            print(f"Выбран фильтр: {filter_type}")
        
        smoothing_settings = ModernSmoothingSettings(main_frame, on_filter_change)
        
        # Добавляем кнопку для тестирования
        def test_filter():
            try:
                parameters = smoothing_settings.get_filter_parameters()
                print(f"Параметры фильтра: {parameters}")
                
                # Тестируем создание фильтра
                from image_processing.factories.transform_factory import TransformFactory
                filter_transform = TransformFactory.create_transform(parameters['transform_type'])
                print(f"Фильтр создан: {filter_transform.get_name()}")
                
                # Показываем сообщение об успехе
                tk.messagebox.showinfo("Успех", f"Фильтр {filter_transform.get_name()} готов к использованию!")
                
            except Exception as e:
                tk.messagebox.showerror("Ошибка", f"Ошибка при создании фильтра: {e}")
        
        test_button = tk.Button(main_frame, text="Тестировать фильтр", command=test_filter)
        test_button.pack(pady=10)
        
        print("Приложение запущено успешно!")
        print("Доступные фильтры:")
        print("- Прямоугольный фильтр 3x3")
        print("- Прямоугольный фильтр 5x5") 
        print("- Медианный фильтр 3x3")
        print("- Медианный фильтр 5x5")
        
        # Запускаем главный цикл
        root.mainloop()
        
    except Exception as e:
        print(f"Ошибка при запуске приложения: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
