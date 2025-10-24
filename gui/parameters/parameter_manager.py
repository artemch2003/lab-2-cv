"""
Менеджер параметров для приложения.
Содержит логику управления параметрами преобразований.
"""

import tkinter as tk
from constants import (
    DEFAULT_PARAMS, THRESHOLD_PRESETS, TRANSFORM_DESCRIPTIONS,
    SHARPNESS_KERNEL_SIZES, SHARPNESS_LAMBDA_VALUES
)
from gui.components.ui_factory import UIFactory


class ParameterManager:
    """Менеджер параметров для управления настройками преобразований."""
    
    def __init__(self, parent):
        self.parent = parent
        self.ui_factory = UIFactory()
        self.variables = {}
        self.elements = {}
        self._create_variables()
        self._create_elements()
    
    def pack(self, **kwargs):
        """Упаковывает фрейм параметров."""
        # ParameterManager не имеет своего фрейма, элементы создаются напрямую в parent
        pass
    
    def _create_variables(self):
        """Создает переменные для параметров."""
        self.variables = {
            'mode': tk.StringVar(value="Автоматически"),
            'gamma': tk.StringVar(value=str(DEFAULT_PARAMS['gamma'])),
            'c_coefficient': tk.StringVar(value=str(DEFAULT_PARAMS['c_coefficient'])),
            'threshold': tk.StringVar(value=str(DEFAULT_PARAMS['threshold'])),
            'threshold_mode': tk.StringVar(value="Произвольный"),
            'preset': tk.StringVar(value="Средний (128)"),
            'min_brightness': tk.StringVar(value=str(DEFAULT_PARAMS['min_brightness'])),
            'max_brightness': tk.StringVar(value=str(DEFAULT_PARAMS['max_brightness'])),
            'outside_mode': tk.StringVar(value="Константа"),
            'constant_value': tk.StringVar(value=str(DEFAULT_PARAMS['constant_value']))
        }
    
    def _create_elements(self):
        """Создает элементы интерфейса для параметров."""
        # Режим
        self.elements['mode_label'] = self.ui_factory.create_label(
            self.parent, "Режим:"
        )
        self.elements['mode_combo'] = self.ui_factory.create_mode_combobox(
            self.parent, self.variables['mode']
        )
        # Привязываем событие изменения режима
        self.elements['mode_combo'].bind('<<ComboboxSelected>>', lambda e: self._on_mode_change())
        
        # Гамма
        self.elements['gamma_label'] = self.ui_factory.create_label(
            self.parent, "Гамма:"
        )
        self.elements['gamma_entry'] = self.ui_factory.create_entry(
            self.parent, self.variables['gamma'], width=15
        )
        
        # Коэффициент c
        self.elements['c_label'] = self.ui_factory.create_label(
            self.parent, "Коэффициент c:"
        )
        self.elements['c_entry'] = self.ui_factory.create_entry(
            self.parent, self.variables['c_coefficient'], width=15
        )
        
        # Режим порога
        self.elements['threshold_mode_label'] = self.ui_factory.create_label(
            self.parent, "Режим порога:"
        )
        self.elements['threshold_mode_combo'] = self.ui_factory.create_threshold_mode_combobox(
            self.parent, self.variables['threshold_mode']
        )
        # Привязываем событие изменения режима порога
        self.elements['threshold_mode_combo'].bind('<<ComboboxSelected>>', lambda e: self._on_threshold_mode_change())
        
        # Порог
        self.elements['threshold_label'] = self.ui_factory.create_label(
            self.parent, "Порог:"
        )
        self.elements['threshold_entry'] = self.ui_factory.create_entry(
            self.parent, self.variables['threshold'], width=15
        )
        
        # Заготовленные пороги
        self.elements['preset_label'] = self.ui_factory.create_label(
            self.parent, "Заготовка:"
        )
        self.elements['preset_combo'] = self.ui_factory.create_preset_combobox(
            self.parent, self.variables['preset']
        )
        # Привязываем событие изменения заготовки
        self.elements['preset_combo'].bind('<<ComboboxSelected>>', lambda e: self.on_preset_change())
        
        # Минимальная яркость
        self.elements['min_brightness_label'] = self.ui_factory.create_label(
            self.parent, "Мин. яркость:"
        )
        self.elements['min_brightness_entry'] = self.ui_factory.create_entry(
            self.parent, self.variables['min_brightness'], width=15
        )
        
        # Максимальная яркость
        self.elements['max_brightness_label'] = self.ui_factory.create_label(
            self.parent, "Макс. яркость:"
        )
        self.elements['max_brightness_entry'] = self.ui_factory.create_entry(
            self.parent, self.variables['max_brightness'], width=15
        )
        
        # Режим вне диапазона
        self.elements['outside_mode_label'] = self.ui_factory.create_label(
            self.parent, "Режим вне диапазона:"
        )
        self.elements['outside_mode_combo'] = self.ui_factory.create_outside_mode_combobox(
            self.parent, self.variables['outside_mode']
        )
        # Привязываем событие изменения режима вне диапазона
        self.elements['outside_mode_combo'].bind('<<ComboboxSelected>>', lambda e: self._on_outside_mode_change())
        
        # Константа
        self.elements['constant_value_label'] = self.ui_factory.create_label(
            self.parent, "Константа:"
        )
        self.elements['constant_value_entry'] = self.ui_factory.create_entry(
            self.parent, self.variables['constant_value'], width=15
        )
    
    def hide_all_elements(self):
        """Скрывает все элементы параметров."""
        for element in self.elements.values():
            if hasattr(element, 'pack_forget'):
                element.pack_forget()
    
    def show_elements_for_transform(self, transform_type):
        """Показывает элементы для указанного типа преобразования."""
        self.hide_all_elements()
        self.set_current_transform_type(transform_type)
        
        if transform_type == "Логарифмическое":
            self._show_logarithmic_elements()
        elif transform_type == "Степенное":
            self._show_power_elements()
        elif transform_type == "Бинарное":
            self._show_binary_elements()
        elif transform_type == "Вырезание диапазона яркостей":
            self._show_brightness_range_elements()
    
    def _show_logarithmic_elements(self):
        """Показывает элементы для логарифмического преобразования."""
        self.elements['mode_label'].pack(anchor=tk.W, pady=(5, 0))
        self.elements['mode_combo'].pack(anchor=tk.W, pady=(0, 5))
        self._on_mode_change()
    
    def _show_power_elements(self):
        """Показывает элементы для степенного преобразования."""
        # По заданию: для степенного вводится только γ, коэффициент c подбирается автоматически.
        # Поля режима и c скрываем.
        if hasattr(self.elements['mode_label'], 'pack_forget'):
            self.elements['mode_label'].pack_forget()
        if hasattr(self.elements['mode_combo'], 'pack_forget'):
            self.elements['mode_combo'].pack_forget()
        self.elements['gamma_label'].pack(anchor=tk.W, pady=(5, 0))
        self.elements['gamma_entry'].pack(anchor=tk.W, pady=(0, 5))
    
    def _show_binary_elements(self):
        """Показывает элементы для бинарного преобразования."""
        self.elements['threshold_mode_label'].pack(anchor=tk.W, pady=(5, 0))
        self.elements['threshold_mode_combo'].pack(anchor=tk.W, pady=(0, 5))
        self._on_threshold_mode_change()
    
    def _show_brightness_range_elements(self):
        """Показывает элементы для вырезания диапазона яркостей."""
        self.elements['min_brightness_label'].pack(anchor=tk.W, pady=(5, 0))
        self.elements['min_brightness_entry'].pack(anchor=tk.W, pady=(0, 5))
        self.elements['max_brightness_label'].pack(anchor=tk.W, pady=(5, 0))
        self.elements['max_brightness_entry'].pack(anchor=tk.W, pady=(0, 5))
        self.elements['outside_mode_label'].pack(anchor=tk.W, pady=(5, 0))
        self.elements['outside_mode_combo'].pack(anchor=tk.W, pady=(0, 5))
        self._on_outside_mode_change()
    
    def _on_mode_change(self):
        """Обрабатывает изменение режима."""
        mode = self.variables['mode'].get()
        transform_type = self._get_current_transform_type()
        
        if transform_type == "Логарифмическое":
            # В ручном режиме показываем c, в автоматическом скрываем c
            if mode == "Вручную":
                self.elements['c_label'].pack(anchor=tk.W, pady=(5, 0))
                self.elements['c_entry'].pack(anchor=tk.W, pady=(0, 5))
            else:
                self.elements['c_label'].pack_forget()
                self.elements['c_entry'].pack_forget()
            # Поля γ для логарифмического не используются
            self.elements['gamma_label'].pack_forget()
            self.elements['gamma_entry'].pack_forget()
        elif transform_type == "Степенное":
            # Для степенного всегда показываем γ; режим и c не используются
            self.elements['gamma_label'].pack(anchor=tk.W, pady=(5, 0))
            self.elements['gamma_entry'].pack(anchor=tk.W, pady=(0, 5))
            self.elements['c_label'].pack_forget()
            self.elements['c_entry'].pack_forget()
            if hasattr(self.elements['mode_label'], 'pack_forget'):
                self.elements['mode_label'].pack_forget()
            if hasattr(self.elements['mode_combo'], 'pack_forget'):
                self.elements['mode_combo'].pack_forget()
        else:
            # Для остальных типов скрываем специфичные поля
            self.elements['gamma_label'].pack_forget()
            self.elements['gamma_entry'].pack_forget()
            self.elements['c_label'].pack_forget()
            self.elements['c_entry'].pack_forget()
    
    def _on_threshold_mode_change(self):
        """Обрабатывает изменение режима порога."""
        mode = self.variables['threshold_mode'].get()
        
        if mode == "Произвольный":
            self.elements['threshold_label'].pack(anchor=tk.W, pady=(5, 0))
            self.elements['threshold_entry'].pack(anchor=tk.W, pady=(0, 5))
            self.elements['preset_label'].pack_forget()
            self.elements['preset_combo'].pack_forget()
        else:  # Заготовленные
            self.elements['preset_label'].pack(anchor=tk.W, pady=(5, 0))
            self.elements['preset_combo'].pack(anchor=tk.W, pady=(0, 5))
            self.elements['threshold_label'].pack_forget()
            self.elements['threshold_entry'].pack_forget()
    
    def _on_outside_mode_change(self):
        """Обрабатывает изменение режима вне диапазона."""
        mode = self.variables['outside_mode'].get()
        
        if mode == "Константа":
            self.elements['constant_value_label'].pack(anchor=tk.W, pady=(5, 0))
            self.elements['constant_value_entry'].pack(anchor=tk.W, pady=(0, 5))
        else:
            self.elements['constant_value_label'].pack_forget()
            self.elements['constant_value_entry'].pack_forget()
    
    def _get_current_transform_type(self):
        """Возвращает текущий тип преобразования."""
        # Это должно быть передано из главного окна
        return getattr(self, '_current_transform_type', "Логарифмическое")
    
    def set_current_transform_type(self, transform_type):
        """Устанавливает текущий тип преобразования."""
        self._current_transform_type = transform_type
    
    def on_preset_change(self):
        """Обрабатывает изменение заготовки порога."""
        preset = self.variables['preset'].get()
        threshold = THRESHOLD_PRESETS.get(preset, 128)
        self.variables['threshold'].set(str(threshold))

    def is_group_header(self, value: str) -> bool:
        """Возвращает True, если элемент в комбобоксе — заголовок группы."""
        return isinstance(value, str) and value.strip().startswith("—")
    
    def get_parameters(self, transform_type):
        """Возвращает параметры для указанного типа преобразования."""
        params = {'transform_type': transform_type}
        
        if transform_type == "Логарифмическое":
            mode = self.variables['mode'].get()
            params['mode'] = mode
            if mode == "Вручную":
                try:
                    params['c'] = float(self.variables['c_coefficient'].get())
                except ValueError:
                    raise ValueError("Неверное значение коэффициента c")
        
        elif transform_type == "Степенное":
            # Вводится только γ; коэффициент c подбирается автоматически в алгоритме
            try:
                params['gamma'] = float(self.variables['gamma'].get())
            except ValueError:
                raise ValueError("Неверное значение гаммы")
        
        elif transform_type == "Бинарное":
            mode = self.variables['threshold_mode'].get()
            params['threshold_mode'] = mode
            if mode == "Произвольный":
                try:
                    params['threshold'] = int(self.variables['threshold'].get())
                except ValueError:
                    raise ValueError("Неверное значение порога")
            else:  # Заготовленные
                preset = self.variables['preset'].get()
                params['threshold'] = THRESHOLD_PRESETS.get(preset, 128)
        
        elif transform_type == "Вырезание диапазона яркостей":
            try:
                params['min_brightness'] = int(self.variables['min_brightness'].get())
                params['max_brightness'] = int(self.variables['max_brightness'].get())
                params['outside_mode'] = self.variables['outside_mode'].get()
                if self.variables['outside_mode'].get() == "Константа":
                    params['constant_value'] = int(self.variables['constant_value'].get())
            except ValueError:
                raise ValueError("Неверные значения параметров яркости")
        
        return params
    
    def format_parameters_info(self, params):
        """Форматирует информацию о параметрах для отображения."""
        transform_type = params['transform_type']
        info_lines = []
        
        if transform_type == "Логарифмическое":
            mode = params.get('mode', 'Автоматически')
            info_lines.append(f"Режим: {mode}")
            if mode == "Вручную" and 'c' in params:
                info_lines.append(f"Коэффициент c: {params['c']}")
        
        elif transform_type == "Степенное":
            if 'gamma' in params:
                info_lines.append(f"Гамма: {params['gamma']}")
        
        elif transform_type == "Бинарное":
            mode = params.get('threshold_mode', 'Произвольный')
            info_lines.append(f"Режим порога: {mode}")
            if 'threshold' in params:
                info_lines.append(f"Порог: {params['threshold']}")
        
        elif transform_type == "Вырезание диапазона яркостей":
            info_lines.append(f"Диапазон: {params.get('min_brightness', 0)} - {params.get('max_brightness', 255)}")
            info_lines.append(f"Режим вне диапазона: {params.get('outside_mode', 'Константа')}")
            if params.get('outside_mode') == "Константа" and 'constant_value' in params:
                info_lines.append(f"Константа: {params['constant_value']}")
        
        elif transform_type in ["Прямоугольный фильтр 3x3", "Прямоугольный фильтр 5x5", 
                               "Медианный фильтр 3x3", "Медианный фильтр 5x5",
                               "Фильтр Гаусса σ=1.0", "Фильтр Гаусса σ=2.0", "Фильтр Гаусса σ=3.0",
                               "Сигма-фильтр σ=1.0", "Сигма-фильтр σ=2.0", "Сигма-фильтр σ=3.0"]:
            info_lines.append("Фильтр сглаживания применен")
        elif transform_type.startswith("Нерезкое маскирование"):
            info_lines.append("Фильтр резкости применен")
        
        return "\n".join(info_lines) if info_lines else "Параметры не заданы"
