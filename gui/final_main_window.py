"""
Финальная рефакторированная версия главного окна.
Использует все созданные компоненты и устраняет дублирование.
"""

import tkinter as tk
from tkinter import ttk

from constants import MESSAGES
from gui.components.ui_factory import UIFactory
from gui.components.base_components import BaseCanvas, BaseInfoPanel
from gui.styles.style_manager import StyleManager
from gui.windows.window_manager import WindowManager
from gui.parameters.parameter_manager import ParameterManager
from gui.quality.quality_manager import QualityManager
from gui.image.image_manager import ImageManager
from gui.events.event_manager import EventManager


class FinalMainWindow:
    """Финальная рефакторированная версия главного окна."""
    
    def __init__(self, root):
        """Инициализация главного окна."""
        self.root = root
        
        # Инициализация менеджеров
        self.style_manager = StyleManager()
        self.window_manager = WindowManager(root)
        self.ui_factory = UIFactory()
        self.image_manager = ImageManager(self.window_manager)
        self.parameter_manager = None
        self.quality_manager = None
        self.event_manager = None
        
        # Настройка окна
        self.window_manager.setup_main_window()
        
        # Создание интерфейса
        self.main_container = self.create_interface()
        
        # Инициализация менеджеров после создания интерфейса
        self.initialize_managers()
    
    def create_interface(self):
        """Создание интерфейса."""
        # Главный контейнер
        main_container = ttk.Frame(self.root, style='Modern.TFrame', padding="0")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        self.create_header(main_container)
        
        # Основная рабочая область
        self.create_workspace(main_container)
        
        # Создаем менеджер качества (передаем image_manager для авто-расчета карты)
        self.quality_manager = QualityManager(main_container, self.window_manager, self.image_manager)
        
        # Панель оценки качества
        self.create_quality_panel(main_container)
        
        # Нижняя панель
        self.create_bottom_panel(main_container)
        
        return main_container
    
    def initialize_managers(self):
        """Инициализирует менеджеры после создания интерфейса."""
        # Создаем менеджер параметров
        self.parameter_manager = ParameterManager(self.params_frame)
        self.parameter_manager.pack()
        
        # Менеджер качества уже создан в create_interface
        
        # Создаем менеджер событий
        self.event_manager = EventManager(
            self.parameter_manager,
            self.image_manager,
            self.quality_manager,
            self.update_info
        )

        # Инициализируем UI параметров и описание для текущего выбранного преобразования
        current_transform = self.transform_combo.get()
        self.event_manager.on_transform_change(current_transform, self.desc_text)
    
    def create_quality_panel(self, parent):
        """Создает панель оценки качества."""
        return self.quality_manager.create_quality_panel(parent)
    
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
        display_frame = self.ui_factory.create_label_frame(parent, "Изображения", padding="10")
        display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Исходное изображение
        original_frame = self.ui_factory.create_label_frame(display_frame.frame, "Исходное изображение", padding="5")
        original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.original_canvas = BaseCanvas(original_frame.frame)
        self.original_canvas.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
        self.original_canvas.display_placeholder(MESSAGES['load_placeholder'])
        
        # Обработанное изображение
        processed_frame = self.ui_factory.create_label_frame(display_frame.frame, "Обработанное изображение", padding="5")
        processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.processed_canvas = BaseCanvas(processed_frame.frame)
        self.processed_canvas.grid(sticky=(tk.W, tk.E, tk.N, tk.S))
        self.processed_canvas.display_placeholder(MESSAGES['processed_placeholder'])
    
    def create_settings_panel(self, parent):
        """Создает панель настроек."""
        settings_frame = self.ui_factory.create_label_frame(parent, "Настройки преобразования", padding="15")
        settings_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Тип преобразования
        ttk.Label(settings_frame.frame, text="Тип преобразования:", style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.transform_combo = self.ui_factory.create_transform_combobox(settings_frame.frame)
        self.transform_combo.pack(fill=tk.X, pady=(0, 10))
        # Устанавливаем первый реальный элемент (пропуская заголовок группы)
        try:
            # Найдём первый элемент, который не начинается с символа длинного тире
            for val in self.transform_combo.get().split():
                pass
        except Exception:
            pass
        self.transform_combo.set("Логарифмическое")
        self.transform_combo.bind("<<ComboboxSelected>>", self.on_transform_change)
        
        # Описание
        self.desc_text = self.ui_factory.create_text(settings_frame.frame, height=4, width=30)
        self.desc_text.pack(fill=tk.X, pady=(0, 10))
        self.desc_text.insert(1.0, "Логарифмическое преобразование улучшает видимость деталей в темных областях изображения.")
        self.desc_text.configure(state=tk.DISABLED)
        
        # Параметры
        self.params_frame = ttk.Frame(settings_frame.frame, style='Modern.TFrame')
        self.params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопка применения
        apply_btn = self.ui_factory.create_button(settings_frame.frame, "✨ Применить преобразование", self.apply_transform)
        apply_btn.pack(fill=tk.X, pady=(10, 0))
    
    def create_quality_panel(self, parent):
        """Создает панель оценки качества."""
        self.quality_panel = self.quality_manager.create_quality_panel(parent)
        # Перепривязываем команды кнопок к методам окна,
        # чтобы не требовались позиционные аргументы
        if hasattr(self.quality_manager, 'show_diff_map_btn'):
            self.quality_manager.show_diff_map_btn.configure(command=self.show_difference_map)
    
    def create_bottom_panel(self, parent):
        """Создает нижнюю панель."""
        # Информационная панель
        info_frame = self.ui_factory.create_label_frame(parent, "Информация", padding="10")
        info_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.info_panel = BaseInfoPanel(info_frame.frame, height=3)
        self.info_panel.pack(fill=tk.X)
        self.info_panel.update_info(f"Информация об изображении:\n{MESSAGES['no_image']}")
        
        # Статус бар
        self.status_var = tk.StringVar(value=MESSAGES['ready'])
        status_bar = ttk.Label(parent, textvariable=self.status_var, style='Status.TLabel')
        status_bar.pack(fill=tk.X, pady=(10, 0), padx=20)
    
    def load_image(self):
        """Загружает изображение."""
        success, message = self.event_manager.on_load_image(self.original_canvas)
        if success:
            self.status_var.set(message)
        else:
            self.status_var.set("Ошибка загрузки изображения")
    
    def save_image(self):
        """Сохраняет обработанное изображение."""
        success, message = self.event_manager.on_save_image()
        if success:
            self.status_var.set(message)
        else:
            self.status_var.set("Ошибка сохранения изображения")
    
    def reset_image(self):
        """Сбрасывает изображение к исходному состоянию."""
        success, message = self.event_manager.on_reset_image(self.processed_canvas)
        if success:
            self.status_var.set(message)
        else:
            self.status_var.set("Ошибка сброса изображения")
    
    def apply_transform(self):
        """Применяет преобразование."""
        transform_type = self.transform_combo.get()
        self.status_var.set(f"Применение {transform_type.lower()} преобразования...")
        
        success, message = self.event_manager.on_apply_transform(transform_type, self.processed_canvas)
        if success:
            self.status_var.set(message)
        else:
            self.status_var.set("Ошибка применения преобразования")
    
    def on_transform_change(self, event=None):
        """Обрабатывает изменение типа преобразования."""
        transform_type = self.transform_combo.get()
        # Если выбран заголовок группы — ничего не делаем
        try:
            from gui.parameters.parameter_manager import ParameterManager
            if ParameterManager.is_group_header(self.parameter_manager, transform_type):
                return
        except Exception:
            pass
        self.event_manager.on_transform_change(transform_type, self.desc_text)
    
    def update_info(self, message):
        """Обновляет информационную панель."""
        self.info_panel.update_info(f"Информация об изображении:\n{message}")
    
    def analyze_quality(self):
        """Анализирует качество обработки изображения."""
        self.event_manager.on_analyze_quality()
    
    def show_difference_map(self):
        """Показывает карту разности."""
        self.event_manager.on_show_difference_map()
    
    def compare_filters(self):
        """Сравнивает качество различных фильтров."""
        self.event_manager.on_compare_filters()
    
    def compare_sharpness_filters(self):
        """Сравнивает различные фильтры резкости."""
        self.event_manager.on_compare_sharpness_filters()
