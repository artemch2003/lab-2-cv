#!/usr/bin/env python3
"""
Тест для проверки исправления ошибки в SharpnessComparator.
"""

import numpy as np
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from image_processing.sharpness_comparator import SharpnessComparator

def test_sharpness_comparator():
    """Тестирует работу компаратора фильтров резкости."""
    print("🧪 Тестирование SharpnessComparator...")
    
    try:
        # Создаем тестовое изображение
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        print(f"✅ Создано тестовое изображение: {test_image.shape}")
        
        # Создаем компаратор
        comparator = SharpnessComparator()
        print("✅ Создан SharpnessComparator")
        
        # Тестируем сравнение с минимальными параметрами
        print("🔄 Запуск сравнения фильтров...")
        results = comparator.compare_sharpness_filters(
            test_image,
            kernel_sizes=[3],  # Только одно значение для быстрого теста
            lambda_values=[1.0]  # Только одно значение для быстрого теста
        )
        
        print(f"✅ Сравнение завершено успешно!")
        print(f"   Протестировано фильтров: {len(results['quality_metrics'])}")
        print(f"   Результаты: {list(results['quality_metrics'].keys())}")
        
        # Проверяем, что метрики содержат числовые значения
        for filter_name, metrics in results['quality_metrics'].items():
            quality_rating = metrics['quality_rating']
            print(f"   {filter_name}: quality_rating = {quality_rating} (тип: {type(quality_rating)})")
            
            # Проверяем, что это число
            if not isinstance(quality_rating, (int, float)):
                raise ValueError(f"quality_rating должен быть числом, получен {type(quality_rating)}")
        
        # Тестируем форматирование отчета
        print("🔄 Тестирование форматирования отчета...")
        report = comparator.format_comparison_report()
        print(f"✅ Отчет сгенерирован (длина: {len(report)} символов)")
        
        # Тестируем рекомендации
        print("🔄 Тестирование рекомендаций...")
        recommendations = comparator.get_filter_recommendations()
        print(f"✅ Рекомендации сгенерированы (количество: {len(recommendations)})")
        
        print("\n🎉 Все тесты прошли успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в тесте: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sharpness_comparator()
    sys.exit(0 if success else 1)
