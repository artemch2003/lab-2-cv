#!/usr/bin/env python3
"""
Тестовый скрипт для демонстрации отображения коэффициента c.
"""

import numpy as np
from PIL import Image
import os
import sys

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_processing.image_processor import ImageProcessor
from utils.logger import setup_logger

def create_test_gradient():
    """Создает тестовое изображение с градиентом для демонстрации коэффициента."""
    width, height = 400, 300
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Создаем горизонтальный градиент от 0 до 255
    for x in range(width):
        intensity = int(255 * x / width)
        image_array[:, x] = [intensity, intensity, intensity]
    
    return Image.fromarray(image_array)

def test_coefficient_display():
    """Тестирует отображение коэффициента c."""
    logger = setup_logger()
    logger.info("Тестирование отображения коэффициента c")
    
    try:
        # Создаем тестовое изображение
        test_image = create_test_gradient()
        test_path = "test_gradient.png"
        test_image.save(test_path)
        print(f"✅ Создано тестовое изображение: {test_path}")
        
        # Создаем процессор изображений
        processor = ImageProcessor()
        
        # Загружаем изображение
        if not processor.load_image(test_path):
            print("❌ Ошибка загрузки изображения")
            return False
        
        print("✅ Изображение загружено")
        
        # Применяем логарифмическое преобразование
        if not processor.apply_logarithmic_transform():
            print("❌ Ошибка применения преобразования")
            return False
        
        print("✅ Логарифмическое преобразование применено")
        
        # Получаем информацию о коэффициенте
        info = processor.get_image_info()
        print(f"\n📊 Информация об изображении:")
        print(f"   Размер: {info.get('size')}")
        print(f"   Режим: {info.get('mode')}")
        print(f"   Обработано: {'Да' if info.get('has_processed', False) else 'Нет'}")
        
        if 'last_coefficient_c' in info:
            c_value = info.get('last_coefficient_c')
            print(f"   🎯 Коэффициент c: {c_value}")
            print(f"   📐 Формула: c = 1.0 / log(1 + max_value)")
            print(f"   💡 Этот коэффициент обеспечивает оптимальное отображение")
        else:
            print("   ⚠️  Коэффициент не найден")
        
        # Сохраняем результат
        result_path = "test_gradient_result.png"
        if processor.save_image(result_path):
            print(f"✅ Результат сохранен: {result_path}")
        else:
            print("❌ Ошибка сохранения результата")
            return False
        
        # Очищаем временные файлы
        if os.path.exists(test_path):
            os.remove(test_path)
        
        print(f"\n🎉 Тест завершен успешно!")
        print(f"   Теперь запустите графическое приложение: python main.py")
        print(f"   В автоматическом режиме вы увидите вычисленный коэффициент c")
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка при тестировании: {e}")
        print(f"❌ Ошибка: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Тестирование отображения коэффициента c")
    print("=" * 50)
    
    success = test_coefficient_display()
    
    if not success:
        print("❌ Тест завершился с ошибками")
        sys.exit(1)
