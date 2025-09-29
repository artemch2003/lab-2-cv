"""
Современный компонент для настроек фильтров сглаживания.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any, Optional
import logging

from utils.validators import ParameterValidator

logger = logging.getLogger(__name__)


class ModernSmoothingSettings:
    """Современный компонент для управления настройками фильтров сглаживания."""
    
    def __init__(self, parent_frame: ttk.Frame, on_filter_change: Callable[[str], None]):
        """
        Инициализация компонента настроек сглаживания.
        
        Args:
            parent_frame: Родительский фрейм
            on_filter_change: Callback для изменения типа фильтра
        """
        self.parent_frame = parent_frame
        self.on_filter_change = on_filter_change
        self.validator = ParameterValidator()
        
        # Переменные для хранения значений
        self.filter_type_var = tk.StringVar(value="Прямоугольный фильтр 3x3")
        self.kernel_size_var = tk.StringVar(value="3x3")
        
        self._create_widgets()
        self._setup_bindings()
    
    def _create_widgets(self):
        """Создает виджеты настроек."""
        # Главный контейнер
        settings_container = ttk.LabelFrame(self.parent_frame, 
                                          text="Настройки сглаживания", 
                                          style='Modern.TLabelFrame',
                                          padding="15")
        settings_container.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        settings_container.columnconfigure(0, weight=1)
        
        # Тип фильтра
        self.create_filter_type_section(settings_container)
        
        # Параметры фильтра
        self.create_parameters_section(settings_container)
        
        # Кнопки управления
        self.create_control_buttons(settings_container)
    
    def create_filter_type_section(self, parent):
        """Создает секцию выбора типа фильтра."""
        type_frame = ttk.LabelFrame(parent, 
                                  text="Тип фильтра", 
                                  style='Modern.TLabelFrame',
                                  padding="10")
        type_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        type_frame.columnconfigure(0, weight=1)
        
        # Выбор типа фильтра
        filter_combo = ttk.Combobox(
            type_frame, 
            textvariable=self.filter_type_var,
            values=[
                "Прямоугольный фильтр 3x3",
                "Прямоугольный фильтр 5x5", 
                "Медианный фильтр 3x3",
                "Медианный фильтр 5x5"
            ], 
            state="readonly", 
            style='Modern.TCombobox',
            font=('Segoe UI', 10)
        )
        filter_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Описание выбранного фильтра
        self.description_label = ttk.Label(type_frame, 
                                          text="Прямоугольный фильтр 3x3 применяет усреднение по окну 3x3 пикселя для сглаживания изображения.",
                                          style='Modern.TLabel',
                                          wraplength=300,
                                          justify=tk.LEFT)
        self.description_label.grid(row=1, column=0, sticky=(tk.W, tk.E))
    
    def create_parameters_section(self, parent):
        """Создает секцию параметров фильтра."""
        self.parameters_frame = ttk.LabelFrame(parent, 
                                             text="Параметры", 
                                             style='Modern.TLabelFrame',
                                             padding="10")
        self.parameters_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        self.parameters_frame.columnconfigure(0, weight=1)
        
        # Размер ядра (только для информации)
        self.kernel_size_label = ttk.Label(self.parameters_frame, 
                                          text="Размер ядра:", 
                                          style='Modern.TLabel')
        self.kernel_size_label.grid(row=0, column=0, sticky=tk.W, pady=(5, 0))
        
        self.kernel_size_display = ttk.Label(self.parameters_frame, 
                                           textvariable=self.kernel_size_var,
                                           style='Modern.TLabel',
                                           font=('Segoe UI', 10, 'bold'))
        self.kernel_size_display.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Информация о фильтре
        self.info_label = ttk.Label(self.parameters_frame, 
                                  text="Фильтр автоматически применяется с выбранным размером ядра.",
                                  style='Modern.TLabel',
                                  wraplength=300,
                                  justify=tk.LEFT)
        self.info_label.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def create_control_buttons(self, parent):
        """Создает кнопки управления."""
        buttons_frame = ttk.Frame(parent, style='Modern.TFrame')
        buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        
        # Кнопка применения
        self.apply_button = ttk.Button(buttons_frame, 
                                     text="✨ Применить фильтр", 
                                     style='Modern.TButton',
                                     command=self.apply_filter)
        self.apply_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        # Кнопка предварительного просмотра
        self.preview_button = ttk.Button(buttons_frame, 
                                        text="👁 Предварительный просмотр", 
                                        style='Modern.TButton',
                                        command=self.preview_filter)
        self.preview_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 0))
    
    def _setup_bindings(self):
        """Настраивает привязки событий."""
        self.filter_type_var.trace_add('write', self._on_filter_type_change)
    
    def _on_filter_type_change(self, *args):
        """Обрабатывает изменение типа фильтра."""
        filter_type = self.filter_type_var.get()
        self._update_ui_for_filter(filter_type)
        self._update_description(filter_type)
        self.on_filter_change(filter_type)
    
    def _update_description(self, filter_type: str):
        """Обновляет описание фильтра."""
        descriptions = {
            "Прямоугольный фильтр 3x3": "Прямоугольный фильтр 3x3 применяет усреднение по окну 3x3 пикселя для сглаживания изображения.",
            "Прямоугольный фильтр 5x5": "Прямоугольный фильтр 5x5 применяет усреднение по окну 5x5 пикселя для более сильного сглаживания.",
            "Медианный фильтр 3x3": "Медианный фильтр 3x3 заменяет каждый пиксель медианой значений в окне 3x3. Эффективен против импульсного шума.",
            "Медианный фильтр 5x5": "Медианный фильтр 5x5 заменяет каждый пиксель медианой значений в окне 5x5. Обеспечивает более сильное подавление шума."
        }
        
        self.description_label.configure(text=descriptions.get(filter_type, ""))
    
    def _update_ui_for_filter(self, filter_type: str):
        """Обновляет UI для выбранного типа фильтра."""
        # Обновляем размер ядра
        if "3x3" in filter_type:
            self.kernel_size_var.set("3x3")
        elif "5x5" in filter_type:
            self.kernel_size_var.set("5x5")
        
        # Обновляем информацию
        if "Прямоугольный" in filter_type:
            self.info_label.configure(text="Прямоугольный фильтр применяет усреднение по окну для сглаживания изображения.")
        elif "Медианный" in filter_type:
            self.info_label.configure(text="Медианный фильтр заменяет каждый пиксель медианой значений в окне. Эффективен против импульсного шума.")
    
    def get_filter_parameters(self) -> Dict[str, Any]:
        """
        Возвращает параметры фильтра.
        
        Returns:
            Dict[str, Any]: Словарь с параметрами
        """
        filter_type = self.filter_type_var.get()
        
        # Извлекаем размер ядра из названия
        if "3x3" in filter_type:
            kernel_size = 3
        elif "5x5" in filter_type:
            kernel_size = 5
        else:
            kernel_size = 3
        
        params = {
            'transform_type': filter_type,
            'kernel_size': kernel_size
        }
        
        return params
    
    def set_apply_command(self, command: Callable):
        """Устанавливает команду для кнопки применения."""
        self.apply_button.configure(command=command)
    
    def apply_filter(self):
        """Применяет фильтр."""
        # Эта функция будет вызвана из главного окна
        pass
    
    def preview_filter(self):
        """Показывает предварительный просмотр фильтра."""
        # TODO: Реализовать предварительный просмотр
        pass
