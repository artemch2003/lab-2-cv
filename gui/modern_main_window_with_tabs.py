"""
Современное главное окно приложения с вкладками в стиле фоторедактора.
Включает отдельную вкладку для фильтров сглаживания.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import os
from typing import Optional, Callable
from PIL import Image, ImageTk
import time

from gui.components.modern_image_display import ModernImageDisplay
from gui.components.modern_transform_settings import ModernTransformSettings
from gui.components.modern_smoothing_settings import ModernSmoothingSettings
from gui.components.modern_info_panel import ModernInfoPanel
from gui.components.animations import AnimationManager, LoadingSpinner, ProgressBar
from gui.styles.modern_styles import ModernStyles
from gui.controllers.main_controller import MainController
from di.container import DIContainer
from di.config import create_container

logger = logging.getLogger(__name__)


class ModernMainWindowWithTabs:
    """Современное главное окно приложения с вкладками в стиле фоторедактора."""
    
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
        self.setup_styles()
        self.create_widgets()
        self.setup_controller()
        self.setup_animations()
    
    def setup_animations(self):
        """Настраивает анимации."""
        self.animation_manager = AnimationManager()
        
    def setup_window(self):
        """Настройка параметров окна."""
        self.root.title("Photo Editor Pro - Обработка изображений")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 800)
        
        # Устанавливаем иконку (если есть)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def setup_styles(self):
        """Настраивает стили интерфейса."""
        self.styles = ModernStyles()
        
        # Настройка фона главного окна
        self.root.configure(bg=self.styles.get_color('bg_primary'))
    
    def create_widgets(self):
        """Создание виджетов интерфейса."""
        # Главный контейнер
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding="0")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания главного контейнера
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Заголовок приложения
        self.create_header(main_container)
        
        # Основная рабочая область с вкладками
        self.create_main_workspace(main_container)
        
        # Нижняя панель
        self.create_bottom_panel(main_container)
    
    def create_header(self, parent):
        """Создает заголовок приложения."""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        # Логотип и название
        title_label = ttk.Label(header_frame, 
                               text="Photo Editor Pro", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W, padx=(20, 0), pady=10)
        
        # Панель управления
        control_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        control_frame.grid(row=0, column=1, sticky=tk.E, padx=(0, 20), pady=10)
        
        # Кнопки управления
        self.load_btn = ttk.Button(control_frame, 
                                  text="📁 Загрузить", 
                                  style='Modern.TButton',
                                  command=self.load_image)
        self.load_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.save_btn = ttk.Button(control_frame, 
                                  text="💾 Сохранить", 
                                  style='Modern.TButton',
                                  command=self.save_image)
        self.save_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.reset_btn = ttk.Button(control_frame, 
                                   text="🔄 Сброс", 
                                   style='Modern.TButton',
                                   command=self.reset_image)
        self.reset_btn.grid(row=0, column=2)
    
    def create_main_workspace(self, parent):
        """Создает основную рабочую область с вкладками."""
        workspace_frame = ttk.Frame(parent, style='Modern.TFrame')
        workspace_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20)
        workspace_frame.columnconfigure(0, weight=2)
        workspace_frame.columnconfigure(1, weight=1)
        workspace_frame.rowconfigure(1, weight=1)
        
        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(workspace_frame, style='Modern.TNotebook')
        self.notebook.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Вкладка "Основные преобразования"
        self.create_basic_transforms_tab()
        
        # Вкладка "Сглаживание"
        self.create_smoothing_tab()
        
        # Область отображения изображений (общая для всех вкладок)
        self.image_display = ModernImageDisplay(workspace_frame, self.on_image_loaded)
    
    def create_basic_transforms_tab(self):
        """Создает вкладку основных преобразований."""
        # Фрейм для вкладки основных преобразований
        basic_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(basic_frame, text="🎨 Основные преобразования")
        
        # Настройки основных преобразований
        self.transform_settings = ModernTransformSettings(basic_frame, self.on_transform_type_change)
        self.transform_settings.set_apply_command(self.apply_basic_transform)
    
    def create_smoothing_tab(self):
        """Создает вкладку сглаживания."""
        # Фрейм для вкладки сглаживания
        smoothing_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(smoothing_frame, text="🔧 Сглаживание")
        
        # Настройки сглаживания
        self.smoothing_settings = ModernSmoothingSettings(smoothing_frame, self.on_filter_type_change)
        self.smoothing_settings.set_apply_command(self.apply_smoothing_filter)
    
    def create_bottom_panel(self, parent):
        """Создает нижнюю панель."""
        bottom_frame = ttk.Frame(parent, style='Modern.TFrame')
        bottom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        bottom_frame.columnconfigure(0, weight=1)
        bottom_frame.rowconfigure(0, weight=1)
        
        # Информационная панель
        self.info_panel = ModernInfoPanel(bottom_frame)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(bottom_frame, 
                              textvariable=self.status_var, 
                              style='Status.TLabel',
                              anchor='w')
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0), padx=20)
    
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
    
    def reset_image(self):
        """Сбрасывает изображение к исходному состоянию."""
        self.controller.reset_image()
    
    def apply_basic_transform(self):
        """Применяет основное преобразование."""
        try:
            parameters = self.transform_settings.get_transform_parameters()
            self.controller.apply_transform(parameters)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def apply_smoothing_filter(self):
        """Применяет фильтр сглаживания."""
        try:
            parameters = self.smoothing_settings.get_filter_parameters()
            self.controller.apply_transform(parameters)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def on_transform_type_change(self, transform_type: str):
        """Обрабатывает изменение типа преобразования."""
        # Обновляем UI в зависимости от типа преобразования
        pass
    
    def on_filter_type_change(self, filter_type: str):
        """Обрабатывает изменение типа фильтра."""
        # Обновляем UI в зависимости от типа фильтра
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
        # Анимация появления изображений
        if original_image:
            self.animation_manager.fade_in(self.image_display.original_canvas, duration=300)
        if processed_image:
            self.animation_manager.fade_in(self.image_display.processed_canvas, duration=300)
        
        self.image_display.display_original_image(original_image)
        self.image_display.display_processed_image(processed_image)
    
    def update_info(self, info):
        """Обновляет информационную панель."""
        # Анимация обновления информационной панели
        self.animation_manager.fade_in(self.info_panel.notebook, duration=200)
        self.info_panel.update_info(info)
