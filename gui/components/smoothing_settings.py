"""
Компонент для настроек фильтров сглаживания.
Группирует прямоугольные, медианные, Гаусса и сигма-фильтры.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class SmoothingSettings:
    """Компонент для управления настройками фильтров сглаживания."""
    
    def __init__(self, parent_frame: ttk.Frame, on_filter_change: Callable[[str], None]):
        """
        Инициализация компонента настроек сглаживания.
        
        Args:
            parent_frame: Родительский фрейм
            on_filter_change: Callback для изменения типа фильтра
        """
        self.parent_frame = parent_frame
        self.on_filter_change = on_filter_change
        
        # Переменные для хранения значений
        self.filter_type_var = tk.StringVar(value="Прямоугольный фильтр 3x3")
        
        self._create_widgets()
        self._setup_bindings()
    
    def _setup_styles(self):
        """Настраивает стили если они не инициализированы."""
        try:
            # Проверяем, есть ли уже стили
            style = ttk.Style()
            style.configure('Modern.TLabelFrame')
        except:
            # Если стили не настроены, настраиваем их
            style = ttk.Style()
            style.theme_use('clam')
            
            # Базовые стили
            style.configure('Modern.TFrame', background='#2b2b2b')
            style.configure('Modern.TLabelFrame', 
                           background='#3c3c3c', 
                           foreground='#ffffff',
                           borderwidth=1,
                           relief='solid')
            style.configure('Modern.TLabelFrame.Label', 
                           background='#3c3c3c', 
                           foreground='#ffffff',
                           font=('Segoe UI', 10, 'bold'))
            style.configure('Modern.TLabel', 
                           background='#3c3c3c', 
                           foreground='#ffffff',
                           font=('Segoe UI', 9))
            style.configure('Modern.TButton', 
                           background='#0078d4',
                           foreground='#ffffff',
                           font=('Segoe UI', 9, 'bold'),
                           borderwidth=0,
                           focuscolor='none')
            style.configure('Modern.TCombobox',
                           fieldbackground='#3c3c3c',
                           background='#3c3c3c',
                           foreground='#ffffff',
                           borderwidth=1,
                           arrowcolor='#ffffff')
    
    def _create_widgets(self):
        """Создает виджеты настроек фильтров сглаживания."""
        # Инициализируем стили если они не настроены
        self._setup_styles()
        
        # Главный контейнер
        self.settings_container = ttk.LabelFrame(self.parent_frame, 
                                               text="🌊 Фильтры сглаживания", 
                                               style='Modern.TLabelFrame',
                                               padding="15")
        self.settings_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        self.settings_container.columnconfigure(0, weight=1)
        
        # Тип фильтра
        self.create_filter_type_section()
        
        # Описание фильтра
        self.create_description_section()
        
        # Кнопки управления
        self.create_control_buttons()
    
    def create_filter_type_section(self):
        """Создает секцию выбора типа фильтра сглаживания."""
        type_frame = ttk.LabelFrame(self.settings_container, 
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
                "Прямоугольный фильтр 3x3", "Прямоугольный фильтр 5x5",
                "Медианный фильтр 3x3", "Медианный фильтр 5x5",
                "Фильтр Гаусса σ=1.0", "Фильтр Гаусса σ=2.0", "Фильтр Гаусса σ=3.0",
                "Сигма-фильтр σ=1.0", "Сигма-фильтр σ=2.0", "Сигма-фильтр σ=3.0"
            ], 
            state="readonly", 
            style='Modern.TCombobox',
            font=('Segoe UI', 10)
        )
        filter_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    
    def create_description_section(self):
        """Создает секцию описания фильтра."""
        desc_frame = ttk.LabelFrame(self.settings_container, 
                                  text="Описание", 
                                  style='Modern.TLabelFrame',
                                  padding="10")
        desc_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        desc_frame.columnconfigure(0, weight=1)
        
        # Описание выбранного фильтра
        self.description_label = ttk.Label(desc_frame, 
                                          text="Прямоугольный фильтр 3x3 применяет усреднение по окну 3x3 для сглаживания изображения.",
                                          style='Modern.TLabel',
                                          wraplength=300,
                                          justify=tk.LEFT)
        self.description_label.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def create_control_buttons(self):
        """Создает кнопки управления."""
        buttons_frame = ttk.Frame(self.settings_container, style='Modern.TFrame')
        buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        buttons_frame.columnconfigure(0, weight=1)
        
        # Кнопка применения
        self.apply_button = ttk.Button(buttons_frame, 
                                     text="🌊 Применить фильтр сглаживания", 
                                     style='Modern.TButton',
                                     command=self.apply_filter)
        self.apply_button.grid(row=0, column=0, sticky=(tk.W, tk.E))
    
    def _setup_bindings(self):
        """Настраивает привязки событий."""
        self.filter_type_var.trace_add('write', self._on_filter_type_change)
    
    def _on_filter_type_change(self, *args):
        """Обрабатывает изменение типа фильтра."""
        filter_type = self.filter_type_var.get()
        self._update_description(filter_type)
        self.on_filter_change(filter_type)
    
    def _update_description(self, filter_type: str):
        """Обновляет описание фильтра."""
        descriptions = {
            "Прямоугольный фильтр 3x3": "Прямоугольный фильтр 3x3 применяет усреднение по окну 3x3 для сглаживания изображения.",
            "Прямоугольный фильтр 5x5": "Прямоугольный фильтр 5x5 применяет усреднение по окну 5x5 для более сильного сглаживания.",
            "Медианный фильтр 3x3": "Медианный фильтр 3x3 удаляет шум, заменяя каждый пиксель медианой в окне 3x3.",
            "Медианный фильтр 5x5": "Медианный фильтр 5x5 удаляет шум, заменяя каждый пиксель медианой в окне 5x5.",
            "Фильтр Гаусса σ=1.0": "Фильтр Гаусса с σ=1.0 применяет мягкое сглаживание с ядром 7x7 по правилу 3σ.",
            "Фильтр Гаусса σ=2.0": "Фильтр Гаусса с σ=2.0 применяет среднее сглаживание с ядром 13x13 по правилу 3σ.",
            "Фильтр Гаусса σ=3.0": "Фильтр Гаусса с σ=3.0 применяет сильное сглаживание с ядром 19x19 по правилу 3σ.",
            "Сигма-фильтр σ=1.0": "Сигма-фильтр с σ=1.0 удаляет пиксели, отклоняющиеся от среднего более чем на 1σ в окне 5x5.",
            "Сигма-фильтр σ=2.0": "Сигма-фильтр с σ=2.0 удаляет пиксели, отклоняющиеся от среднего более чем на 2σ в окне 5x5.",
            "Сигма-фильтр σ=3.0": "Сигма-фильтр с σ=3.0 удаляет пиксели, отклоняющиеся от среднего более чем на 3σ в окне 5x5."
        }
        
        self.description_label.configure(text=descriptions.get(filter_type, ""))
    
    def get_filter_parameters(self) -> Dict[str, Any]:
        """
        Возвращает параметры фильтра.
        
        Returns:
            Dict[str, Any]: Словарь с параметрами
        """
        filter_type = self.filter_type_var.get()
        return {'transform_type': filter_type}
    
    def set_apply_command(self, command: Callable):
        """Устанавливает команду для кнопки применения."""
        self.apply_button.configure(command=command)
    
    def apply_filter(self):
        """Применяет фильтр."""
        # Эта функция будет вызвана из главного окна
        pass
