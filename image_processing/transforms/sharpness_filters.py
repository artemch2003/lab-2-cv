"""
Фильтры резкости для повышения четкости изображений.
"""

import numpy as np
from typing import Dict, Any, Tuple
from .base_transform import BaseTransform
from .smoothing_filters import GaussianFilter
import logging

logger = logging.getLogger(__name__)


class SharpnessFilter(BaseTransform):
    """Базовый класс для фильтров резкости."""
    
    def __init__(self, kernel_size: int = 3, lambda_coeff: float = 1.0):
        """
        Инициализация фильтра резкости.
        
        Args:
            kernel_size: Размер ядра фильтра (k)
            lambda_coeff: Коэффициент усиления резкости (λ)
        """
        super().__init__()
        self.kernel_size = kernel_size
        self.lambda_coeff = lambda_coeff
        self._validate_parameters()
    
    def _validate_parameters(self):
        """Валидирует параметры фильтра."""
        if self.kernel_size <= 0:
            raise ValueError("Размер ядра должен быть положительным")
        if self.lambda_coeff < 0:
            raise ValueError("Коэффициент λ должен быть неотрицательным")
    
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
        lambda_coeff = kwargs.get('lambda_coeff', self.lambda_coeff)
        return kernel_size > 0 and lambda_coeff >= 0


class UnsharpMasking(SharpnessFilter):
    """Фильтр нерезкого маскирования для повышения резкости."""
    
    def __init__(self, kernel_size: int = 3, lambda_coeff: float = 1.0, sigma: float = 1.0):
        """
        Инициализация фильтра нерезкого маскирования.
        
        Args:
            kernel_size: Размер ядра фильтра (k)
            lambda_coeff: Коэффициент усиления резкости (λ)
            sigma: Стандартное отклонение для фильтра Гаусса
        """
        super().__init__(kernel_size, lambda_coeff)
        self.sigma = sigma
        self._create_gaussian_kernel()
    
    def _create_gaussian_kernel(self):
        """Создает ядро фильтра Гаусса для размытия."""
        # Вычисляем размер ядра по правилу 3σ
        kernel_size = int(2 * 3 * self.sigma) + 1
        # Обеспечиваем нечетный размер ядра
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        center = kernel_size // 2
        kernel = np.zeros((kernel_size, kernel_size), dtype=np.float64)
        
        # Вычисляем значения ядра по формуле Гаусса
        for i in range(kernel_size):
            for j in range(kernel_size):
                x = i - center
                y = j - center
                # Формула 2D Гаусса: G(x,y) = (1/(2πσ²)) * exp(-(x²+y²)/(2σ²))
                exponent = -(x*x + y*y) / (2 * self.sigma * self.sigma)
                kernel[i, j] = np.exp(exponent)
        
        # Нормализуем ядро, чтобы сумма была равна 1
        kernel_sum = np.sum(kernel)
        if kernel_sum > 0:
            self.blur_kernel = kernel / kernel_sum
        else:
            # Если сумма равна 0, создаем единичное ядро
            self.blur_kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
    
    def apply(self, image_array: np.ndarray, **kwargs) -> np.ndarray:
        """
        Применяет нерезкое маскирование к изображению.
        
        Алгоритм нерезкого маскирования:
        1. Создаем размытую версию изображения (I_blurred)
        2. Вычисляем маску: mask = I_original - I_blurred
        3. Применяем усиление: I_sharp = I_original + λ * mask
        
        Args:
            image_array: Массив изображения
            **kwargs: Дополнительные параметры (kernel_size, lambda_coeff, sigma)
            
        Returns:
            np.ndarray: Изображение с повышенной резкостью
        """
        # Обновляем параметры если указаны
        if 'kernel_size' in kwargs:
            self.kernel_size = kwargs['kernel_size']
            self._validate_parameters()
        if 'lambda_coeff' in kwargs:
            self.lambda_coeff = kwargs['lambda_coeff']
            self._validate_parameters()
        if 'sigma' in kwargs:
            self.sigma = kwargs['sigma']
            self._create_gaussian_kernel()
        
        # Применяем padding
        padded_image = self._apply_padding(image_array)
        
        # Применяем нерезкое маскирование
        sharpened_image = self._apply_unsharp_masking(padded_image)
        
        # Удаляем padding
        result = self._remove_padding(sharpened_image)
        
        # Обеспечиваем корректный тип данных
        return np.clip(result, 0, 255).astype(np.uint8)
    
    def _apply_unsharp_masking(self, image: np.ndarray) -> np.ndarray:
        """
        Применяет алгоритм нерезкого маскирования.
        
        Args:
            image: Изображение с padding
            
        Returns:
            np.ndarray: Результат нерезкого маскирования
        """
        if len(image.shape) == 3:
            # Цветное изображение
            result = np.zeros_like(image)
            for channel in range(image.shape[2]):
                result[:, :, channel] = self._unsharp_masking_2d(image[:, :, channel])
            return result
        else:
            # Оттенки серого
            return self._unsharp_masking_2d(image)
    
    def _unsharp_masking_2d(self, image: np.ndarray) -> np.ndarray:
        """
        Выполняет нерезкое маскирование для одного канала.
        
        Args:
            image: 2D массив изображения
            
        Returns:
            np.ndarray: Результат нерезкого маскирования
        """
        # Шаг 1: Создаем размытую версию изображения
        blurred = self._apply_gaussian_blur(image)
        
        # Шаг 2: Вычисляем маску (разность между оригиналом и размытым)
        mask = image.astype(np.float64) - blurred.astype(np.float64)
        
        # Шаг 3: Применяем усиление резкости
        sharpened = image.astype(np.float64) + self.lambda_coeff * mask
        
        return sharpened
    
    def _apply_gaussian_blur(self, image: np.ndarray) -> np.ndarray:
        """
        Применяет размытие по Гауссу.
        
        Args:
            image: 2D массив изображения
            
        Returns:
            np.ndarray: Размытое изображение
        """
        result = np.zeros_like(image, dtype=np.float64)
        kernel_size = self.blur_kernel.shape[0]
        pad_size = kernel_size // 2
        
        for i in range(pad_size, image.shape[0] - pad_size):
            for j in range(pad_size, image.shape[1] - pad_size):
                # Извлекаем окно
                window = image[i-pad_size:i+pad_size+1, j-pad_size:j+pad_size+1]
                # Применяем свертку
                result[i, j] = np.sum(window * self.blur_kernel)
        
        return result
    
    def get_name(self) -> str:
        """Возвращает название фильтра."""
        return f"Нерезкое маскирование k={self.kernel_size}, λ={self.lambda_coeff:.1f}"
    
    def get_kernel_size(self) -> int:
        """Возвращает размер ядра."""
        return self.kernel_size
    
    def get_lambda_coeff(self) -> float:
        """Возвращает коэффициент λ."""
        return self.lambda_coeff
    
    def get_sigma(self) -> float:
        """Возвращает значение σ."""
        return self.sigma


