"""
Фильтры сглаживания для обработки зашумленных изображений.
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_transform import BaseTransform
import logging

logger = logging.getLogger(__name__)


class SmoothingFilter(BaseTransform):
    """Базовый класс для фильтров сглаживания."""
    
    def __init__(self, kernel_size: int = 3):
        """
        Инициализация фильтра сглаживания.
        
        Args:
            kernel_size: Размер ядра фильтра (3 или 5)
        """
        super().__init__()
        self.kernel_size = kernel_size
        self._validate_kernel_size()
    
    def _validate_kernel_size(self):
        """Валидирует размер ядра."""
        if self.kernel_size not in [3, 5]:
            raise ValueError("Размер ядра должен быть 3 или 5")
    
    def _apply_padding(self, image: np.ndarray) -> np.ndarray:
        """
        Применяет padding к изображению для корректной обработки краев.
        
        Args:
            image: Исходное изображение
            
        Returns:
            np.ndarray: Изображение с padding
        """
        pad_size = self.kernel_size // 2
        if len(image.shape) == 3:
            # Цветное изображение
            return np.pad(image, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode='edge')
        else:
            # Оттенки серого
            return np.pad(image, pad_size, mode='edge')
    
    def _remove_padding(self, image: np.ndarray) -> np.ndarray:
        """
        Удаляет padding с изображения.
        
        Args:
            image: Изображение с padding
            
        Returns:
            np.ndarray: Изображение без padding
        """
        pad_size = self.kernel_size // 2
        if len(image.shape) == 3:
            return image[pad_size:-pad_size, pad_size:-pad_size, :]
        else:
            return image[pad_size:-pad_size, pad_size:-pad_size]
    
    def validate_parameters(self, **kwargs) -> bool:
        """Валидирует параметры фильтра."""
        kernel_size = kwargs.get('kernel_size', self.kernel_size)
        return kernel_size in [3, 5]


class RectangularFilter(SmoothingFilter):
    """Прямоугольный фильтр сглаживания."""
    
    def __init__(self, kernel_size: int = 3):
        """
        Инициализация прямоугольного фильтра.
        
        Args:
            kernel_size: Размер ядра (3 или 5)
        """
        super().__init__(kernel_size)
        self._create_kernel()
    
    def _create_kernel(self):
        """Создает ядро прямоугольного фильтра."""
        kernel_value = 1.0 / (self.kernel_size * self.kernel_size)
        self.kernel = np.full((self.kernel_size, self.kernel_size), kernel_value)
    
    def apply(self, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет прямоугольный фильтр к изображению.
        
        Args:
            image_array: Массив изображения
            **kwargs: Дополнительные параметры (kernel_size)
            
        Returns:
            np.ndarray: Отфильтрованное изображение
        """
        # Обновляем размер ядра если указан
        if 'kernel_size' in kwargs:
            self.kernel_size = kwargs['kernel_size']
            self._validate_kernel_size()
            self._create_kernel()
        
        # Применяем padding
        padded_image = self._apply_padding(image_array)
        
        # Применяем фильтр
        filtered_image = self._apply_convolution(padded_image)
        
        # Удаляем padding
        result = self._remove_padding(filtered_image)
        
        # Обеспечиваем корректный тип данных
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _apply_convolution(self, image: np.ndarray) -> np.ndarray:
        """
        Применяет свертку с ядром фильтра.
        
        Args:
            image: Изображение с padding
            
        Returns:
            np.ndarray: Результат свертки
        """
        if len(image.shape) == 3:
            # Цветное изображение
            result = np.zeros_like(image)
            for channel in range(image.shape[2]):
                result[:, :, channel] = self._convolve_2d(image[:, :, channel])
            return result
        else:
            # Оттенки серого
            return self._convolve_2d(image)
    
    def _convolve_2d(self, image: np.ndarray) -> np.ndarray:
        """
        Выполняет 2D свертку для одного канала.
        
        Args:
            image: 2D массив изображения
            
        Returns:
            np.ndarray: Результат свертки
        """
        result = np.zeros_like(image, dtype=np.float64)
        pad_size = self.kernel_size // 2
        
        for i in range(pad_size, image.shape[0] - pad_size):
            for j in range(pad_size, image.shape[1] - pad_size):
                # Извлекаем окно
                window = image[i-pad_size:i+pad_size+1, j-pad_size:j+pad_size+1]
                # Применяем свертку
                result[i, j] = np.sum(window * self.kernel)
        
        return result
    
    def get_name(self) -> str:
        """Возвращает название фильтра."""
        return f"Прямоугольный фильтр {self.kernel_size}x{self.kernel_size}"


