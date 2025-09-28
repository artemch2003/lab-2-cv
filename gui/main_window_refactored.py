"""
Рефакторированное главное окно приложения.
Использует принципы SOLID для разделения ответственности.
"""

import tkinter as tk
from tkinter import ttk
import logging
import os
from typing import Optional

from .components.transform_settings import TransformSettings
from .components.image_display import ImageDisplay
from .components.info_panel import InfoPanel
from .controllers.main_controller import MainController
from di.container import DIContainer
from di.config import create_container

logger = logging.getLogger(__name__)


class MainWindow:
    """Главное окно приложения."""
    
    def __init__(self, root, container: Optional[DIContainer] = None):
        """
        Инициализация главного окна.
        
        Args:
            root: Корневое окно tkinter
            container: Контейнер зависимостей
        """
        self.root = root
        self.container = container or create_container()
        
        # Создаем контроллер с инжекцией зависимостей
        from image_processing.interfaces.image_processor_interface import ImageProcessorInterface
        from utils.validators import ParameterValidator
        
        image_processor = self.container.get(ImageProcessorInterface)
        validator = self.container.get(ParameterValidator)
        self.controller = MainController(image_processor, validator)
        
        self.setup_window()
        self.create_widgets()
        self.setup_controller()
        
    def setup_window(self):
        """Настройка параметров окна."""
        self.root.title("Обработка изображений - Преобразования")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
    def create_widgets(self):
        """Создание виджетов интерфейса."""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Обработка изображений", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Кнопки управления
        ttk.Button(control_frame, text="Загрузить изображение", 
                  command=self.load_image).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(control_frame, text="Сохранить результат", 
                  command=self.save_image).grid(row=0, column=1, padx=(0, 10))
        
        # Настройки преобразования
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="10")
        settings_frame.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Создаем компонент настроек
        self.transform_settings = TransformSettings(settings_frame, self.on_transform_type_change)
        self.transform_settings.set_apply_command(self.apply_transform)
        
        # Область отображения изображений
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Создаем компонент отображения изображений
        self.image_display = ImageDisplay(display_frame, self.on_image_loaded)
        
        # Информационная панель
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Создаем информационную панель
        self.info_panel = InfoPanel(info_frame)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def setup_controller(self):
        """Настраивает контроллер с callbacks."""
        self.controller.set_callbacks(
            on_status_update=self.update_status,
            on_image_display_update=self.update_image_display,
            on_info_update=self.update_info
        )
    
    def load_image(self):
        """Загружает изображение из файла."""
        file_path = self.image_display.load_image_dialog()
        if file_path:
            self.controller.load_image(file_path)
    
    def save_image(self):
        """Сохраняет обработанное изображение."""
        file_path = self.image_display.save_image_dialog()
        if file_path:
            self.controller.save_image(file_path)
    
    def apply_transform(self):
        """Применяет преобразование."""
        try:
            parameters = self.transform_settings.get_transform_parameters()
            self.controller.apply_transform(parameters)
        except ValueError as e:
            tk.messagebox.showerror("Ошибка", str(e))
    
    def on_transform_type_change(self, transform_type: str):
        """Обрабатывает изменение типа преобразования."""
        # Обновляем UI в зависимости от типа преобразования
        pass
    
    def on_image_loaded(self, file_path: str):
        """Обрабатывает загрузку изображения."""
        self.controller.load_image(file_path)
    
    def update_status(self, message: str):
        """Обновляет статус."""
        self.status_var.set(message)
        self.root.update()
    
    def update_image_display(self, original_image, processed_image):
        """Обновляет отображение изображений."""
        self.image_display.display_original_image(original_image)
        self.image_display.display_processed_image(processed_image)
    
    def update_info(self, info):
        """Обновляет информационную панель."""
        self.info_panel.update_info(info)
