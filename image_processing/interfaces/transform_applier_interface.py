"""
Интерфейс для применения преобразований.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class TransformApplierInterface(ABC):
    """Интерфейс для применения преобразований."""
    
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
    def get_available_transforms(self) -> list[str]:
        """
        Возвращает список доступных преобразований.
        
        Returns:
            list[str]: Список названий преобразований
        """
        pass
