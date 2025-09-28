"""
Негативное преобразование изображений.
"""

import numpy as np
from typing import Dict, Any
import logging

from .base_transform import BaseTransform

logger = logging.getLogger(__name__)


class NegativeTransform(BaseTransform):
    """Класс для негативного преобразования изображений."""
    
    def apply(self, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет негативное преобразование к изображению.
        
        Args:
            image_array: Массив изображения
            **kwargs: Дополнительные параметры
            
        Returns:
            np.ndarray: Преобразованный массив изображения
        """
        try:
            # Сохраняем параметры
            self.save_parameters()
            
            logger.info("Применение негативного преобразования")
            
            # Применяем негативное преобразование
            # Формула: s = 255 - r, где r - исходное значение, s - результат
            negative_array = 255 - image_array
            
            logger.info("Негативное преобразование успешно применено")
            return negative_array
            
        except Exception as e:
            logger.error(f"Ошибка при применении негативного преобразования: {e}")
            raise
    
    def get_name(self) -> str:
        """Возвращает название преобразования."""
        return "Негативное"
    
    def validate_parameters(self, **kwargs) -> bool:
        """Валидирует параметры негативного преобразования."""
        # Негативное преобразование не требует параметров
        return True
    
    def get_optimal_parameters(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Вычисляет оптимальные параметры для негативного преобразования."""
        # Негативное преобразование не требует параметров
        return {}
