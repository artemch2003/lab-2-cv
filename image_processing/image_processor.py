"""
Модуль для обработки изображений.
Содержит класс ImageProcessor для работы с изображениями.
"""

from typing import Tuple, Optional
import logging

from .image_manager import ImageManager
from .transform_manager import TransformManager

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Класс для обработки изображений."""
    
    def __init__(self):
        """Инициализация процессора изображений."""
        self.image_manager = ImageManager()
        self.transform_manager = TransformManager()
    
    def load_image(self, file_path: str) -> bool:
        """
        Загружает изображение из файла.
        
        Args:
            file_path: Путь к файлу изображения
            
        Returns:
            bool: True если изображение успешно загружено, False иначе
        """
        return self.image_manager.load_image(file_path)
    
    def save_image(self, file_path: str) -> bool:
        """
        Сохраняет обработанное изображение в файл.
        
        Args:
            file_path: Путь для сохранения файла
            
        Returns:
            bool: True если изображение успешно сохранено, False иначе
        """
        return self.image_manager.save_image(file_path)
    
    def get_image_for_display(self, image, max_size: Tuple[int, int] = (400, 400)):
        """
        Подготавливает изображение для отображения в GUI.
        
        Args:
            image: Изображение для отображения
            max_size: Максимальный размер для отображения
            
        Returns:
            ImageTk.PhotoImage: Изображение готовое для отображения в tkinter
        """
        return self.image_manager.get_image_for_display(image, max_size)
    
    def apply_logarithmic_transform(self, c: Optional[float] = None) -> bool:
        """
        Применяет логарифмическое преобразование к изображению.
        
        Args:
            c: Коэффициент для логарифмического преобразования.
               Если None, то коэффициент будет вычислен автоматически.
               
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        try:
            if not self.image_manager.has_original_image():
                logger.error("Изображение не загружено")
                return False
            
            # Применяем преобразование
            processed_array = self.transform_manager.apply_transform(
                "Логарифмическое", 
                self.image_manager.image_array, 
                c=c
            )
            
            # Устанавливаем обработанное изображение
            self.image_manager.set_processed_image(processed_array)
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении логарифмического преобразования: {e}")
            return False
    
    def apply_power_transform(self, gamma: float, c: Optional[float] = None) -> bool:
        """
        Применяет степенное преобразование к изображению.
        
        Args:
            gamma: Значение гаммы для степенного преобразования
            c: Коэффициент для степенного преобразования.
               Если None, то коэффициент будет вычислен автоматически.
               
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        try:
            if not self.image_manager.has_original_image():
                logger.error("Изображение не загружено")
                return False
            
            # Применяем преобразование
            processed_array = self.transform_manager.apply_transform(
                "Степенное", 
                self.image_manager.image_array, 
                gamma=gamma, c=c
            )
            
            # Устанавливаем обработанное изображение
            self.image_manager.set_processed_image(processed_array)
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении степенного преобразования: {e}")
            return False
    
    def apply_binary_transform(self, threshold: float) -> bool:
        """
        Применяет бинарное преобразование к изображению.
        
        Args:
            threshold: Пороговое значение для бинарного преобразования (0-255)
            
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        try:
            if not self.image_manager.has_original_image():
                logger.error("Изображение не загружено")
                return False
            
            # Применяем преобразование
            processed_array = self.transform_manager.apply_transform(
                "Бинарное", 
                self.image_manager.image_array, 
                threshold=threshold
            )
            
            # Устанавливаем обработанное изображение
            self.image_manager.set_processed_image(processed_array)
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении бинарного преобразования: {e}")
            return False
    
    def apply_brightness_range_transform(self, min_brightness: float, max_brightness: float, 
                                       outside_mode: str, constant_value: Optional[float] = None) -> bool:
        """
        Применяет вырезание диапазона яркостей к изображению.
        
        Args:
            min_brightness: Минимальная яркость диапазона (0-255)
            max_brightness: Максимальная яркость диапазона (0-255)
            outside_mode: Режим обработки пикселей вне диапазона ("Константа" или "Исходное")
            constant_value: Константное значение для пикселей вне диапазона (если режим "Константа")
            
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        try:
            if not self.image_manager.has_original_image():
                logger.error("Изображение не загружено")
                return False
            
            # Применяем преобразование
            processed_array = self.transform_manager.apply_transform(
                "Вырезание диапазона яркостей", 
                self.image_manager.image_array, 
                min_brightness=min_brightness,
                max_brightness=max_brightness,
                outside_mode=outside_mode,
                constant_value=constant_value
            )
            
            # Устанавливаем обработанное изображение
            self.image_manager.set_processed_image(processed_array)
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении вырезания диапазона яркостей: {e}")
            return False
    
    def apply_transform(self, transform_name: str, **kwargs) -> bool:
        """
        Применяет указанное преобразование к изображению.
        
        Args:
            transform_name: Название преобразования
            **kwargs: Параметры преобразования
            
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        try:
            if not self.image_manager.has_original_image():
                logger.error("Изображение не загружено")
                return False
            
            # Применяем преобразование
            processed_array = self.transform_manager.apply_transform(
                transform_name, 
                self.image_manager.image_array, 
                **kwargs
            )
            
            # Устанавливаем обработанное изображение
            self.image_manager.set_processed_image(processed_array)
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении преобразования {transform_name}: {e}")
            return False
    
    def apply_custom_transform(self, transform, **kwargs) -> bool:
        """
        Применяет пользовательское преобразование к изображению.
        
        Args:
            transform: Объект преобразования
            **kwargs: Параметры преобразования
            
        Returns:
            bool: True если преобразование успешно применено, False иначе
        """
        try:
            if not self.image_manager.has_original_image():
                logger.error("Изображение не загружено")
                return False
            
            # Применяем пользовательское преобразование
            processed_array = transform.apply(self.image_manager.image_array, **kwargs)
            
            # Устанавливаем обработанное изображение
            self.image_manager.set_processed_image(processed_array)
            
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении пользовательского преобразования: {e}")
            return False
    
    def get_image_info(self) -> dict:
        """
        Возвращает информацию об изображении.
        
        Returns:
            dict: Словарь с информацией об изображении
        """
        info = self.image_manager.get_image_info()
        
        # Добавляем информацию о последнем преобразовании
        transform_info = self.transform_manager.get_last_transform_info()
        if transform_info:
            info.update(transform_info)
        
        return info
    
    # Свойства для обратной совместимости
    @property
    def original_image(self):
        """Исходное изображение."""
        return self.image_manager.original_image
    
    @property
    def processed_image(self):
        """Обработанное изображение."""
        return self.image_manager.processed_image
    
    @property
    def image_array(self):
        """Массив изображения."""
        return self.image_manager.image_array