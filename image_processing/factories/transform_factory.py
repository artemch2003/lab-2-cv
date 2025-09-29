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
    MedianFilter3x3, MedianFilter5x5,
    GaussianFilterSigma1, GaussianFilterSigma2, GaussianFilterSigma3,
    SigmaFilterSigma1, SigmaFilterSigma2, SigmaFilterSigma3
)
from ..transforms.sharpness_filters import (
    UnsharpMasking3x3Lambda05, UnsharpMasking3x3Lambda10, UnsharpMasking3x3Lambda15, UnsharpMasking3x3Lambda20,
    UnsharpMasking5x5Lambda05, UnsharpMasking5x5Lambda10, UnsharpMasking5x5Lambda15, UnsharpMasking5x5Lambda20,
    UnsharpMasking7x7Lambda05, UnsharpMasking7x7Lambda10, UnsharpMasking7x7Lambda15, UnsharpMasking7x7Lambda20
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
        "Медианный фильтр 5x5": MedianFilter5x5,
        "Фильтр Гаусса σ=1.0": GaussianFilterSigma1,
        "Фильтр Гаусса σ=2.0": GaussianFilterSigma2,
        "Фильтр Гаусса σ=3.0": GaussianFilterSigma3,
        "Сигма-фильтр σ=1.0": SigmaFilterSigma1,
        "Сигма-фильтр σ=2.0": SigmaFilterSigma2,
        "Сигма-фильтр σ=3.0": SigmaFilterSigma3,
        # Фильтры резкости (нерезкое маскирование)
        "Нерезкое маскирование k=3, λ=0.5": UnsharpMasking3x3Lambda05,
        "Нерезкое маскирование k=3, λ=1.0": UnsharpMasking3x3Lambda10,
        "Нерезкое маскирование k=3, λ=1.5": UnsharpMasking3x3Lambda15,
        "Нерезкое маскирование k=3, λ=2.0": UnsharpMasking3x3Lambda20,
        "Нерезкое маскирование k=5, λ=0.5": UnsharpMasking5x5Lambda05,
        "Нерезкое маскирование k=5, λ=1.0": UnsharpMasking5x5Lambda10,
        "Нерезкое маскирование k=5, λ=1.5": UnsharpMasking5x5Lambda15,
        "Нерезкое маскирование k=5, λ=2.0": UnsharpMasking5x5Lambda20,
        "Нерезкое маскирование k=7, λ=0.5": UnsharpMasking7x7Lambda05,
        "Нерезкое маскирование k=7, λ=1.0": UnsharpMasking7x7Lambda10,
        "Нерезкое маскирование k=7, λ=1.5": UnsharpMasking7x7Lambda15,
        "Нерезкое маскирование k=7, λ=2.0": UnsharpMasking7x7Lambda20
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
