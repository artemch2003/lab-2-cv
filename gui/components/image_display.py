"""
Компонент для отображения изображений.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Callable
import os
import logging

logger = logging.getLogger(__name__)


class ImageDisplay:
    """Компонент для отображения изображений."""
    
    def __init__(self, parent_frame: ttk.Frame, on_image_loaded: Callable[[str], None]):
        """
        Инициализация компонента отображения.
        
        Args:
            parent_frame: Родительский фрейм
            on_image_loaded: Callback для загрузки изображения
        """
        self.parent_frame = parent_frame
        self.on_image_loaded = on_image_loaded
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Создает виджеты отображения."""
        # Область отображения изображений
        display_frame = ttk.Frame(self.parent_frame)
        display_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Исходное изображение
        original_frame = ttk.LabelFrame(display_frame, text="Исходное изображение", padding="5")
        original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        original_frame.rowconfigure(0, weight=1)
        
        self.original_label = ttk.Label(
            original_frame, 
            text="Изображение не загружено", 
            anchor="center", 
            background="lightgray"
        )
        self.original_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Обработанное изображение
        processed_frame = ttk.LabelFrame(display_frame, text="Обработанное изображение", padding="5")
        processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        processed_frame.rowconfigure(0, weight=1)
        
        self.processed_label = ttk.Label(
            processed_frame, 
            text="Результат обработки", 
            anchor="center", 
            background="lightgray"
        )
        self.processed_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def display_original_image(self, image):
        """
        Отображает исходное изображение.
        
        Args:
            image: Изображение для отображения
        """
        if image:
            self.original_label.configure(image=image, text="")
            self.original_label.image = image  # Сохраняем ссылку
        else:
            self.original_label.configure(image="", text="Изображение не загружено")
    
    def display_processed_image(self, image):
        """
        Отображает обработанное изображение.
        
        Args:
            image: Изображение для отображения
        """
        if image:
            self.processed_label.configure(image=image, text="")
            self.processed_label.image = image  # Сохраняем ссылку
        else:
            self.processed_label.configure(image="", text="Результат обработки")
    
    def load_image_dialog(self) -> Optional[str]:
        """
        Открывает диалог загрузки изображения.
        
        Returns:
            Optional[str]: Путь к выбранному файлу или None
        """
        file_types = [
            ("Изображения", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
            ("PNG файлы", "*.png"),
            ("JPEG файлы", "*.jpg *.jpeg"),
            ("Все файлы", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=file_types
        )
        
        if file_path:
            self.on_image_loaded(file_path)
            return file_path
        
        return None
    
    def save_image_dialog(self) -> Optional[str]:
        """
        Открывает диалог сохранения изображения.
        
        Returns:
            Optional[str]: Путь для сохранения или None
        """
        file_types = [
            ("PNG файлы", "*.png"),
            ("JPEG файлы", "*.jpg"),
            ("Все файлы", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить обработанное изображение",
            defaultextension=".png",
            filetypes=file_types
        )
        
        return file_path if file_path else None
