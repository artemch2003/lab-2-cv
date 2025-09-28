"""
Бинарное преобразование изображений.
"""

import numpy as np
from typing import Dict, Any
import logging

from .base_transform import BaseTransform

logger = logging.getLogger(__name__)


class BinaryTransform(BaseTransform):
    """Класс для бинарного преобразования изображений."""
    
    def apply(self, image_array: np.ndarray, threshold: float, **kwargs) -> np.ndarray:
        """
        Применяет бинарное преобразование к изображению.
        
        Args:
            image_array: Массив изображения
            threshold: Пороговое значение для бинарного преобразования (0-255)
            **kwargs: Дополнительные параметры
            
        Returns:
            np.ndarray: Преобразованный массив изображения
        """
        try:
            # Сохраняем параметры
            self.save_parameters(threshold=threshold)
            
            logger.info(f"Применение бинарного преобразования с порогом = {threshold}")
            
            # Конвертируем в grayscale если изображение цветное
            if len(image_array.shape) == 3:
                # Используем формулу для конвертации RGB в grayscale
                gray_array = np.dot(image_array[...,:3], [0.2989, 0.5870, 0.1140])
            else:
                gray_array = image_array.copy()
            
            # Применяем бинарное преобразование
            # Все пиксели выше порога становятся 255 (белые), ниже - 0 (черные)
            binary_array = np.where(gray_array >= threshold, 255, 0).astype(np.uint8)
            
            logger.info("Бинарное преобразование успешно применено")
            return binary_array
            
        except Exception as e:
            logger.error(f"Ошибка при применении бинарного преобразования: {e}")
            raise
    
    def get_name(self) -> str:
        """Возвращает название преобразования."""
        return "Бинарное"
    
    def validate_parameters(self, **kwargs) -> bool:
        """Валидирует параметры бинарного преобразования."""
        threshold = kwargs.get('threshold')
        if threshold is not None and (threshold < 0 or threshold > 255):
            return False
        return True
    
    def get_optimal_parameters(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Вычисляет оптимальные параметры для бинарного преобразования."""
        # Используем среднее значение как оптимальный порог
        if len(image_array.shape) == 3:
            gray_array = np.dot(image_array[...,:3], [0.2989, 0.5870, 0.1140])
        else:
            gray_array = image_array.copy()
        
        threshold = float(np.mean(gray_array))
        return {'threshold': threshold}
