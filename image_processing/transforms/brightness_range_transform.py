"""
Вырезание диапазона яркостей изображений.
"""

import numpy as np
from typing import Dict, Any, Optional
import logging

from .base_transform import BaseTransform

logger = logging.getLogger(__name__)


class BrightnessRangeTransform(BaseTransform):
    """Класс для вырезания диапазона яркостей изображений."""
    
    def apply(self, image_array: np.ndarray, min_brightness: float, max_brightness: float, 
              outside_mode: str, constant_value: Optional[float] = None, **kwargs) -> np.ndarray:
        """
        Применяет вырезание диапазона яркостей к изображению.
        
        Args:
            image_array: Массив изображения
            min_brightness: Минимальная яркость диапазона (0-255)
            max_brightness: Максимальная яркость диапазона (0-255)
            outside_mode: Режим обработки пикселей вне диапазона ("Константа" или "Исходное")
            constant_value: Константное значение для пикселей вне диапазона
            **kwargs: Дополнительные параметры
            
        Returns:
            np.ndarray: Преобразованный массив изображения
        """
        try:
            # Сохраняем параметры
            self.save_parameters(
                min_brightness=min_brightness,
                max_brightness=max_brightness,
                outside_mode=outside_mode,
                constant_value=constant_value
            )
            
            logger.info(f"Применение вырезания диапазона яркостей: {min_brightness}-{max_brightness}, режим: {outside_mode}")
            
            # Конвертируем в grayscale если изображение цветное
            if len(image_array.shape) == 3:
                # Используем формулу для конвертации RGB в grayscale
                gray_array = np.dot(image_array[...,:3], [0.2989, 0.5870, 0.1140])
            else:
                gray_array = image_array.copy()
            
            # Создаем маску для пикселей в диапазоне
            in_range_mask = (gray_array >= min_brightness) & (gray_array <= max_brightness)
            
            # Создаем результирующий массив
            result_array = gray_array.copy()
            
            if outside_mode == "Константа":
                # Пиксели вне диапазона заменяем на константное значение
                result_array[~in_range_mask] = constant_value
            else:  # "Исходное"
                # Пиксели вне диапазона остаются в исходном виде
                # Пиксели в диапазоне остаются без изменений
                pass  # result_array уже содержит исходные значения
            
            # Конвертируем в uint8
            result_array = result_array.astype(np.uint8)
            
            logger.info("Вырезание диапазона яркостей успешно применено")
            return result_array
            
        except Exception as e:
            logger.error(f"Ошибка при применении вырезания диапазона яркостей: {e}")
            raise
    
    def get_name(self) -> str:
        """Возвращает название преобразования."""
        return "Вырезание диапазона яркостей"
    
    def validate_parameters(self, **kwargs) -> bool:
        """Валидирует параметры вырезания диапазона яркостей."""
        min_brightness = kwargs.get('min_brightness')
        max_brightness = kwargs.get('max_brightness')
        outside_mode = kwargs.get('outside_mode')
        constant_value = kwargs.get('constant_value')
        
        if min_brightness is not None and (min_brightness < 0 or min_brightness > 255):
            return False
        if max_brightness is not None and (max_brightness < 0 or max_brightness > 255):
            return False
        if min_brightness is not None and max_brightness is not None and min_brightness >= max_brightness:
            return False
        if outside_mode == "Константа" and constant_value is not None:
            if constant_value < 0 or constant_value > 255:
                return False
        return True
    
    def get_optimal_parameters(self, image_array: np.ndarray) -> Dict[str, Any]:
        """Вычисляет оптимальные параметры для вырезания диапазона яркостей."""
        # Конвертируем в grayscale если изображение цветное
        if len(image_array.shape) == 3:
            gray_array = np.dot(image_array[...,:3], [0.2989, 0.5870, 0.1140])
        else:
            gray_array = image_array.copy()
        
        # Используем квантили для определения диапазона
        min_brightness = float(np.percentile(gray_array, 25))  # 25-й перцентиль
        max_brightness = float(np.percentile(gray_array, 75))  # 75-й перцентиль
        
        return {
            'min_brightness': min_brightness,
            'max_brightness': max_brightness,
            'outside_mode': 'Исходное',
            'constant_value': None
        }
