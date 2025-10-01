"""
Менеджер событий для приложения.
Содержит общую логику обработки событий интерфейса.
"""

import tkinter as tk
from constants import TRANSFORM_DESCRIPTIONS


class EventManager:
    """Менеджер событий для обработки взаимодействий с интерфейсом."""
    
    def __init__(self, parameter_manager, image_manager, quality_manager, update_info_callback):
        self.parameter_manager = parameter_manager
        self.image_manager = image_manager
        self.quality_manager = quality_manager
        self.update_info_callback = update_info_callback
    
    def on_transform_change(self, transform_type, desc_text):
        """Обрабатывает изменение типа преобразования."""
        # Обновляем описание
        desc_text.configure(state=tk.NORMAL)
        desc_text.delete(1.0, tk.END)
        desc_text.insert(1.0, TRANSFORM_DESCRIPTIONS.get(transform_type, ""))
        desc_text.configure(state=tk.DISABLED)
        
        # Обновляем UI для выбранного типа преобразования
        self.parameter_manager.show_elements_for_transform(transform_type)
    
    def on_load_image(self, canvas):
        """Обрабатывает загрузку изображения."""
        success, message = self.image_manager.load_image()
        
        if success:
            canvas.display_image(self.image_manager.original_image)
            self.update_info_callback(message)
        else:
            from gui.windows.window_manager import WindowManager
            window_manager = WindowManager(None)
            window_manager.show_error("Ошибка", message)
        
        return success, message
    
    def on_save_image(self):
        """Обрабатывает сохранение изображения."""
        success, message = self.image_manager.save_image()
        
        if not success:
            from gui.windows.window_manager import WindowManager
            window_manager = WindowManager(None)
            window_manager.show_warning("Предупреждение", message)
        
        return success, message
    
    def on_reset_image(self, canvas):
        """Обрабатывает сброс изображения."""
        success, message = self.image_manager.reset_image()
        
        if success:
            canvas.display_placeholder("Примените преобразование\nдля просмотра результата")
            self.update_info_callback(message)
        else:
            from gui.windows.window_manager import WindowManager
            window_manager = WindowManager(None)
            window_manager.show_warning("Предупреждение", message)
        
        return success, message
    
    def on_apply_transform(self, transform_type, canvas):
        """Обрабатывает применение преобразования."""
        try:
            # Получаем параметры преобразования
            params = self.parameter_manager.get_parameters(transform_type)
            
            # Применяем преобразование
            success, message = self.image_manager.apply_transform(transform_type, params)
            
            if success:
                canvas.display_image(self.image_manager.processed_image)
                
                # Обновляем информацию о примененных параметрах
                param_info = self.parameter_manager.format_parameters_info(params)
                self.update_info_callback(f"Применено преобразование: {transform_type}\n{param_info}")
            else:
                from gui.windows.window_manager import WindowManager
                window_manager = WindowManager(None)
                window_manager.show_error("Ошибка", message)
            
            return success, message
        except Exception as e:
            from gui.windows.window_manager import WindowManager
            window_manager = WindowManager(None)
            window_manager.show_error("Ошибка", f"Не удалось применить преобразование: {e}")
            return False, str(e)
    
    def on_analyze_quality(self):
        """Обрабатывает анализ качества."""
        self.quality_manager.analyze_quality(
            self.image_manager.original_image,
            self.image_manager.processed_image,
            self.update_info_callback
        )
    
    def on_show_difference_map(self):
        """Обрабатывает показ карты разности."""
        self.quality_manager.show_difference_map()
    
    def on_compare_filters(self):
        """Обрабатывает сравнение фильтров."""
        self.quality_manager.compare_filters(
            self.image_manager.original_image, 
            self.update_info_callback
        )
    
    def on_compare_sharpness_filters(self):
        """Обрабатывает сравнение фильтров резкости."""
        self.quality_manager.compare_sharpness_filters(
            self.image_manager.original_image, 
            self.update_info_callback
        )
