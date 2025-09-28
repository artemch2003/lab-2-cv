"""
Тесты для проверки соблюдения принципов SOLID.
"""

import unittest
import numpy as np
from PIL import Image

from image_processing.transforms.base_transform import BaseTransform
from image_processing.transforms.logarithmic_transform import LogarithmicTransform
from image_processing.transforms.power_transform import PowerTransform
from image_processing.transforms.binary_transform import BinaryTransform
from image_processing.transforms.brightness_range_transform import BrightnessRangeTransform
from image_processing.transforms.negative_transform import NegativeTransform
from image_processing.image_processor import ImageProcessor
from image_processing.interfaces.image_processor_interface import ImageProcessorInterface


class TestLiskovSubstitutionPrinciple(unittest.TestCase):
    """Тесты для проверки принципа подстановки Лисков."""
    
    def setUp(self):
        """Настройка тестов."""
        self.test_image = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        self.transforms = [
            LogarithmicTransform(),
            PowerTransform(),
            BinaryTransform(),
            BrightnessRangeTransform(),
            NegativeTransform()
        ]
    
    def test_transform_substitution(self):
        """Тест заменяемости преобразований."""
        for transform in self.transforms:
            with self.subTest(transform=transform.get_name()):
                # Проверяем, что все преобразования наследуются от BaseTransform
                self.assertIsInstance(transform, BaseTransform)
                
                # Проверяем, что все преобразования имеют необходимые методы
                self.assertTrue(hasattr(transform, 'apply'))
                self.assertTrue(hasattr(transform, 'get_name'))
                self.assertTrue(hasattr(transform, 'validate_parameters'))
                self.assertTrue(hasattr(transform, 'get_optimal_parameters'))
                
                # Проверяем, что методы возвращают правильные типы
                name = transform.get_name()
                self.assertIsInstance(name, str)
                self.assertGreater(len(name), 0)
                
                # Проверяем валидацию параметров
                self.assertTrue(transform.validate_parameters())
                
                # Проверяем получение оптимальных параметров
                optimal_params = transform.get_optimal_parameters(self.test_image)
                self.assertIsInstance(optimal_params, dict)
    
    def test_transform_behavior_consistency(self):
        """Тест согласованности поведения преобразований."""
        for transform in self.transforms:
            with self.subTest(transform=transform.get_name()):
                # Проверяем, что apply всегда возвращает массив того же размера
                result = transform.apply(self.test_image)
                self.assertEqual(result.shape, self.test_image.shape)
                self.assertEqual(result.dtype, np.uint8)
                
                # Проверяем, что результат находится в допустимом диапазоне
                self.assertTrue(np.all(result >= 0))
                self.assertTrue(np.all(result <= 255))
    
    def test_image_processor_substitution(self):
        """Тест заменяемости процессора изображений."""
        processor = ImageProcessor()
        
        # Проверяем, что ImageProcessor реализует интерфейс
        self.assertIsInstance(processor, ImageProcessorInterface)
        
        # Проверяем наличие всех необходимых методов
        required_methods = [
            'load_image', 'save_image', 'get_image_for_display',
            'apply_transform', 'get_image_info'
        ]
        
        for method_name in required_methods:
            self.assertTrue(hasattr(processor, method_name))
            self.assertTrue(callable(getattr(processor, method_name)))


class TestInterfaceSegregationPrinciple(unittest.TestCase):
    """Тесты для проверки принципа разделения интерфейсов."""
    
    def test_transform_interface_segregation(self):
        """Тест разделения интерфейсов преобразований."""
        # Проверяем, что интерфейс TransformInterface содержит только необходимые методы
        from image_processing.interfaces.transform_interface import TransformInterface
        
        required_methods = ['apply', 'get_name', 'validate_parameters', 'get_optimal_parameters']
        
        for method_name in required_methods:
            self.assertTrue(hasattr(TransformInterface, method_name))
    
    def test_image_processor_interface_segregation(self):
        """Тест разделения интерфейсов процессора изображений."""
        from image_processing.interfaces.image_processor_interface import ImageProcessorInterface
        
        required_methods = [
            'load_image', 'save_image', 'get_image_for_display',
            'apply_transform', 'get_image_info'
        ]
        
        for method_name in required_methods:
            self.assertTrue(hasattr(ImageProcessorInterface, method_name))


class TestDependencyInversionPrinciple(unittest.TestCase):
    """Тесты для проверки принципа инверсии зависимостей."""
    
    def test_controller_dependencies(self):
        """Тест зависимостей контроллера."""
        from gui.controllers.main_controller import MainController
        
        controller = MainController()
        
        # Проверяем, что контроллер использует абстракции, а не конкретные классы
        self.assertIsInstance(controller.image_processor, ImageProcessorInterface)
        
        # Проверяем, что контроллер может работать с любым процессором, реализующим интерфейс
        self.assertTrue(hasattr(controller.image_processor, 'apply_transform'))
        self.assertTrue(hasattr(controller.image_processor, 'get_image_info'))


if __name__ == '__main__':
    unittest.main()
