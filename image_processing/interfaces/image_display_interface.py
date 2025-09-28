"""
Интерфейс для отображения изображений.
"""

from abc import ABC, abstractmethod
from typing import Tuple, Optional


class ImageDisplayInterface(ABC):
    """Интерфейс для отображения изображений."""
    
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
