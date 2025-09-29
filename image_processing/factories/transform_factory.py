"""
Фабрика для создания преобразований.
"""

from typing import Dict, Type
from ..transforms.base_transform import BaseTransform
from ..transforms.logarithmic_transform import LogarithmicTransform
from ..transforms.power_transform import PowerTransform
from ..transforms.binary_transform import BinaryTransform
from ..transforms.brightness_range_transform import BrightnessRangeTransform
from ..transforms.smoothing_filters import (
    RectangularFilter3x3, RectangularFilter5x5,
    MedianFilter3x3, MedianFilter5x5
)
import logging

logger = logging.getLogger(__name__)


class TransformFactory:
    """Фабрика для создания преобразований."""
    
    _transforms: Dict[str, Type[BaseTransform]] = {
        "Логарифмическое": LogarithmicTransform,
        "Степенное": PowerTransform,
        "Бинарное": BinaryTransform,
        "Вырезание диапазона яркостей": BrightnessRangeTransform,
        "Прямоугольный фильтр 3x3": RectangularFilter3x3,
        "Прямоугольный фильтр 5x5": RectangularFilter5x5,
        "Медианный фильтр 3x3": MedianFilter3x3,
        "Медианный фильтр 5x5": MedianFilter5x5
    }
    
    @classmethod
    def create_transform(cls, transform_name: str) -> BaseTransform:
        """
        Создает экземпляр преобразования по имени.
        
        Args:
            transform_name: Название преобразования
            
        Returns:
            BaseTransform: Экземпляр преобразования
            
        Raises:
            ValueError: Если преобразование не найдено
        """
        if transform_name not in cls._transforms:
            raise ValueError(f"Преобразование '{transform_name}' не найдено")
        
        transform_class = cls._transforms[transform_name]
        return transform_class()
    
    @classmethod
    def get_available_transforms(cls) -> list[str]:
        """
        Возвращает список доступных преобразований.
        
        Returns:
            list[str]: Список названий преобразований
        """
        return list(cls._transforms.keys())
    
    @classmethod
    def register_transform(cls, name: str, transform_class: Type[BaseTransform]) -> None:
        """
        Регистрирует новое преобразование.
        
        Args:
            name: Название преобразования
            transform_class: Класс преобразования
        """
        cls._transforms[name] = transform_class
        logger.info(f"Зарегистрировано преобразование: {name}")
    
    @classmethod
    def unregister_transform(cls, name: str) -> None:
        """
        Удаляет преобразование из реестра.
        
        Args:
            name: Название преобразования
        """
        if name in cls._transforms:
            del cls._transforms[name]
            logger.info(f"Удалено преобразование: {name}")
    
    @classmethod
    def is_transform_available(cls, name: str) -> bool:
        """
        Проверяет, доступно ли преобразование.
        
        Args:
            name: Название преобразования
            
        Returns:
            bool: True если преобразование доступно
        """
        return name in cls._transforms
