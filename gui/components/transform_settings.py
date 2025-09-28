"""
Компонент для настроек преобразований.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Any, Optional
import logging

from utils.validators import ParameterValidator

logger = logging.getLogger(__name__)


class TransformSettings:
    """Компонент для управления настройками преобразований."""
    
    def __init__(self, parent_frame: ttk.Frame, on_transform_change: Callable[[str], None]):
        """
        Инициализация компонента настроек.
        
        Args:
            parent_frame: Родительский фрейм
            on_transform_change: Callback для изменения типа преобразования
        """
        self.parent_frame = parent_frame
        self.on_transform_change = on_transform_change
        self.validator = ParameterValidator()
        
        # Переменные для хранения значений
        self.transform_type_var = tk.StringVar(value="Логарифмическое")
        self.mode_var = tk.StringVar(value="Автоматически")
        self.gamma_var = tk.StringVar(value="1.0")
        self.c_var = tk.StringVar(value="1.0")
        self.threshold_var = tk.StringVar(value="128")
        self.threshold_mode_var = tk.StringVar(value="Произвольный")
        self.preset_var = tk.StringVar(value="Средний (128)")
        self.min_brightness_var = tk.StringVar(value="0")
        self.max_brightness_var = tk.StringVar(value="255")
        self.outside_mode_var = tk.StringVar(value="Константа")
        self.constant_value_var = tk.StringVar(value="0")
        
        self._create_widgets()
        self._setup_bindings()
    
    def _create_widgets(self):
        """Создает виджеты настроек."""
        # Тип преобразования
        ttk.Label(self.parent_frame, text="Тип преобразования:").grid(row=0, column=0, sticky=tk.W)
        transform_combo = ttk.Combobox(
            self.parent_frame, 
            textvariable=self.transform_type_var,
            values=["Логарифмическое", "Степенное", "Бинарное", "Вырезание диапазона яркостей"], 
            state="readonly", 
            width=15
        )
        transform_combo.grid(row=0, column=1, padx=(5, 0))
        
        # Режим настройки
        self.mode_label = ttk.Label(self.parent_frame, text="Режим:")
        self.mode_var = tk.StringVar(value="Автоматически")
        self.mode_combo = ttk.Combobox(
            self.parent_frame, 
            textvariable=self.mode_var,
            values=["Автоматически", "Вручную"], 
            state="readonly", 
            width=12
        )
        
        # Коэффициент c
        self.c_label = ttk.Label(self.parent_frame, text="Коэффициент c:")
        self.c_var = tk.StringVar(value="1.0")
        self.c_entry = ttk.Entry(self.parent_frame, textvariable=self.c_var, width=15)
        
        # Гамма
        self.gamma_label = ttk.Label(self.parent_frame, text="Гамма γ:")
        self.gamma_var = tk.StringVar(value="1.0")
        self.gamma_entry = ttk.Entry(self.parent_frame, textvariable=self.gamma_var, width=15)
        
        # Пороговое значение
        self.threshold_mode_label = ttk.Label(self.parent_frame, text="Режим порога:")
        self.threshold_mode_combo = ttk.Combobox(
            self.parent_frame, 
            textvariable=self.threshold_mode_var,
            values=["Произвольный", "Заготовленные"], 
            state="readonly", 
            width=15
        )
        
        self.threshold_label = ttk.Label(self.parent_frame, text="Порог:")
        self.threshold_entry = ttk.Entry(self.parent_frame, textvariable=self.threshold_var, width=15)
        
        # Заготовленные пороги
        self.preset_label = ttk.Label(self.parent_frame, text="Заготовка:")
        self.preset_combo = ttk.Combobox(
            self.parent_frame, 
            textvariable=self.preset_var,
            values=["Очень светлый (64)", "Светлый (96)", "Средний (128)", 
                   "Темный (160)", "Очень темный (192)", "Максимально темный (224)"],
            state="readonly", 
            width=15
        )
        
        # Элементы для вырезания диапазона яркостей
        self.min_brightness_label = ttk.Label(self.parent_frame, text="Мин. яркость:")
        self.min_brightness_entry = ttk.Entry(self.parent_frame, textvariable=self.min_brightness_var, width=15)
        
        self.max_brightness_label = ttk.Label(self.parent_frame, text="Макс. яркость:")
        self.max_brightness_entry = ttk.Entry(self.parent_frame, textvariable=self.max_brightness_var, width=15)
        
        self.outside_mode_label = ttk.Label(self.parent_frame, text="Режим вне диапазона:")
        self.outside_mode_combo = ttk.Combobox(
            self.parent_frame, 
            textvariable=self.outside_mode_var,
            values=["Константа", "Исходное"], 
            state="readonly", 
            width=15
        )
        
        self.constant_value_label = ttk.Label(self.parent_frame, text="Константа:")
        self.constant_value_entry = ttk.Entry(self.parent_frame, textvariable=self.constant_value_var, width=15)
        
        # Кнопка применения
        self.apply_button = ttk.Button(self.parent_frame, text="Применить")
        self.apply_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def _setup_bindings(self):
        """Настраивает привязки событий."""
        self.transform_type_var.trace('w', self._on_transform_type_change)
        self.mode_var.trace('w', self._on_mode_change)
        self.threshold_mode_var.trace('w', self._on_threshold_mode_change)
        self.preset_var.trace('w', self._on_preset_change)
        self.outside_mode_var.trace('w', self._on_outside_mode_change)
    
    def _on_transform_type_change(self, *args):
        """Обрабатывает изменение типа преобразования."""
        transform_type = self.transform_type_var.get()
        self._update_ui_for_transform(transform_type)
        self.on_transform_change(transform_type)
    
    def _on_mode_change(self, *args):
        """Обрабатывает изменение режима настройки."""
        transform_type = self.transform_type_var.get()
        mode = self.mode_var.get()
        self._update_ui_for_mode(transform_type, mode)
    
    def _on_threshold_mode_change(self, *args):
        """Обрабатывает изменение режима порога."""
        mode = self.threshold_mode_var.get()
        self._update_ui_for_threshold_mode(mode)
    
    def _on_preset_change(self, *args):
        """Обрабатывает изменение заготовки порога."""
        preset = self.preset_var.get()
        threshold = self._get_threshold_from_preset(preset)
        self.threshold_var.set(str(threshold))
    
    def _on_outside_mode_change(self, *args):
        """Обрабатывает изменение режима обработки пикселей вне диапазона."""
        mode = self.outside_mode_var.get()
        self._update_ui_for_outside_mode(mode)
    
    def _update_ui_for_transform(self, transform_type: str):
        """Обновляет UI для выбранного типа преобразования."""
        # Скрываем все элементы
        self._hide_all_elements()
        
        if transform_type == "Степенное":
            self._show_power_transform_elements()
        elif transform_type == "Бинарное":
            self._show_binary_transform_elements()
        elif transform_type == "Вырезание диапазона яркостей":
            self._show_brightness_range_elements()
        else:  # Логарифмическое
            self._show_logarithmic_transform_elements()
    
    def _update_ui_for_mode(self, transform_type: str, mode: str):
        """Обновляет UI для выбранного режима."""
        if transform_type == "Степенное":
            if mode == "Вручную":
                self.gamma_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
                self.gamma_entry.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
            else:
                self.gamma_label.grid_remove()
                self.gamma_entry.grid_remove()
        elif transform_type == "Логарифмическое":
            if mode == "Вручную":
                self.c_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
                self.c_entry.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
            else:
                self.c_label.grid_remove()
                self.c_entry.grid_remove()
    
    def _update_ui_for_threshold_mode(self, mode: str):
        """Обновляет UI для режима порога."""
        if mode == "Произвольный":
            self.threshold_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
            self.threshold_entry.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
            self.preset_label.grid_remove()
            self.preset_combo.grid_remove()
        else:  # Заготовленные
            self.threshold_label.grid_remove()
            self.threshold_entry.grid_remove()
            self.preset_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
            self.preset_combo.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
    
    def _update_ui_for_outside_mode(self, mode: str):
        """Обновляет UI для режима обработки пикселей вне диапазона."""
        if mode == "Константа":
            self.constant_value_label.grid(row=5, column=0, sticky=tk.W, pady=(5, 0))
            self.constant_value_entry.grid(row=5, column=1, padx=(5, 0), pady=(5, 0))
            self.apply_button.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        else:  # Исходное
            self.constant_value_label.grid_remove()
            self.constant_value_entry.grid_remove()
            self.apply_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
    
    def _hide_all_elements(self):
        """Скрывает все элементы настроек."""
        elements = [
            self.mode_label, self.mode_combo,
            self.c_label, self.c_entry,
            self.gamma_label, self.gamma_entry,
            self.threshold_label, self.threshold_entry,
            self.threshold_mode_label, self.threshold_mode_combo,
            self.preset_label, self.preset_combo,
            self.min_brightness_label, self.min_brightness_entry,
            self.max_brightness_label, self.max_brightness_entry,
            self.outside_mode_label, self.outside_mode_combo,
            self.constant_value_label, self.constant_value_entry
        ]
        
        for element in elements:
            element.grid_remove()
    
    def _show_logarithmic_transform_elements(self):
        """Показывает элементы для логарифмического преобразования."""
        self.mode_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.mode_combo.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
        self.apply_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        self._update_ui_for_mode("Логарифмическое", self.mode_var.get())
    
    def _show_power_transform_elements(self):
        """Показывает элементы для степенного преобразования."""
        self.mode_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.mode_combo.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
        self.apply_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        self._update_ui_for_mode("Степенное", self.mode_var.get())
    
    def _show_binary_transform_elements(self):
        """Показывает элементы для бинарного преобразования."""
        self.threshold_mode_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.threshold_mode_combo.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
        self.apply_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        self._update_ui_for_threshold_mode(self.threshold_mode_var.get())
    
    def _show_brightness_range_elements(self):
        """Показывает элементы для вырезания диапазона яркостей."""
        self.min_brightness_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.min_brightness_entry.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
        self.max_brightness_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.max_brightness_entry.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
        self.outside_mode_label.grid(row=4, column=0, sticky=tk.W, pady=(5, 0))
        self.outside_mode_combo.grid(row=4, column=1, padx=(5, 0), pady=(5, 0))
        self.apply_button.grid(row=7, column=0, columnspan=2, pady=(10, 0))
        self._update_ui_for_outside_mode(self.outside_mode_var.get())
    
    def _get_threshold_from_preset(self, preset: str) -> int:
        """Извлекает пороговое значение из названия заготовки."""
        if "Очень светлый" in preset:
            return 64
        elif "Светлый" in preset:
            return 96
        elif "Средний" in preset:
            return 128
        elif "Темный" in preset:
            return 160
        elif "Очень темный" in preset:
            return 192
        elif "Максимально темный" in preset:
            return 224
        else:
            return 128
    
    def get_transform_parameters(self) -> Dict[str, Any]:
        """
        Возвращает параметры преобразования.
        
        Returns:
            Dict[str, Any]: Словарь с параметрами
        """
        transform_type = self.transform_type_var.get()
        params = {'transform_type': transform_type}
        
        if transform_type == "Логарифмическое":
            mode = self.mode_var.get()
            params['mode'] = mode
            if mode == "Вручную":
                try:
                    params['c'] = self.validator.validate_positive_float(self.c_var.get(), "коэффициент c")
                except ValueError as e:
                    raise ValueError(f"Неверное значение коэффициента: {e}")
        
        elif transform_type == "Степенное":
            mode = self.mode_var.get()
            params['mode'] = mode
            if mode == "Вручную":
                try:
                    params['gamma'] = self.validator.validate_positive_float(self.gamma_var.get(), "гамма")
                except ValueError as e:
                    raise ValueError(f"Неверное значение гаммы: {e}")
        
        elif transform_type == "Бинарное":
            mode = self.threshold_mode_var.get()
            params['threshold_mode'] = mode
            if mode == "Произвольный":
                try:
                    params['threshold'] = self.validator.validate_threshold(self.threshold_var.get())
                except ValueError as e:
                    raise ValueError(f"Неверное значение порога: {e}")
            else:  # Заготовленные
                params['threshold'] = self._get_threshold_from_preset(self.preset_var.get())
        
        elif transform_type == "Вырезание диапазона яркостей":
            try:
                min_brightness, max_brightness = self.validator.validate_brightness_range(
                    self.min_brightness_var.get(), 
                    self.max_brightness_var.get()
                )
                params['min_brightness'] = min_brightness
                params['max_brightness'] = max_brightness
                params['outside_mode'] = self.outside_mode_var.get()
                
                if params['outside_mode'] == "Константа":
                    params['constant_value'] = self.validator.validate_threshold(self.constant_value_var.get())
            except ValueError as e:
                raise ValueError(f"Неверные параметры диапазона: {e}")
        
        return params
    
    def set_apply_command(self, command: Callable):
        """Устанавливает команду для кнопки применения."""
        self.apply_button.configure(command=command)
