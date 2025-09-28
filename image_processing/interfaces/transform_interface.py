"""
Интерфейс для преобразований изображений.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import numpy as np


class TransformInterface(ABC):
    """Интерфейс для преобразований изображений."""
    
    @abstractmethod
    def apply(self, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет преобразование к массиву изображения.
        
        Args:
            image_array: Массив изображения
            **kwargs: Дополнительные параметры преобразования
            
        Returns:
            np.ndarray: Преобразованный массив изображения
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Возвращает название преобразования.
        
        Returns:
            str: Название преобразования
        """
        pass
    
    @abstractmethod
    def validate_parameters(self, **kwargs) -> bool:
        """
        Валидирует параметры преобразования.
        
        Args:
            **kwargs: Параметры для валидации
            
        Returns:
            bool: True если параметры корректны, False иначе
        """
        pass
    
    @abstractmethod
    def get_optimal_parameters(self, image_array: np.ndarray) -> Dict[str, Any]:
        """
        Вычисляет оптимальные параметры для изображения.
        
        Args:
            image_array: Массив изображения
            
        Returns:
            Dict[str, Any]: Словарь с оптимальными параметрами
        """
        pass
