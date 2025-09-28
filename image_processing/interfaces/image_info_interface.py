"""
Интерфейс для получения информации об изображениях.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ImageInfoInterface(ABC):
    """Интерфейс для получения информации об изображениях."""
    
    @abstractmethod
    def get_image_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию об изображении.
        
        Returns:
            dict: Словарь с информацией об изображении
        """
        pass