class UnsharpMasking3x3(UnsharpMasking):
    """Нерезкое маскирование с ядром 3x3."""
    
    def __init__(self, lambda_coeff: float = 1.0):
        super().__init__(kernel_size=3, lambda_coeff=lambda_coeff)
    
    def get_name(self) -> str:
        return f"Нерезкое маскирование 3x3, λ={self.lambda_coeff:.1f}"


class UnsharpMasking5x5(UnsharpMasking):
    """Нерезкое маскирование с ядром 5x5."""
    
    def __init__(self, lambda_coeff: float = 1.0):
        super().__init__(kernel_size=5, lambda_coeff=lambda_coeff)
    
    def get_name(self) -> str:
        return f"Нерезкое маскирование 5x5, λ={self.lambda_coeff:.1f}"


class UnsharpMasking7x7(UnsharpMasking):
    """Нерезкое маскирование с ядром 7x7."""
    
    def __init__(self, lambda_coeff: float = 1.0):
        super().__init__(kernel_size=7, lambda_coeff=lambda_coeff)
    
    def get_name(self) -> str:
        return f"Нерезкое маскирование 7x7, λ={self.lambda_coeff:.1f}"


# Специализированные классы для различных значений λ
class UnsharpMaskingLambda05(UnsharpMasking):
    """Нерезкое маскирование с λ=0.5."""
    
    def __init__(self, kernel_size: int = 3):
        super().__init__(kernel_size=kernel_size, lambda_coeff=0.5)
    
    def get_name(self) -> str:
        return f"Нерезкое маскирование k={self.kernel_size}, λ=0.5"


