"""
Рефакторированное главное окно приложения.
Использует модульную архитектуру и устраняет дублирование кода.
"""

import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import numpy as np

from constants import (
    COLORS, FONTS, MESSAGES, TRANSFORM_DESCRIPTIONS, 
    DISPLAY_IMAGE_SIZE, FILE_TYPES
)
from gui.components.ui_factory import UIFactory
from gui.components.base_components import BaseCanvas, BaseInfoPanel
from gui.styles.style_manager import StyleManager
from gui.windows.window_manager import WindowManager
from gui.parameters.parameter_manager import ParameterManager
from gui.quality.quality_manager import QualityManager


class RefactoredMainWindow:
    """Рефакторированное главное окно приложения."""
    
    def __init__(self, root):
        """Инициализация главного окна."""
        self.root = root
        self.original_image = None
        self.processed_image = None
        
        # Инициализация менеджеров
        self.style_manager = StyleManager()
        self.window_manager = WindowManager(root)
        self.ui_factory = UIFactory()
        
        # Настройка окна
        self.window_manager.setup_main_window()
        
        # Создание интерфейса
        self.create_interface()
    
    def create_interface(self):
        """Создание интерфейса."""
        # Главный контейнер
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding="0")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        self.create_header(main_container)
        
        # Основная рабочая область
        self.create_workspace(main_container)
        
        # Панель оценки качества
        self.quality_manager = QualityManager(main_container, self.window_manager)
        self.quality_panel = self.quality_manager.create_quality_panel(main_container)
        
        # Нижняя панель
        self.create_bottom_panel(main_container)
    
    def create_header(self, parent):
        """Создает заголовок приложения."""
        header_frame = ttk.Frame(parent, style='Modern.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Логотип и название
        title_label = ttk.Label(header_frame, text="Photo Editor Pro", style='Title.TLabel')
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Панель управления
        control_frame = ttk.Frame(header_frame, style='Modern.TFrame')
        control_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Кнопки управления
        load_btn = self.ui_factory.create_button(control_frame, "📁 Загрузить", self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = self.ui_factory.create_button(control_frame, "💾 Сохранить", self.save_image)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = self.ui_factory.create_button(control_frame, "🔄 Сброс", self.reset_image)
        reset_btn.pack(side=tk.LEFT, padx=5)
    
    def create_workspace(self, parent):
        """Создает основную рабочую область."""
        workspace_frame = ttk.Frame(parent, style='Modern.TFrame')
        workspace_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        workspace_frame.columnconfigure(0, weight=2)
        workspace_frame.columnconfigure(1, weight=1)
        
        # Область отображения изображений
        self.create_image_area(workspace_frame)
        
        # Панель настроек
        self.create_settings_panel(workspace_frame)
    
    def create_image_area(self, parent):
        """Создает область отображения изображений."""
        display_frame = self.ui_factory.create_label_frame(
            parent, "Изображения", padding="10"
        )
        display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Исходное изображение
        original_frame = self.ui_factory.create_label_frame(
            display_frame, "Исходное изображение", padding="5"
        )
        original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.original_canvas = BaseCanvas(original_frame)
        self.original_canvas.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
        self.original_canvas.display_placeholder(MESSAGES['load_placeholder'])
        
        # Обработанное изображение
        processed_frame = self.ui_factory.create_label_frame(
            display_frame, "Обработанное изображение", padding="5"
        )
        processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.processed_canvas = BaseCanvas(processed_frame)
        self.processed_canvas.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
        self.processed_canvas.display_placeholder(MESSAGES['processed_placeholder'])
    
    def create_settings_panel(self, parent):
        """Создает панель настроек."""
        settings_frame = self.ui_factory.create_label_frame(
            parent, "Настройки преобразования", padding="15"
        )
        settings_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Тип преобразования
        ttk.Label(settings_frame, text="Тип преобразования:", style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.transform_combo = self.ui_factory.create_transform_combobox(settings_frame)
        self.transform_combo.pack(fill=tk.X, pady=(0, 10))
        self.transform_combo.set("Логарифмическое")
        self.transform_combo.bind("<<ComboboxSelected>>", self.on_transform_change)
        
        # Описание
        self.desc_text = self.ui_factory.create_text(settings_frame, height=4, width=30)
        self.desc_text.pack(fill=tk.X, pady=(0, 10))
        self.desc_text.insert(1.0, TRANSFORM_DESCRIPTIONS["Логарифмическое"])
        self.desc_text.configure(state=tk.DISABLED)
        
        # Параметры
        self.params_frame = ttk.Frame(settings_frame, style='Modern.TFrame')
        self.params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Менеджер параметров
        self.parameter_manager = ParameterManager(self.params_frame)
        self.parameter_manager.pack()
        
        # Кнопка применения
        apply_btn = self.ui_factory.create_button(
            settings_frame, "✨ Применить преобразование", self.apply_transform
        )
        apply_btn.pack(fill=tk.X, pady=(10, 0))
    
    def create_bottom_panel(self, parent):
        """Создает нижнюю панель."""
        # Информационная панель
        info_frame = self.ui_factory.create_label_frame(parent, "Информация", padding="10")
        info_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.info_panel = BaseInfoPanel(info_frame, height=3)
        self.info_panel.pack(fill=tk.X)
        self.info_panel.update_info(f"Информация об изображении:\n{MESSAGES['no_image']}")
        
        # Статус бар
        self.status_var = tk.StringVar(value=MESSAGES['ready'])
        status_bar = ttk.Label(parent, textvariable=self.status_var, style='Status.TLabel')
        status_bar.pack(fill=tk.X, pady=(10, 0), padx=20)
    
    def load_image(self):
        """Загружает изображение."""
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=FILE_TYPES['load']
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.original_canvas.display_image(self.original_image)
                self.update_info(f"Изображение загружено: {os.path.basename(file_path)}")
                self.status_var.set(f"Изображение загружено: {os.path.basename(file_path)}")
            except Exception as e:
                self.window_manager.show_error("Ошибка", f"Не удалось загрузить изображение: {e}")
                self.status_var.set("Ошибка загрузки изображения")
    
    def apply_transform(self):
        """Применяет преобразование."""
        if not self.original_image:
            self.window_manager.show_warning("Предупреждение", "Сначала загрузите изображение")
            return
        
        transform_type = self.transform_combo.get()
        self.status_var.set(f"Применение {transform_type.lower()} преобразования...")
        
        try:
            # Получаем параметры преобразования
            params = self.parameter_manager.get_parameters(transform_type)
            
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
            
            self.processed_canvas.display_image(self.processed_image)
            
            # Обновляем информацию о примененных параметрах
            param_info = self.parameter_manager.format_parameters_info(params)
            self.update_info(f"Применено преобразование: {transform_type}\n{param_info}")
            self.status_var.set(f"{transform_type} преобразование применено")
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось применить преобразование: {e}")
            self.status_var.set("Ошибка применения преобразования")
    
    def save_image(self):
        """Сохраняет обработанное изображение."""
        if not self.processed_image:
            self.window_manager.show_warning("Предупреждение", "Нет обработанного изображения для сохранения")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить обработанное изображение",
            defaultextension=".png",
            filetypes=FILE_TYPES['save']
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.status_var.set(f"Изображение сохранено: {os.path.basename(file_path)}")
            except Exception as e:
                self.window_manager.show_error("Ошибка", f"Не удалось сохранить изображение: {e}")
                self.status_var.set("Ошибка сохранения изображения")
    
    def reset_image(self):
        """Сбрасывает изображение к исходному состоянию."""
        if not self.original_image:
            self.window_manager.show_warning("Предупреждение", "Нет изображения для сброса")
            return
        
        self.processed_image = None
        self.processed_canvas.display_placeholder(MESSAGES['processed_placeholder'])
        self.update_info("Изображение сброшено к исходному состоянию")
        self.status_var.set("Изображение сброшено к исходному состоянию")
    
    def on_transform_change(self, event=None):
        """Обрабатывает изменение типа преобразования."""
        transform_type = self.transform_combo.get()
        
        # Обновляем описание
        self.desc_text.configure(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(1.0, TRANSFORM_DESCRIPTIONS.get(transform_type, ""))
        self.desc_text.configure(state=tk.DISABLED)
        
        # Обновляем UI для выбранного типа преобразования
        self.parameter_manager.show_elements_for_transform(transform_type)
    
    def update_info(self, message):
        """Обновляет информационную панель."""
        self.info_panel.update_info(f"Информация об изображении:\n{message}")
    
    def analyze_quality(self):
        """Анализирует качество обработки изображения."""
        self.quality_manager.analyze_quality(
            self.original_image, 
            self.processed_image, 
            self.update_info
        )
    
    def show_difference_map(self):
        """Показывает карту разности."""
        self.quality_manager.show_difference_map()
    
    def compare_filters(self):
        """Сравнивает качество различных фильтров."""
        self.quality_manager.compare_filters(self.original_image, self.update_info)
    
    def compare_sharpness_filters(self):
        """Сравнивает различные фильтры резкости."""
        self.quality_manager.compare_sharpness_filters(self.original_image, self.update_info)
