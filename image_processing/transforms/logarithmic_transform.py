"""
Логарифмическое преобразование изображений.
"""

import math
import numpy as np
from typing import Dict, Any, Optional
import logging

from .base_transform import BaseTransform

logger = logging.getLogger(__name__)


class LogarithmicTransform(BaseTransform):
    """Класс для логарифмического преобразования изображений."""
    
    def apply(self, image_array: np.ndarray, c: Optional[float] = None, **kwargs) -> np.ndarray:
        """
        Применяет логарифмическое преобразование к изображению.
        
        Args:
            image_array: Массив изображения
            c: Коэффициент для логарифмического преобразования
            **kwargs: Дополнительные параметры
            
        Returns:
            np.ndarray: Преобразованный массив изображения
        """
        try:
            # Конвертируем в float для точных вычислений
            image_float = image_array.astype(np.float64)
            
            # Нормализуем значения в диапазон [0, 1]
            if image_float.max() > 1.0:
                image_float = image_float / 255.0
            
            # Вычисляем коэффициент c если не задан
            if c is None:
                c = self._calculate_optimal_c(image_float)
            
            # Сохраняем параметры
            self.save_parameters(c=c)
            
            logger.info(f"Применение логарифмического преобразования с коэффициентом c = {c}")
            
            # Применяем логарифмическое преобразование
            # Формула: s = c * log(1 + r), где r - исходное значение, s - результат
            processed_array = c * np.log(1 + image_float)
            
            # Нормализуем результат обратно в диапазон [0, 255]
            processed_array = np.clip(processed_array * 255, 0, 255)
            processed_array = processed_array.astype(np.uint8)
            
            logger.info("Логарифмическое преобразование успешно применено")
            return processed_array
            
        except Exception as e:
            logger.error(f"Ошибка при применении логарифмического преобразования: {e}")
            raise
    
    def get_name(self) -> str:
        """Возвращает название преобразования."""
        return "Логарифмическое"
    
    def validate_parameters(self, **kwargs) -> bool:
        """Валидирует параметры логарифмического преобразования."""
        c = kwargs.get('c')
        if c is not None and c <= 0:
            return False
        return True
    
    def get_optimal_parameters(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Вычисляет оптимальный коэффициент c."""
        try:
            # Конвертируем в float для точных вычислений
            image_float = image_array.astype(np.float64)
            
            # Нормализуем значения в диапазон [0, 1]
            if image_float.max() > 1.0:
                image_float = image_float / 255.0
            
            c = self._calculate_optimal_c(image_float)
            return {'c': c}
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении оптимальных параметров: {e}")
            return {'c': 1.0}
    
    def _calculate_optimal_c(self, image_array: np.ndarray) -> float:
        """
        Вычисляет оптимальный коэффициент c для логарифмического преобразования.
        
        Args:
            image_array: Массив изображения в формате float [0, 1]
            
        Returns:
            float: Оптимальный коэффициент c
        """
        try:
            # Находим максимальное значение в изображении
            max_value = np.max(image_array)
            
            # Вычисляем коэффициент c так, чтобы максимальное значение
            # после преобразования было равно 1.0
            # c * log(1 + max_value) = 1.0
            # c = 1.0 / log(1 + max_value)
            c = 1.0 / math.log(1 + max_value)
            
            logger.info(f"Вычислен оптимальный коэффициент c = {c}")
            return c
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении коэффициента c: {e}")
            # Возвращаем значение по умолчанию
            return 1.0
