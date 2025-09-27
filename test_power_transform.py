#!/usr/bin/env python3
"""
Демонстрационный скрипт для степенного преобразования изображений.
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
    """Создает тестовое изображение для демонстрации степенного преобразования."""
    width, height = 400, 300
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Создаем горизонтальный градиент от 0 до 255
    for x in range(width):
        intensity = int(255 * x / width)
        image_array[:, x] = [intensity, intensity, intensity]
    
    # Добавляем вертикальные полосы для разнообразия
    for y in range(height):
        if y % 40 < 20:  # Каждая вторая полоса
            image_array[y, :] = image_array[y, :] // 2
    
    return Image.fromarray(image_array)

def test_power_transform():
    """Тестирует степенное преобразование с разными значениями гаммы."""
    logger = setup_logger()
    logger.info("Тестирование степенного преобразования")
    
    try:
        # Создаем тестовое изображение
        test_image = create_test_image()
        test_path = "test_power_image.png"
        test_image.save(test_path)
        print(f"✅ Создано тестовое изображение: {test_path}")
        
        # Создаем процессор изображений
        processor = ImageProcessor()
        
        # Загружаем изображение
        if not processor.load_image(test_path):
            print("❌ Ошибка загрузки изображения")
            return False
        
        print("✅ Изображение загружено")
        
        # Тестируем разные значения гаммы
        gamma_values = [0.5, 1.0, 1.5, 2.0]
        
        for gamma in gamma_values:
            print(f"\n🧪 Тестирование степенного преобразования с γ = {gamma}")
            
            # Применяем степенное преобразование
            if not processor.apply_power_transform(gamma):
                print(f"❌ Ошибка применения степенного преобразования с γ = {gamma}")
                continue
            
            print(f"✅ Степенное преобразование применено с γ = {gamma}")
            
            # Получаем информацию о коэффициенте
            info = processor.get_image_info()
            c_value = info.get('last_coefficient_c', 'неизвестно')
            print(f"   📐 Коэффициент c: {c_value}")
            print(f"   🧮 Формула: c = 1.0 / (max_value^γ)")
            
            # Сохраняем результат
            result_path = f"test_power_result_gamma_{gamma}.png"
            if processor.save_image(result_path):
                print(f"✅ Результат сохранен: {result_path}")
            else:
                print(f"❌ Ошибка сохранения результата для γ = {gamma}")
        
        # Очищаем временные файлы
        if os.path.exists(test_path):
            os.remove(test_path)
        
        print(f"\n🎉 Тестирование степенного преобразования завершено!")
        print(f"   Теперь запустите графическое приложение: python main.py")
        print(f"   Выберите 'Степенное' в типе преобразования")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при тестировании: {e}")
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Тестирование степенного преобразования")
    print("=" * 50)
    
    success = test_power_transform()
    
    if not success:
        print("❌ Тест завершился с ошибками")
        sys.exit(1)
