"""
Интерфейс для сохранения изображений.
"""

from abc import ABC, abstractmethod


class ImageSaverInterface(ABC):
    """Интерфейс для сохранения изображений."""
    
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
    def has_processed_image(self) -> bool:
        """
        Проверяет, есть ли обработанное изображение.
        
        Returns:
            bool: True если есть обработанное изображение
        """
        pass
