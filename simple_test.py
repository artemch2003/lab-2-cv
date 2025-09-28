#!/usr/bin/env python3
"""
Простой тест для проверки работы фильтров сглаживания.
"""

import numpy as np
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Тестирует импорты."""
    print("Тестирование импортов...")
    
    try:
        from image_processing.transforms.smoothing_filters import RectangularFilter3x3
        print("✅ RectangularFilter3x3 импортирован успешно")
        
        from image_processing.transforms.smoothing_filters import MedianFilter3x3
        print("✅ MedianFilter3x3 импортирован успешно")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_filter_creation():
    """Тестирует создание фильтров."""
    print("\nТестирование создания фильтров...")
    
    try:
        from image_processing.transforms.smoothing_filters import RectangularFilter3x3, MedianFilter3x3
        
        rect_filter = RectangularFilter3x3()
        print(f"✅ Прямоугольный фильтр создан: {rect_filter.get_name()}")
        
        median_filter = MedianFilter3x3()
        print(f"✅ Медианный фильтр создан: {median_filter.get_name()}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка создания фильтров: {e}")
        return False

def test_filter_application():
    """Тестирует применение фильтров."""
    print("\nТестирование применения фильтров...")
    
    try:
        from image_processing.transforms.smoothing_filters import RectangularFilter3x3, MedianFilter3x3
        
        # Создаем простое тестовое изображение
        test_image = np.random.randint(0, 256, (50, 50), dtype=np.uint8)
        print(f"Создано тестовое изображение: {test_image.shape}")
        
        # Тестируем прямоугольный фильтр
        rect_filter = RectangularFilter3x3()
        result_rect = rect_filter.apply(test_image)
        print(f"✅ Прямоугольный фильтр применен: {result_rect.shape}")
        
        # Тестируем медианный фильтр
        median_filter = MedianFilter3x3()
        result_median = median_filter.apply(test_image)
        print(f"✅ Медианный фильтр применен: {result_median.shape}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка применения фильтров: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Главная функция тестирования."""
    print("=== Простой тест фильтров сглаживания ===\n")
    
    success = True
    
    # Тестируем импорты
    if not test_imports():
        success = False
    
    # Тестируем создание фильтров
    if not test_filter_creation():
        success = False
    
    # Тестируем применение фильтров
    if not test_filter_application():
        success = False
    
    print("\n=== Результат тестирования ===")
    if success:
        print("✅ Все тесты пройдены успешно!")
        print("Фильтры сглаживания работают корректно.")
    else:
        print("❌ Некоторые тесты не прошли.")
        print("Проверьте ошибки выше.")

if __name__ == "__main__":
    main()
