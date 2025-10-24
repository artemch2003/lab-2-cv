"""
Главный контроллер приложения.
"""

import tkinter as tk
from tkinter import messagebox
from typing import Optional, Dict, Any
import logging

from image_processing.interfaces.image_processor_interface import ImageProcessorInterface
from utils.validators import ParameterValidator

logger = logging.getLogger(__name__)


class MainController:
    """Главный контроллер приложения."""
    
    def __init__(self, image_processor: ImageProcessorInterface, validator: ParameterValidator):
        """
        Инициализация контроллера.
        
        Args:
            image_processor: Процессор изображений
            validator: Валидатор параметров
        """
        self.image_processor = image_processor
        self.validator = validator
        
        # Callbacks для обновления UI
        self.on_status_update: Optional[callable] = None
        self.on_image_display_update: Optional[callable] = None
        self.on_info_update: Optional[callable] = None
    
    def set_callbacks(self, on_status_update: callable, on_image_display_update: callable, on_info_update: callable):
        """
        Устанавливает callbacks для обновления UI.
        
        Args:
            on_status_update: Callback для обновления статуса
            on_image_display_update: Callback для обновления отображения изображений
            on_info_update: Callback для обновления информации
        """
        self.on_status_update = on_status_update
        self.on_image_display_update = on_image_display_update
        self.on_info_update = on_info_update
    
    def load_image(self, file_path: str) -> bool:
        """
        Загружает изображение.
        
        Args:
            file_path: Путь к файлу изображения
            
        Returns:
            bool: True если изображение успешно загружено
        """
        self._update_status("Загрузка изображения...")
        
        if self.image_processor.load_image(file_path):
            self._update_image_display()
            self._update_info()
            self._update_status(f"Изображение загружено: {file_path}")
            return True
        else:
            self._update_status("Ошибка загрузки изображения")
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение")
            return False
    
    def save_image(self, file_path: str) -> bool:
        """
        Сохраняет обработанное изображение.
        
        Args:
            file_path: Путь для сохранения
            
        Returns:
            bool: True если изображение успешно сохранено
        """
        if not self.image_processor.image_manager.has_processed_image():
            messagebox.showwarning("Предупреждение", "Нет обработанного изображения для сохранения")
            return False
        
        self._update_status("Сохранение изображения...")
        
        if self.image_processor.save_image(file_path):
            self._update_status(f"Изображение сохранено: {file_path}")
            return True
        else:
            self._update_status("Ошибка сохранения изображения")
            messagebox.showerror("Ошибка", "Не удалось сохранить изображение")
            return False
    
    def apply_transform(self, parameters: Dict[str, Any]) -> bool:
        """
        Применяет преобразование с заданными параметрами.
        
        Args:
            parameters: Словарь с параметрами преобразования
            
        Returns:
            bool: True если преобразование успешно применено
        """
        if not self.image_processor.image_manager.has_original_image():
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return False
        
        transform_type = parameters.get('transform_type')
        self._update_status(f"Применение {transform_type.lower()} преобразования...")
        
        try:
            success = False
            
            if transform_type == "Логарифмическое":
                success = self._apply_logarithmic_transform(parameters)
            elif transform_type == "Степенное":
                success = self._apply_power_transform(parameters)
            elif transform_type == "Бинарное":
                success = self._apply_binary_transform(parameters)
            elif transform_type == "Вырезание диапазона яркостей":
                success = self._apply_brightness_range_transform(parameters)
            elif transform_type in ["Прямоугольный фильтр 3x3", "Прямоугольный фильтр 5x5", 
                                  "Медианный фильтр 3x3", "Медианный фильтр 5x5"]:
                success = self._apply_smoothing_filter(parameters)
            
            if success:
                self._update_image_display()
                self._update_info()
                self._update_status(f"{transform_type} преобразование применено")
            else:
                self._update_status("Ошибка применения преобразования")
                messagebox.showerror("Ошибка", "Не удалось применить преобразование")
            
            return success
            
        except ValueError as e:
            self._update_status("Ошибка валидации параметров")
            messagebox.showerror("Ошибка", str(e))
            return False
        except Exception as e:
            logger.error(f"Ошибка при применении преобразования: {e}")
            self._update_status("Ошибка применения преобразования")
            messagebox.showerror("Ошибка", f"Произошла ошибка при применении преобразования: {e}")
            return False
    
    def _apply_logarithmic_transform(self, parameters: Dict[str, Any]) -> bool:
        """Применяет логарифмическое преобразование."""
        mode = parameters.get('mode', 'Автоматически')
        c = parameters.get('c') if mode == "Вручную" else None
        
        return self.image_processor.apply_logarithmic_transform(c)
    
    def _apply_power_transform(self, parameters: Dict[str, Any]) -> bool:
        """Применяет степенное преобразование."""
        mode = parameters.get('mode', 'Автоматически')
        gamma = parameters.get('gamma', 1.0) if mode == "Вручную" else 1.0
        c = parameters.get('c') if mode == "Вручную" else None
        
        return self.image_processor.apply_power_transform(gamma, c)
    
    def _apply_binary_transform(self, parameters: Dict[str, Any]) -> bool:
        """Применяет бинарное преобразование."""
        threshold = parameters.get('threshold', 128)
        
        return self.image_processor.apply_binary_transform(threshold)
    
    def _apply_brightness_range_transform(self, parameters: Dict[str, Any]) -> bool:
        """Применяет вырезание диапазона яркостей."""
        min_brightness = parameters.get('min_brightness', 0)
        max_brightness = parameters.get('max_brightness', 255)
        outside_mode = parameters.get('outside_mode', 'Исходное')
        constant_value = parameters.get('constant_value')
        
        return self.image_processor.apply_brightness_range_transform(
            min_brightness, max_brightness, outside_mode, constant_value
        )
    
    def _apply_smoothing_filter(self, parameters: Dict[str, Any]) -> bool:
        """Применяет фильтр сглаживания."""
        transform_type = parameters.get('transform_type')
        kernel_size = parameters.get('kernel_size', 3)
        
        # Используем фабрику для создания фильтра
        from image_processing.factories.transform_factory import TransformFactory
        
        try:
            filter_transform = TransformFactory.create_transform(transform_type)
            return self.image_processor.apply_custom_transform(filter_transform, kernel_size=kernel_size)
        except Exception as e:
            logger.error(f"Ошибка при применении фильтра сглаживания: {e}")
            return False
    
    def get_image_for_display(self, image_type: str = "original"):
        """
        Получает изображение для отображения.
        
        Args:
            image_type: Тип изображения ("original" или "processed")
            
        Returns:
            Изображение для отображения
        """
        if image_type == "original":
            image = self.image_processor.original_image
        else:
            image = self.image_processor.processed_image
        
        if image:
            return self.image_processor.get_image_for_display(image)
        return None
    
    def get_image_info(self) -> Dict[str, Any]:
        """Возвращает информацию об изображении."""
        return self.image_processor.get_image_info()
    
    def _update_status(self, message: str):
        """Обновляет статус."""
        if self.on_status_update:
            self.on_status_update(message)
    
    def _update_image_display(self):
        """Обновляет отображение изображений."""
        if self.on_image_display_update:
            original_image = self.get_image_for_display("original")
            processed_image = self.get_image_for_display("processed")
            self.on_image_display_update(original_image, processed_image)
    
    def reset_image(self) -> bool:
        """
        Сбрасывает изображение к исходному состоянию.
        
        Returns:
            bool: True если сброс выполнен успешно
        """
        if not self.image_processor.image_manager.has_original_image():
            messagebox.showwarning("Предупреждение", "Нет изображения для сброса")
            return False
        
        self._update_status("Сброс изображения...")
        
        # Сбрасываем обработанное изображение
        self.image_processor.image_manager.clear_processed_image()
        
        self._update_image_display()
        self._update_info()
        self._update_status("Изображение сброшено к исходному состоянию")
        return True
    
    def _update_info(self):
        """Обновляет информацию."""
        if self.on_info_update:
            info = self.get_image_info()
            self.on_info_update(info)
