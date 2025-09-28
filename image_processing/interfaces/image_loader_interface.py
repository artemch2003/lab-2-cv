"""
Интерфейс для загрузки изображений.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional


class ImageLoaderInterface(ABC):
    """Интерфейс для загрузки изображений."""
    
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
    def has_original_image(self) -> bool:
        """
        Проверяет, загружено ли исходное изображение.
        
        Returns:
            bool: True если изображение загружено
        """
        pass