class UnsharpMaskingLambda10(UnsharpMasking):
    """Нерезкое маскирование с λ=1.0."""
    
    def __init__(self, kernel_size: int = 3):
        super().__init__(kernel_size=kernel_size, lambda_coeff=1.0)
    
    def get_name(self) -> str:
        return f"Нерезкое маскирование k={self.kernel_size}, λ=1.0"


class UnsharpMaskingLambda15(UnsharpMasking):
    """Нерезкое маскирование с λ=1.5."""
    
    def __init__(self, kernel_size: int = 3):
        super().__init__(kernel_size=kernel_size, lambda_coeff=1.5)
    
    def get_name(self) -> str:
        return f"Нерезкое маскирование k={self.kernel_size}, λ=1.5"


class UnsharpMaskingLambda20(UnsharpMasking):
    """Нерезкое маскирование с λ=2.0."""
    
    def __init__(self, kernel_size: int = 3):
        super().__init__(kernel_size=kernel_size, lambda_coeff=2.0)
    
    def get_name(self) -> str:
        return f"Нерезкое маскирование k={self.kernel_size}, λ=2.0"


# Комбинированные классы для различных комбинаций k и λ
class UnsharpMasking3x3Lambda05(UnsharpMasking):
    """Нерезкое маскирование k=3, λ=0.5."""
    
    def __init__(self):
        super().__init__(kernel_size=3, lambda_coeff=0.5)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=3, λ=0.5"


class UnsharpMasking3x3Lambda10(UnsharpMasking):
    """Нерезкое маскирование k=3, λ=1.0."""
    
    def __init__(self):
        super().__init__(kernel_size=3, lambda_coeff=1.0)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=3, λ=1.0"


class UnsharpMasking3x3Lambda15(UnsharpMasking):
    """Нерезкое маскирование k=3, λ=1.5."""
    
    def __init__(self):
        super().__init__(kernel_size=3, lambda_coeff=1.5)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=3, λ=1.5"


class UnsharpMasking3x3Lambda20(UnsharpMasking):
    """Нерезкое маскирование k=3, λ=2.0."""
    
    def __init__(self):
        super().__init__(kernel_size=3, lambda_coeff=2.0)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=3, λ=2.0"


class UnsharpMasking5x5Lambda05(UnsharpMasking):
    """Нерезкое маскирование k=5, λ=0.5."""
    
    def __init__(self):
        super().__init__(kernel_size=5, lambda_coeff=0.5)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=5, λ=0.5"


class UnsharpMasking5x5Lambda10(UnsharpMasking):
    """Нерезкое маскирование k=5, λ=1.0."""
    
    def __init__(self):
        super().__init__(kernel_size=5, lambda_coeff=1.0)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=5, λ=1.0"


class UnsharpMasking5x5Lambda15(UnsharpMasking):
    """Нерезкое маскирование k=5, λ=1.5."""
    
    def __init__(self):
        super().__init__(kernel_size=5, lambda_coeff=1.5)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=5, λ=1.5"


class UnsharpMasking5x5Lambda20(UnsharpMasking):
    """Нерезкое маскирование k=5, λ=2.0."""
    
    def __init__(self):
        super().__init__(kernel_size=5, lambda_coeff=2.0)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=5, λ=2.0"


class UnsharpMasking7x7Lambda05(UnsharpMasking):
    """Нерезкое маскирование k=7, λ=0.5."""
    
    def __init__(self):
        super().__init__(kernel_size=7, lambda_coeff=0.5)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=7, λ=0.5"


class UnsharpMasking7x7Lambda10(UnsharpMasking):
    """Нерезкое маскирование k=7, λ=1.0."""
    
    def __init__(self):
        super().__init__(kernel_size=7, lambda_coeff=1.0)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=7, λ=1.0"


class UnsharpMasking7x7Lambda15(UnsharpMasking):
    """Нерезкое маскирование k=7, λ=1.5."""
    
    def __init__(self):
        super().__init__(kernel_size=7, lambda_coeff=1.5)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=7, λ=1.5"


class UnsharpMasking7x7Lambda20(UnsharpMasking):
    """Нерезкое маскирование k=7, λ=2.0."""
    
    def __init__(self):
        super().__init__(kernel_size=7, lambda_coeff=2.0)
    
    def get_name(self) -> str:
        return "Нерезкое маскирование k=7, λ=2.0"
