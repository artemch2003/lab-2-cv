"""
Менеджер изображений для приложения.
Содержит общую логику работы с изображениями.
"""

import tkinter as tk
from tkinter import filedialog
from PIL import Image
import numpy as np
import os

from constants import FILE_TYPES, DISPLAY_IMAGE_SIZE
from gui.components.base_components import BaseCanvas
from gui.windows.window_manager import WindowManager


class ImageManager:
    """Менеджер изображений для обработки и отображения."""
    
    def __init__(self, window_manager):
        self.window_manager = window_manager
        self.original_image = None
        self.processed_image = None
    
    def load_image(self):
        """Загружает изображение из файла."""
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=FILE_TYPES['load']
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                return True, f"Изображение загружено: {os.path.basename(file_path)}"
            except Exception as e:
                return False, f"Не удалось загрузить изображение: {e}"
        
        return False, "Файл не выбран"
    
    def save_image(self):
        """Сохраняет обработанное изображение."""
        if not self.processed_image:
            return False, "Нет обработанного изображения для сохранения"
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить обработанное изображение",
            defaultextension=".png",
            filetypes=FILE_TYPES['save']
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                return True, f"Изображение сохранено: {os.path.basename(file_path)}"
            except Exception as e:
                return False, f"Не удалось сохранить изображение: {e}"
        
        return False, "Файл не выбран"
    
    def reset_image(self):
        """Сбрасывает обработанное изображение."""
        if not self.original_image:
            return False, "Нет изображения для сброса"
        
        self.processed_image = None
        return True, "Изображение сброшено к исходному состоянию"
    
    def apply_transform(self, transform_type, params):
        """Применяет преобразование к изображению."""
        if not self.original_image:
            return False, "Сначала загрузите изображение"
        
        try:
            # Применяем преобразование с помощью фабрики
            from image_processing.factories.transform_factory import TransformFactory
            
            # Создаем преобразование
            transform = TransformFactory.create_transform(transform_type)
            
            # Конвертируем изображение в numpy array
            image_array = np.array(self.original_image)
            
            # Применяем преобразование
            processed_array = transform.apply(image_array, **params)
            
            # Конвертируем обратно в PIL Image
            if len(processed_array.shape) == 3:
                self.processed_image = Image.fromarray(processed_array)
            else:
                self.processed_image = Image.fromarray(processed_array, mode='L')
            
            return True, f"{transform_type} преобразование применено"
        except Exception as e:
            return False, f"Не удалось применить преобразование: {e}"
    
    def get_image_info(self):
        """Возвращает информацию об изображении."""
        if not self.original_image:
            return "Изображение не загружено"
        
        info = f"Размер: {self.original_image.size}\n"
        info += f"Режим: {self.original_image.mode}\n"
        info += f"Формат: {self.original_image.format}"
        
        return info
    
    def display_image_in_canvas(self, canvas, image, size=None):
        """Отображает изображение в canvas."""
        if image is None:
            return
        
        if size is None:
            size = DISPLAY_IMAGE_SIZE
        
        # Изменяем размер для отображения
        display_image = image.copy()
        display_image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Конвертируем в PhotoImage
        photo = ImageTk.PhotoImage(display_image)
        
        # Очищаем canvas и отображаем изображение
        canvas.delete("all")
        canvas.create_image(
            canvas.winfo_width() // 2, 
            canvas.winfo_height() // 2, 
            image=photo
        )
        canvas.image = photo  # Сохраняем ссылку
        
        return photo
