"""
Базовый класс для алгоритмов преобразования изображений.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any, Dict
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class BaseTransform(ABC):
    """Базовый класс для всех алгоритмов преобразования изображений."""
    
    def __init__(self):
        """Инициализация базового преобразования."""
        self.last_parameters: Optional[Dict[str, Any]] = None
    
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
    
    def validate_parameters(self, **kwargs) -> bool:
        """
        Валидирует параметры преобразования.
        
        Args:
            **kwargs: Параметры для валидации
            
        Returns:
            bool: True если параметры корректны, False иначе
        """
        return True
    
    def get_optimal_parameters(self, image_array: np.ndarray) -> Dict[str, Any]:
        """
        Вычисляет оптимальные параметры для изображения.
        
        Args:
            image_array: Массив изображения
            
        Returns:
            Dict[str, Any]: Словарь с оптимальными параметрами
        """
        return {}
    
    def save_parameters(self, **kwargs) -> None:
        """
        Сохраняет использованные параметры.
        
        Args:
            **kwargs: Параметры для сохранения
        """
        self.last_parameters = kwargs.copy()
    
    def get_last_parameters(self) -> Optional[Dict[str, Any]]:
        """
        Возвращает последние использованные параметры.
        
        Returns:
            Optional[Dict[str, Any]]: Последние параметры или None
        """
        return self.last_parameters