class MedianFilter(SmoothingFilter):
    """Медианный фильтр сглаживания."""
    
    def __init__(self, kernel_size: int = 3):
        """
        Инициализация медианного фильтра.
        
        Args:
            kernel_size: Размер ядра (3 или 5)
        """
        super().__init__(kernel_size)
    
    def apply(self, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет медианный фильтр к изображению.
        
        Args:
            image_array: Массив изображения
            **kwargs: Дополнительные параметры (kernel_size)
            
        Returns:
            np.ndarray: Отфильтрованное изображение
        """
        # Обновляем размер ядра если указан
        if 'kernel_size' in kwargs:
            self.kernel_size = kwargs['kernel_size']
            self._validate_kernel_size()
        
        # Применяем padding
        padded_image = self._apply_padding(image_array)
        
        # Применяем медианный фильтр
        filtered_image = self._apply_median_filter(padded_image)
        
        # Удаляем padding
        result = self._remove_padding(filtered_image)
        
        # Обеспечиваем корректный тип данных
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _apply_median_filter(self, image: np.ndarray) -> np.ndarray:
        """
        Применяет медианный фильтр.
        
        Args:
            image: Изображение с padding
            
        Returns:
            np.ndarray: Результат медианной фильтрации
        """
        if len(image.shape) == 3:
            # Цветное изображение
            result = np.zeros_like(image)
            for channel in range(image.shape[2]):
                result[:, :, channel] = self._median_filter_2d(image[:, :, channel])
            return result
        else:
            # Оттенки серого
            return self._median_filter_2d(image)
    
    def _median_filter_2d(self, image: np.ndarray) -> np.ndarray:
        """
        Выполняет медианную фильтрацию для одного канала.
        
        Args:
            image: 2D массив изображения
            
        Returns:
            np.ndarray: Результат медианной фильтрации
        """
        result = np.zeros_like(image, dtype=np.float64)
        pad_size = self.kernel_size // 2
        
        for i in range(pad_size, image.shape[0] - pad_size):
            for j in range(pad_size, image.shape[1] - pad_size):
                # Извлекаем окно
                window = image[i-pad_size:i+pad_size+1, j-pad_size:j+pad_size+1]
                # Вычисляем медиану
                result[i, j] = np.median(window)
        
        return result
    
    def get_name(self) -> str:
        """Возвращает название фильтра."""
        return f"Медианный фильтр {self.kernel_size}x{self.kernel_size}"


class RectangularFilter3x3(RectangularFilter):
    """Прямоугольный фильтр 3x3."""
    
    def __init__(self):
        super().__init__(3)
    
    def get_name(self) -> str:
        return "Прямоугольный фильтр 3x3"


class RectangularFilter5x5(RectangularFilter):
    """Прямоугольный фильтр 5x5."""
    
    def __init__(self):
        super().__init__(5)
    
    def get_name(self) -> str:
        return "Прямоугольный фильтр 5x5"


class MedianFilter3x3(MedianFilter):
    """Медианный фильтр 3x3."""
    
    def __init__(self):
        super().__init__(3)
    
    def get_name(self) -> str:
        return "Медианный фильтр 3x3"


class MedianFilter5x5(MedianFilter):
    """Медианный фильтр 5x5."""
    
    def __init__(self):
        super().__init__(5)
    
    def get_name(self) -> str:
        return "Медианный фильтр 5x5"
