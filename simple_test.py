#!/usr/bin/env python3
"""
Простой тест для проверки исправления.
"""

import numpy as np

# Тестируем, что numpy работает с числовыми значениями
print("Тестирование numpy операций...")

# Создаем тестовые данные
quality_ratings = [90.0, 75.0, 60.0, 30.0]
print(f"quality_ratings: {quality_ratings}")

# Тестируем операции
try:
    mean_val = np.mean(quality_ratings)
    print(f"np.mean работает: {mean_val}")
    
    min_val = min(quality_ratings)
    print(f"min работает: {min_val}")
    
    max_val = max(quality_ratings)
    print(f"max работает: {max_val}")
    
    print("✅ Все операции работают корректно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")

print("Тест завершен.")
