"""
Степенное преобразование изображений.
"""

import numpy as np
from typing import Dict, Any, Optional
import logging

from .base_transform import BaseTransform

logger = logging.getLogger(__name__)


class PowerTransform(BaseTransform):
    """Класс для степенного преобразования изображений."""
    
    def apply(self, image_array: np.ndarray, gamma: float, c: Optional[float] = None, **kwargs) -> np.ndarray:
        """
        Применяет степенное преобразование к изображению.
        
        Args:
            image_array: Массив изображения
            gamma: Значение гаммы для степенного преобразования
            c: Коэффициент для степенного преобразования
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
                c = self._calculate_optimal_c(image_float, gamma)
            
            # Сохраняем параметры
            self.save_parameters(gamma=gamma, c=c)
            
            logger.info(f"Применение степенного преобразования с гаммой γ = {gamma} и коэффициентом c = {c}")
            
            # Применяем степенное преобразование
            # Формула: s = c * r^γ, где r - исходное значение, s - результат, γ - гамма
            processed_array = c * np.power(image_float, gamma)
            
            # Нормализуем результат обратно в диапазон [0, 255]
            processed_array = np.clip(processed_array * 255, 0, 255)
            processed_array = processed_array.astype(np.uint8)
            
            logger.info("Степенное преобразование успешно применено")
            return processed_array
            
        except Exception as e:
            logger.error(f"Ошибка при применении степенного преобразования: {e}")
            raise
    
    def get_name(self) -> str:
        """Возвращает название преобразования."""
        return "Степенное"
    
    def validate_parameters(self, **kwargs) -> bool:
        """Валидирует параметры степенного преобразования."""
        gamma = kwargs.get('gamma')
        c = kwargs.get('c')
        
        if gamma is not None and gamma <= 0:
            return False
        if c is not None and c <= 0:
            return False
        return True
    
    def get_optimal_parameters(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Вычисляет оптимальные параметры для степенного преобразования."""
        try:
            # Конвертируем в float для точных вычислений
            image_float = image_array.astype(np.float64)
            
            # Нормализуем значения в диапазон [0, 1]
            if image_float.max() > 1.0:
                image_float = image_float / 255.0
            
            # Используем гамму по умолчанию
            gamma = 1.0
            c = self._calculate_optimal_c(image_float, gamma)
            return {'gamma': gamma, 'c': c}
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении оптимальных параметров: {e}")
            return {'gamma': 1.0, 'c': 1.0}
    
    def _calculate_optimal_c(self, image_array: np.ndarray, gamma: float) -> float:
        """
        Вычисляет оптимальный коэффициент c для степенного преобразования.
        
        Args:
            image_array: Массив изображения в формате float [0, 1]
            gamma: Значение гаммы для степенного преобразования
            
        Returns:
            float: Оптимальный коэффициент c
        """
        try:
            # Находим максимальное значение в изображении
            max_value = np.max(image_array)
            
            # Вычисляем коэффициент c так, чтобы максимальное значение
            # после преобразования было равно 1.0
            # c * max_value^γ = 1.0
            # c = 1.0 / (max_value^γ)
            c = 1.0 / (max_value ** gamma)
            
            logger.info(f"Вычислен оптимальный коэффициент c = {c} для гаммы γ = {gamma}")
            return c
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении коэффициента c для степенного преобразования: {e}")
            # Возвращаем значение по умолчанию
            return 1.0
