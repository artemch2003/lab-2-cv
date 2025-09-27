#!/usr/bin/env python3
"""
Демонстрационный скрипт для создания тестового изображения
и показа работы логарифмического преобразования.
"""

import numpy as np
from PIL import Image
import os
import sys

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_processing.image_processor import ImageProcessor
from utils.logger import setup_logger

def create_demo_image():
    """Создает демонстрационное изображение с различными паттернами."""
    width, height = 600, 400
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Создаем несколько зон с разной яркостью
    # Зона 1: Горизонтальный градиент (слева направо)
    for x in range(width // 3):
        intensity = int(255 * x / (width // 3))
        image_array[:, x] = [intensity, intensity, intensity]
    
    # Зона 2: Вертикальный градиент (сверху вниз)
    for y in range(height):
        intensity = int(255 * y / height)
        for x in range(width // 3, 2 * width // 3):
            image_array[y, x] = [intensity, intensity, intensity]
    
    # Зона 3: Шахматный паттерн
    for y in range(height):
        for x in range(2 * width // 3, width):
            if (x + y) % 40 < 20:
                image_array[y, x] = [255, 255, 255]
            else:
                image_array[y, x] = [0, 0, 0]
    
    # Добавляем круг в центре
    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 6
    
    for y in range(height):
        for x in range(width):
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            if distance < radius:
                # Создаем радиальный градиент
                intensity = int(255 * (1 - distance / radius))
                image_array[y, x] = [intensity, intensity, intensity]
    
    return Image.fromarray(image_array)

def run_demo():
    """Запускает демонстрацию работы приложения."""
    logger = setup_logger()
    logger.info("Запуск демонстрации приложения")
    
    try:
        # Создаем демонстрационное изображение
        demo_image = create_demo_image()
        demo_path = "demo_image.png"
        demo_image.save(demo_path)
        logger.info(f"Создано демонстрационное изображение: {demo_path}")
        
        # Создаем процессор изображений
        processor = ImageProcessor()
        
        # Загружаем изображение
        if not processor.load_image(demo_path):
            logger.error("Ошибка загрузки демонстрационного изображения")
            return False
        
        logger.info("Демонстрационное изображение загружено")
        
        # Применяем логарифмическое преобразование с автоматическим коэффициентом
        if not processor.apply_logarithmic_transform():
            logger.error("Ошибка применения логарифмического преобразования")
            return False
        
        logger.info("Логарифмическое преобразование применено")
        
        # Сохраняем результат
        result_path = "demo_result.png"
        if not processor.save_image(result_path):
            logger.error("Ошибка сохранения результата")
            return False
        
        logger.info(f"Результат сохранен: {result_path}")
        
        # Выводим информацию
        info = processor.get_image_info()
        print(f"\n📊 Информация об изображении:")
        print(f"   Размер: {info.get('size', 'Неизвестно')}")
        print(f"   Режим: {info.get('mode', 'Неизвестно')}")
        print(f"   Формат: {info.get('format', 'Неизвестно')}")
        print(f"   Обработано: {'Да' if info.get('has_processed', False) else 'Нет'}")
        
        print(f"\n📁 Созданные файлы:")
        print(f"   Исходное изображение: {demo_path}")
        print(f"   Обработанное изображение: {result_path}")
        
        print(f"\n🎉 Демонстрация завершена успешно!")
        print(f"   Теперь вы можете запустить графическое приложение: python main.py")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при демонстрации: {e}")
        return False

if __name__ == "__main__":
    print("🎬 Демонстрация приложения обработки изображений")
    print("=" * 50)
    
    success = run_demo()
    
    if not success:
        print("❌ Демонстрация завершилась с ошибками")
        sys.exit(1)
