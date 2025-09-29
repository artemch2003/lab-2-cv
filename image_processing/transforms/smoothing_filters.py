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
            # Для фильтра Гаусса разрешаем большие размеры ядра
            if hasattr(self, 'sigma') and self.kernel_size > 0:
                pass  # Размер ядра вычисляется по правилу 3σ
            else:
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


class GaussianFilter(SmoothingFilter):
    """Фильтр Гаусса с ядром по правилу 3σ."""
    
    def __init__(self, sigma: float = 1.0):
        """
        Инициализация фильтра Гаусса.
        
        Args:
            sigma: Стандартное отклонение для фильтра Гаусса
        """
        # Вычисляем размер ядра по правилу 3σ
        kernel_size = int(2 * 3 * sigma) + 1
        # Обеспечиваем нечетный размер ядра
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        super().__init__(kernel_size)
        self.sigma = sigma
        self._create_gaussian_kernel()
    
    def _validate_kernel_size(self):
        """Валидирует размер ядра для фильтра Гаусса."""
        # Для фильтра Гаусса размер ядра может быть любым положительным числом
        if self.kernel_size <= 0:
            raise ValueError("Размер ядра должен быть положительным")
    
    def _create_gaussian_kernel(self):
        """Создает ядро фильтра Гаусса."""
        center = self.kernel_size // 2
        kernel = np.zeros((self.kernel_size, self.kernel_size), dtype=np.float64)
        
        # Вычисляем значения ядра по формуле Гаусса
        for i in range(self.kernel_size):
            for j in range(self.kernel_size):
                x = i - center
                y = j - center
                # Формула 2D Гаусса: G(x,y) = (1/(2πσ²)) * exp(-(x²+y²)/(2σ²))
                exponent = -(x*x + y*y) / (2 * self.sigma * self.sigma)
                kernel[i, j] = np.exp(exponent)
        
        # Нормализуем ядро, чтобы сумма была равна 1
        kernel_sum = np.sum(kernel)
        if kernel_sum > 0:
            self.kernel = kernel / kernel_sum
        else:
            # Если сумма равна 0, создаем единичное ядро
            self.kernel = np.ones((self.kernel_size, self.kernel_size)) / (self.kernel_size * self.kernel_size)
    
    def apply(self, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет фильтр Гаусса к изображению.
        
        Args:
            image_array: Массив изображения
            **kwargs: Дополнительные параметры (sigma)
            
        Returns:
            np.ndarray: Отфильтрованное изображение
        """
        # Обновляем параметры если указаны
        if 'sigma' in kwargs:
            self.sigma = kwargs['sigma']
            # Пересчитываем размер ядра и ядро
            kernel_size = int(2 * 3 * self.sigma) + 1
            if kernel_size % 2 == 0:
                kernel_size += 1
            self.kernel_size = kernel_size
            self._create_gaussian_kernel()
        
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
        Применяет свертку с ядром фильтра Гаусса.
        
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
        return f"Фильтр Гаусса σ={self.sigma:.1f}"
    
    def get_kernel_size(self) -> int:
        """Возвращает размер ядра."""
        return self.kernel_size
    
    def get_sigma(self) -> float:
        """Возвращает значение σ."""
        return self.sigma


class GaussianFilterSigma1(GaussianFilter):
    """Фильтр Гаусса с σ=1.0."""
    
    def __init__(self):
        super().__init__(1.0)
    
    def get_name(self) -> str:
        return "Фильтр Гаусса σ=1.0"


class GaussianFilterSigma2(GaussianFilter):
    """Фильтр Гаусса с σ=2.0."""
    
    def __init__(self):
        super().__init__(2.0)
    
    def get_name(self) -> str:
        return "Фильтр Гаусса σ=2.0"


class GaussianFilterSigma3(GaussianFilter):
    """Фильтр Гаусса с σ=3.0."""
    
    def __init__(self):
        super().__init__(3.0)
    
    def get_name(self) -> str:
        return "Фильтр Гаусса σ=3.0"


class SigmaFilter(SmoothingFilter):
    """Сигма-фильтр для удаления шума."""
    
    def __init__(self, sigma: float = 1.0, kernel_size: int = 5):
        """
        Инициализация сигма-фильтра.
        
        Args:
            sigma: Коэффициент для определения порога отклонения
            kernel_size: Размер окна для анализа (по умолчанию 5x5)
        """
        super().__init__(kernel_size)
        self.sigma = sigma
    
    def _validate_kernel_size(self):
        """Валидирует размер ядра для сигма-фильтра."""
        # Для сигма-фильтра размер ядра может быть любым положительным числом
        if self.kernel_size <= 0:
            raise ValueError("Размер ядра должен быть положительным")
    
    def apply(self, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет сигма-фильтр к изображению.
        
        Args:
            image_array: Массив изображения
            **kwargs: Дополнительные параметры (sigma, kernel_size)
            
        Returns:
            np.ndarray: Отфильтрованное изображение
        """
        # Обновляем параметры если указаны
        if 'sigma' in kwargs:
            self.sigma = kwargs['sigma']
        if 'kernel_size' in kwargs:
            self.kernel_size = kwargs['kernel_size']
            self._validate_kernel_size()
        
        # Применяем padding
        padded_image = self._apply_padding(image_array)
        
        # Применяем сигма-фильтр
        filtered_image = self._apply_sigma_filter(padded_image)
        
        # Удаляем padding
        result = self._remove_padding(filtered_image)
        
        # Обеспечиваем корректный тип данных
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _apply_sigma_filter(self, image: np.ndarray) -> np.ndarray:
        """
        Применяет сигма-фильтр.
        
        Args:
            image: Изображение с padding
            
        Returns:
            np.ndarray: Результат сигма-фильтрации
        """
        if len(image.shape) == 3:
            # Цветное изображение
            result = np.zeros_like(image)
            for channel in range(image.shape[2]):
                result[:, :, channel] = self._sigma_filter_2d(image[:, :, channel])
            return result
        else:
            # Оттенки серого
            return self._sigma_filter_2d(image)
    
    def _sigma_filter_2d(self, image: np.ndarray) -> np.ndarray:
        """
        Выполняет сигма-фильтрацию для одного канала.
        
        Args:
            image: 2D массив изображения
            
        Returns:
            np.ndarray: Результат сигма-фильтрации
        """
        result = np.zeros_like(image, dtype=np.float64)
        pad_size = self.kernel_size // 2
        
        for i in range(pad_size, image.shape[0] - pad_size):
            for j in range(pad_size, image.shape[1] - pad_size):
                # Извлекаем окно
                window = image[i-pad_size:i+pad_size+1, j-pad_size:j+pad_size+1]
                
                # Вычисляем среднее значение в окне
                mean_value = np.mean(window)
                
                # Вычисляем стандартное отклонение в окне
                std_value = np.std(window)
                
                # Определяем порог отклонения
                threshold = self.sigma * std_value
                
                # Фильтруем пиксели: оставляем только те, что близки к среднему
                filtered_pixels = []
                for pixel in window.flatten():
                    if abs(pixel - mean_value) <= threshold:
                        filtered_pixels.append(pixel)
                
                # Если есть отфильтрованные пиксели, берем их среднее
                if filtered_pixels:
                    result[i, j] = np.mean(filtered_pixels)
                else:
                    # Если все пиксели отклоняются, берем среднее всего окна
                    result[i, j] = mean_value
        
        return result
    
    def get_name(self) -> str:
        """Возвращает название фильтра."""
        return f"Сигма-фильтр σ={self.sigma:.1f}"
    
    def get_sigma(self) -> float:
        """Возвращает значение σ."""
        return self.sigma


class SigmaFilterSigma1(SigmaFilter):
    """Сигма-фильтр с σ=1.0."""
    
    def __init__(self):
        super().__init__(1.0, 5)
    
    def get_name(self) -> str:
        return "Сигма-фильтр σ=1.0"


class SigmaFilterSigma2(SigmaFilter):
    """Сигма-фильтр с σ=2.0."""
    
    def __init__(self):
        super().__init__(2.0, 5)
    
    def get_name(self) -> str:
        return "Сигма-фильтр σ=2.0"


class SigmaFilterSigma3(SigmaFilter):
    """Сигма-фильтр с σ=3.0."""
    
    def __init__(self):
        super().__init__(3.0, 5)
    
    def get_name(self) -> str:
        return "Сигма-фильтр σ=3.0"
