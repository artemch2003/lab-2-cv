"""
Менеджер для работы с изображениями.
"""

from typing import Optional, Tuple
import numpy as np
from PIL import Image, ImageTk
import logging

logger = logging.getLogger(__name__)


class ImageManager:
    """Класс для управления изображениями."""
    
    def __init__(self):
        """Инициализация менеджера изображений."""
        self.original_image: Optional[Image.Image] = None
        self.processed_image: Optional[Image.Image] = None
        self.image_array: Optional[np.ndarray] = None
    
    def load_image(self, file_path: str) -> bool:
        """
        Загружает изображение из файла.
        
        Args:
            file_path: Путь к файлу изображения
            
        Returns:
            bool: True если изображение успешно загружено, False иначе
        """
        try:
            self.original_image = Image.open(file_path)
            self.image_array = np.array(self.original_image)
            logger.info(f"Изображение успешно загружено: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при загрузке изображения: {e}")
            return False
    
    def save_image(self, file_path: str) -> bool:
        """
        Сохраняет обработанное изображение в файл.
        
        Args:
            file_path: Путь для сохранения файла
            
        Returns:
            bool: True если изображение успешно сохранено, False иначе
        """
        try:
            if self.processed_image is None:
                logger.warning("Нет обработанного изображения для сохранения")
                return False
                
            self.processed_image.save(file_path)
            logger.info(f"Изображение успешно сохранено: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении изображения: {e}")
            return False
    
    def get_image_for_display(self, image: Image.Image, max_size: Tuple[int, int] = (400, 400)) -> Optional[ImageTk.PhotoImage]:
        """
        Подготавливает изображение для отображения в GUI.
        
        Args:
            image: Изображение для отображения
            max_size: Максимальный размер для отображения
            
        Returns:
            Optional[ImageTk.PhotoImage]: Изображение готовое для отображения в tkinter
        """
        try:
            # Изменяем размер изображения для отображения
            display_image = image.copy()
            display_image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            return ImageTk.PhotoImage(display_image)
        except Exception as e:
            logger.error(f"Ошибка при подготовке изображения для отображения: {e}")
            return None
    
    def set_processed_image(self, image_array: np.ndarray) -> None:
        """
        Устанавливает обработанное изображение из массива.
        
        Args:
            image_array: Массив обработанного изображения
        """
        try:
            self.processed_image = Image.fromarray(image_array)
            logger.info("Обработанное изображение установлено")
        except Exception as e:
            logger.error(f"Ошибка при установке обработанного изображения: {e}")
            raise
    
    def get_image_info(self) -> dict:
        """
        Возвращает информацию об изображении.
        
        Returns:
            dict: Словарь с информацией об изображении
        """
        if self.original_image is None:
            return {}
        
        return {
            'size': self.original_image.size,
            'mode': self.original_image.mode,
            'format': self.original_image.format,
            'has_processed': self.processed_image is not None
        }
    
    def has_original_image(self) -> bool:
        """Проверяет, загружено ли исходное изображение."""
        return self.original_image is not None
    
    def has_processed_image(self) -> bool:
        """Проверяет, есть ли обработанное изображение."""
        return self.processed_image is not None
    
    def clear_processed_image(self) -> None:
        """Очищает обработанное изображение."""
        self.processed_image = None
        logger.info("Обработанное изображение очищено")
