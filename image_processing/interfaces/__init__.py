"""
Интерфейсы для обработки изображений.
"""

from .image_processor_interface import ImageProcessorInterface
from .transform_interface import TransformInterface

__all__ = [
    'ImageProcessorInterface',
    'TransformInterface'
]
