"""
Менеджер для управления преобразованиями изображений.
"""

from typing import Dict, Any, Optional, Type
import numpy as np
import logging

from .transforms.base_transform import BaseTransform
from .factories.transform_factory import TransformFactory

logger = logging.getLogger(__name__)


class TransformManager:
    """Класс для управления преобразованиями изображений."""
    
    def __init__(self):
        """Инициализация менеджера преобразований."""
        self.transforms: Dict[str, BaseTransform] = {}
        self.last_transform_name: Optional[str] = None
        self.last_parameters: Optional[Dict[str, Any]] = None
        
        # Инициализируем доступные преобразования
        for transform_name in TransformFactory.get_available_transforms():
            self.transforms[transform_name] = TransformFactory.create_transform(transform_name)
    
    def get_available_transforms(self) -> list[str]:
        """
        Возвращает список доступных преобразований.
        
        Returns:
            list[str]: Список названий преобразований
        """
        return TransformFactory.get_available_transforms()
    
    def apply_transform(self, transform_name: str, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет указанное преобразование к изображению.
        
        Args:
            transform_name: Название преобразования
            image_array: Массив изображения
            **kwargs: Параметры преобразования
            
        Returns:
            np.ndarray: Преобразованный массив изображения
            
        Raises:
            ValueError: Если преобразование не найдено или параметры невалидны
        """
        if transform_name not in self.transforms:
            raise ValueError(f"Преобразование '{transform_name}' не найдено")
        
        transform = self.transforms[transform_name]
        
        # Валидируем параметры
        if not transform.validate_parameters(**kwargs):
            raise ValueError(f"Невалидные параметры для преобразования '{transform_name}'")
        
        # Сохраняем информацию о последнем преобразовании
        self.last_transform_name = transform_name
        self.last_parameters = kwargs.copy()
        
        # Применяем преобразование
        return transform.apply(image_array, **kwargs)
    
    def get_optimal_parameters(self, transform_name: str, image_array: np.ndarray) -> Dict[str, Any]:
        """
        Получает оптимальные параметры для преобразования.
        
        Args:
            transform_name: Название преобразования
            image_array: Массив изображения
            
        Returns:
            Dict[str, Any]: Словарь с оптимальными параметрами
            
        Raises:
            ValueError: Если преобразование не найдено
        """
        if transform_name not in self.transforms:
            raise ValueError(f"Преобразование '{transform_name}' не найдено")
        
        transform = self.transforms[transform_name]
        return transform.get_optimal_parameters(image_array)
    
    def get_last_transform_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию о последнем примененном преобразовании.
        
        Returns:
            Dict[str, Any]: Информация о последнем преобразовании
        """
        info = {}
        
        if self.last_transform_name:
            info['transform_name'] = self.last_transform_name
            info['parameters'] = self.last_parameters
            
            # Получаем детальную информацию от самого преобразования
            transform = self.transforms[self.last_transform_name]
            last_params = transform.get_last_parameters()
            if last_params:
                info['detailed_parameters'] = last_params
        
        return info
    
    def register_transform(self, name: str, transform_class: Type[BaseTransform]) -> None:
        """
        Регистрирует новое преобразование.
        
        Args:
            name: Название преобразования
            transform_class: Класс преобразования
        """
        TransformFactory.register_transform(name, transform_class)
        self.transforms[name] = TransformFactory.create_transform(name)
        logger.info(f"Зарегистрировано преобразование: {name}")
    
    def get_transform_info(self, transform_name: str) -> Dict[str, Any]:
        """
        Возвращает информацию о преобразовании.
        
        Args:
            transform_name: Название преобразования
            
        Returns:
            Dict[str, Any]: Информация о преобразовании
            
        Raises:
            ValueError: Если преобразование не найдено
        """
        if transform_name not in self.transforms:
            raise ValueError(f"Преобразование '{transform_name}' не найдено")
        
        transform = self.transforms[transform_name]
        return {
            'name': transform.get_name(),
            'last_parameters': transform.get_last_parameters()
        }
