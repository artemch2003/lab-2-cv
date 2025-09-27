#!/usr/bin/env python3
"""
Скрипт для тестирования приложения обработки изображений.
Создает тестовое изображение и проверяет работу алгоритмов.
"""

import numpy as np
from PIL import Image
import os
import sys

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_processing.image_processor import ImageProcessor
from utils.logger import setup_logger

def create_test_image():
    """Создает тестовое изображение для проверки алгоритмов."""
    # Создаем градиентное изображение
    width, height = 400, 300
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Создаем горизонтальный градиент
    for x in range(width):
        intensity = int(255 * x / width)
        image_array[:, x] = [intensity, intensity, intensity]
    
    # Добавляем вертикальные полосы для разнообразия
    for y in range(height):
        if y % 50 < 25:  # Каждая вторая полоса
            image_array[y, :] = image_array[y, :] // 2
    
    return Image.fromarray(image_array)

def test_logarithmic_transform():
    """Тестирует логарифмическое преобразование."""
    logger = setup_logger()
    logger.info("Начало тестирования логарифмического преобразования")
    
    try:
        # Создаем тестовое изображение
        test_image = create_test_image()
        test_path = "test_image.png"
        test_image.save(test_path)
        logger.info(f"Создано тестовое изображение: {test_path}")
        
        # Тестируем процессор изображений
        processor = ImageProcessor()
        
        # Загружаем изображение
        if not processor.load_image(test_path):
            logger.error("Ошибка загрузки тестового изображения")
            return False
        
        logger.info("Тестовое изображение успешно загружено")
        
        # Применяем логарифмическое преобразование
        if not processor.apply_logarithmic_transform():
            logger.error("Ошибка применения логарифмического преобразования")
            return False
        
        logger.info("Логарифмическое преобразование успешно применено")
        
        # Сохраняем результат
        result_path = "test_result.png"
        if not processor.save_image(result_path):
            logger.error("Ошибка сохранения результата")
            return False
        
        logger.info(f"Результат сохранен: {result_path}")
        
        # Получаем информацию об изображении
        info = processor.get_image_info()
        logger.info(f"Информация об изображении: {info}")
        
        # Очищаем временные файлы
        if os.path.exists(test_path):
            os.remove(test_path)
        logger.info("Тестирование завершено успешно")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при тестировании: {e}")
        return False

if __name__ == "__main__":
    print("Тестирование приложения обработки изображений...")
    success = test_logarithmic_transform()
    
    if success:
        print("✅ Все тесты прошли успешно!")
    else:
        print("❌ Тесты завершились с ошибками")
        sys.exit(1)
