"""
Интерфейс для процессора изображений.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple, Dict, Any
import numpy as np


class ImageProcessorInterface(ABC):
    """Интерфейс для процессора изображений."""
    
    @abstractmethod
    def load_image(self, file_path: str) -> bool:
        """
        Загружает изображение из файла.
        
        Args:
            file_path: Путь к файлу изображения
            
        Returns:
            bool: True если изображение успешно загружено, False иначе
        """
        pass
    
    @abstractmethod
    def save_image(self, file_path: str) -> bool:
        """
        Сохраняет обработанное изображение в файл.
        
        Args:
            file_path: Путь для сохранения файла
            
        Returns:
            bool: True если изображение успешно сохранено, False иначе
        """
        pass
    
    @abstractmethod
    def get_image_for_display(self, image, max_size: Tuple[int, int] = (400, 400)):
        """
        Подготавливает изображение для отображения в GUI.
        
        Args:
            image: Изображение для отображения
            max_size: Максимальный размер для отображения
            
        Returns:
            Изображение готовое для отображения в tkinter
        """
        pass
    
    @abstractmethod
    def apply_transform(self, transform_name: str, **kwargs) -> bool:
        """
        Применяет указанное преобразование к изображению.
        
        Args:
            transform_name: Название преобразования
            **kwargs: Параметры преобразования
            
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        pass
    
    @abstractmethod
    def apply_custom_transform(self, transform, **kwargs) -> bool:
        """
        Применяет пользовательское преобразование к изображению.
        
        Args:
            transform: Объект преобразования
            **kwargs: Параметры преобразования
            
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        pass
    
    @abstractmethod
    def get_image_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию об изображении.
        
        Returns:
            dict: Словарь с информацией об изображении
        """
        pass
    
    @property
    @abstractmethod
    def original_image(self):
        """Исходное изображение."""
        pass
    
    @property
    @abstractmethod
    def processed_image(self):
        """Обработанное изображение."""
        pass
    
    @property
    @abstractmethod
    def image_array(self):
        """Массив изображения."""
        pass
