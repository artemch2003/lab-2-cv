"""
Модуль для обработки изображений.
Содержит класс ImageProcessor для работы с изображениями.
"""

import math
import numpy as np
from typing import Tuple, Optional
from PIL import Image, ImageTk
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Класс для обработки изображений."""
    
    def __init__(self):
        """Инициализация процессора изображений."""
        self.original_image: Optional[Image.Image] = None
        self.processed_image: Optional[Image.Image] = None
        self.image_array: Optional[np.ndarray] = None
        self.last_used_c: Optional[float] = None  # Последний использованный коэффициент
        self.last_used_gamma: Optional[float] = None  # Последнее использованное значение гаммы
        
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
    
    def get_image_for_display(self, image: Image.Image, max_size: Tuple[int, int] = (400, 400)) -> ImageTk.PhotoImage:
        """
        Подготавливает изображение для отображения в GUI.
        
        Args:
            image: Изображение для отображения
            max_size: Максимальный размер для отображения
            
        Returns:
            ImageTk.PhotoImage: Изображение готовое для отображения в tkinter
        """
        try:
            # Изменяем размер изображения для отображения
            display_image = image.copy()
            display_image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            return ImageTk.PhotoImage(display_image)
        except Exception as e:
            logger.error(f"Ошибка при подготовке изображения для отображения: {e}")
            return None
    
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
            if self.image_array is None:
                logger.error("Изображение не загружено")
                return False
            
            # Конвертируем в float для точных вычислений
            image_float = self.image_array.astype(np.float64)
            
            # Нормализуем значения в диапазон [0, 1]
            if image_float.max() > 1.0:
                image_float = image_float / 255.0
            
            # Вычисляем коэффициент c если не задан
            if c is None:
                c = self._calculate_optimal_c(image_float)
            
            # Сохраняем использованный коэффициент
            self.last_used_c = c
            
            logger.info(f"Применение логарифмического преобразования с коэффициентом c = {c}")
            
            # Применяем логарифмическое преобразование
            # Формула: s = c * log(1 + r), где r - исходное значение, s - результат
            processed_array = c * np.log(1 + image_float)
            
            # Нормализуем результат обратно в диапазон [0, 255]
            processed_array = np.clip(processed_array * 255, 0, 255)
            processed_array = processed_array.astype(np.uint8)
            
            # Создаем новое изображение
            self.processed_image = Image.fromarray(processed_array)
            
            logger.info("Логарифмическое преобразование успешно применено")
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
            if self.image_array is None:
                logger.error("Изображение не загружено")
                return False
            
            # Конвертируем в float для точных вычислений
            image_float = self.image_array.astype(np.float64)
            
            # Нормализуем значения в диапазон [0, 1]
            if image_float.max() > 1.0:
                image_float = image_float / 255.0
            
            # Вычисляем коэффициент c если не задан
            if c is None:
                c = self._calculate_optimal_c_power(image_float, gamma)
            
            # Сохраняем использованные параметры
            self.last_used_c = c
            self.last_used_gamma = gamma
            
            logger.info(f"Применение степенного преобразования с гаммой γ = {gamma} и коэффициентом c = {c}")
            
            # Применяем степенное преобразование
            # Формула: s = c * r^γ, где r - исходное значение, s - результат, γ - гамма
            processed_array = c * np.power(image_float, gamma)
            
            # Нормализуем результат обратно в диапазон [0, 255]
            processed_array = np.clip(processed_array * 255, 0, 255)
            processed_array = processed_array.astype(np.uint8)
            
            # Создаем новое изображение
            self.processed_image = Image.fromarray(processed_array)
            
            logger.info("Степенное преобразование успешно применено")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка при применении степенного преобразования: {e}")
            return False
    
    def _calculate_optimal_c(self, image_array: np.ndarray) -> float:
        """
        Вычисляет оптимальный коэффициент c для логарифмического преобразования.
        
        Args:
            image_array: Массив изображения в формате float [0, 1]
            
        Returns:
            float: Оптимальный коэффициент c
        """
        try:
            # Находим максимальное значение в изображении
            max_value = np.max(image_array)
            
            # Вычисляем коэффициент c так, чтобы максимальное значение
            # после преобразования было равно 1.0
            # c * log(1 + max_value) = 1.0
            # c = 1.0 / log(1 + max_value)
            c = 1.0 / math.log(1 + max_value)
            
            logger.info(f"Вычислен оптимальный коэффициент c = {c}")
            return c
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении коэффициента c: {e}")
            # Возвращаем значение по умолчанию
            return 1.0
    
    def _calculate_optimal_c_power(self, image_array: np.ndarray, gamma: float) -> float:
        """
        Вычисляет оптимальный коэффициент c для степенного преобразования.
        
        Args:
            image_array: Массив изображения в формате float [0, 1]
            gamma: Значение гаммы для степенного преобразования
            
        Returns:
            float: Оптимальный коэффициент c
        """
        try:
            # Находим максимальное значение в изображении
            max_value = np.max(image_array)
            
            # Вычисляем коэффициент c так, чтобы максимальное значение
            # после преобразования было равно 1.0
            # c * max_value^γ = 1.0
            # c = 1.0 / (max_value^γ)
            c = 1.0 / (max_value ** gamma)
            
            logger.info(f"Вычислен оптимальный коэффициент c = {c} для гаммы γ = {gamma}")
            return c
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении коэффициента c для степенного преобразования: {e}")
            # Возвращаем значение по умолчанию
            return 1.0
    
    def get_image_info(self) -> dict:
        """
        Возвращает информацию об изображении.
        
        Returns:
            dict: Словарь с информацией об изображении
        """
        if self.original_image is None:
            return {}
        
        info = {
            'size': self.original_image.size,
            'mode': self.original_image.mode,
            'format': self.original_image.format,
            'has_processed': self.processed_image is not None
        }
        
        # Добавляем информацию о коэффициенте, если он был использован
        if self.last_used_c is not None:
            info['last_coefficient_c'] = round(self.last_used_c, 4)
        
        # Добавляем информацию о гамме, если она была использована
        if self.last_used_gamma is not None:
            info['last_gamma'] = round(self.last_used_gamma, 4)
        
        return info
