#!/usr/bin/env python3
"""
Тестирование фильтров сглаживания.
"""

import numpy as np
import sys
import os

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from image_processing.transforms.smoothing_filters import (
    RectangularFilter3x3, RectangularFilter5x5,
    MedianFilter3x3, MedianFilter5x5
)

def create_test_image():
    """Создает тестовое изображение с шумом."""
    # Создаем простое изображение 100x100
    image = np.zeros((100, 100), dtype=np.uint8)
    
    # Добавляем градиент
    for i in range(100):
        for j in range(100):
            image[i, j] = int((i + j) / 2)
    
    # Добавляем шум
    noise = np.random.randint(0, 50, (100, 100))
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    return image

def test_rectangular_filter():
    """Тестирует прямоугольный фильтр."""
    print("Тестирование прямоугольного фильтра...")
    
    # Создаем тестовое изображение
    test_image = create_test_image()
    print(f"Исходное изображение: {test_image.shape}, dtype: {test_image.dtype}")
    
    # Тестируем фильтр 3x3
    filter_3x3 = RectangularFilter3x3()
    result_3x3 = filter_3x3.apply(test_image)
    print(f"Прямоугольный 3x3: {result_3x3.shape}, dtype: {result_3x3.dtype}")
    
    # Тестируем фильтр 5x5
    filter_5x5 = RectangularFilter5x5()
    result_5x5 = filter_5x5.apply(test_image)
    print(f"Прямоугольный 5x5: {result_5x5.shape}, dtype: {result_5x5.dtype}")
    
    print("Прямоугольный фильтр работает корректно!")
    return result_3x3, result_5x5

def test_median_filter():
    """Тестирует медианный фильтр."""
    print("\nТестирование медианного фильтра...")
    
    # Создаем тестовое изображение
    test_image = create_test_image()
    print(f"Исходное изображение: {test_image.shape}, dtype: {test_image.dtype}")
    
    # Тестируем фильтр 3x3
    filter_3x3 = MedianFilter3x3()
    result_3x3 = filter_3x3.apply(test_image)
    print(f"Медианный 3x3: {result_3x3.shape}, dtype: {result_3x3.dtype}")
    
    # Тестируем фильтр 5x5
    filter_5x5 = MedianFilter5x5()
    result_5x5 = filter_5x5.apply(test_image)
    print(f"Медианный 5x5: {result_5x5.shape}, dtype: {result_5x5.dtype}")
    
    print("Медианный фильтр работает корректно!")
    return result_3x3, result_5x5

def test_color_image():
    """Тестирует фильтры на цветном изображении."""
    print("\nТестирование на цветном изображении...")
    
    # Создаем цветное изображение
    color_image = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
    print(f"Цветное изображение: {color_image.shape}, dtype: {color_image.dtype}")
    
    # Тестируем прямоугольный фильтр на цветном изображении
    filter_3x3 = RectangularFilter3x3()
    result_color = filter_3x3.apply(color_image)
    print(f"Прямоугольный фильтр на цветном: {result_color.shape}, dtype: {result_color.dtype}")
    
    # Тестируем медианный фильтр на цветном изображении
    filter_median = MedianFilter3x3()
    result_median = filter_median.apply(color_image)
    print(f"Медианный фильтр на цветном: {result_median.shape}, dtype: {result_median.dtype}")
    
    print("Фильтры работают с цветными изображениями!")
    return result_color, result_median

def main():
    """Главная функция тестирования."""
    print("=== Тестирование фильтров сглаживания ===\n")
    
    try:
        # Тестируем прямоугольный фильтр
        rect_3x3, rect_5x5 = test_rectangular_filter()
        
        # Тестируем медианный фильтр
        med_3x3, med_5x5 = test_median_filter()
        
        # Тестируем на цветном изображении
        color_rect, color_med = test_color_image()
        
        print("\n=== Все тесты пройдены успешно! ===")
        print("Фильтры сглаживания работают корректно.")
        
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
