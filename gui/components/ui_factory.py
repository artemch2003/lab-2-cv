"""
Фабрика для создания UI компонентов.
Устраняет дублирование кода при создании интерфейса.
"""

import tkinter as tk
from tkinter import ttk
from .base_components import (
    BaseCanvas, BaseParameterFrame, BaseInfoPanel, BaseButton, 
    BaseLabel, BaseEntry, BaseCombobox, BaseText, BaseLabelFrame
)
from constants import (
    TRANSFORM_DESCRIPTIONS, THRESHOLD_PRESETS, 
    SHARPNESS_KERNEL_SIZES, SHARPNESS_LAMBDA_VALUES,
    TRANSFORM_GROUPS
)


class UIFactory:
    """Фабрика для создания UI компонентов."""
    
    @staticmethod
    def create_image_canvas(parent, width=400, height=300):
        """Создает canvas для отображения изображений."""
        return BaseCanvas(parent, width, height)
    
    @staticmethod
    def create_parameter_frame(parent):
        """Создает фрейм для параметров."""
        return BaseParameterFrame(parent)
    
    @staticmethod
    def create_info_panel(parent, height=3):
        """Создает информационную панель."""
        return BaseInfoPanel(parent, height)
    
    @staticmethod
    def create_button(parent, text, command, style='Modern.TButton'):
        """Создает кнопку."""
        return BaseButton(parent, text, command, style)
    
    @staticmethod
    def create_label(parent, text, style='Modern.TLabel'):
        """Создает метку."""
        return BaseLabel(parent, text, style)
    
    @staticmethod
    def create_entry(parent, textvariable=None, width=15, style='Modern.TEntry'):
        """Создает поле ввода."""
        return BaseEntry(parent, textvariable, width, style)
    
    @staticmethod
    def create_combobox(parent, values, textvariable=None, width=20, style='Modern.TCombobox'):
        """Создает выпадающий список."""
        return BaseCombobox(parent, values, textvariable, width, style)
    
    @staticmethod
    def create_text(parent, height=4, width=30, style='Modern.TText'):
        """Создает текстовую область."""
        return BaseText(parent, height, width, style)
    
    @staticmethod
    def create_label_frame(parent, text, padding="10", style='Modern.TLabelFrame'):
        """Создает фрейм с заголовком."""
        return BaseLabelFrame(parent, text, padding, style)
    
    @staticmethod
    def create_transform_combobox(parent, textvariable=None):
        """Создает выпадающий список для типов преобразований."""
        # Формируем значения с видимыми заголовками групп
        transform_values = []
        for group_title, items in TRANSFORM_GROUPS.items():
            transform_values.append(group_title)
            transform_values.extend(items)
        return BaseCombobox(parent, transform_values, textvariable)
    
    @staticmethod
    def create_mode_combobox(parent, textvariable=None):
        """Создает выпадающий список для режимов."""
        mode_values = ["Автоматически", "Вручную"]
        return BaseCombobox(parent, mode_values, textvariable, width=15)
    
    @staticmethod
    def create_threshold_mode_combobox(parent, textvariable=None):
        """Создает выпадающий список для режимов порога."""
        mode_values = ["Произвольный", "Заготовленные"]
        return BaseCombobox(parent, mode_values, textvariable, width=15)
    
    @staticmethod
    def create_preset_combobox(parent, textvariable=None):
        """Создает выпадающий список для заготовленных порогов."""
        preset_values = list(THRESHOLD_PRESETS.keys())
        return BaseCombobox(parent, preset_values, textvariable, width=15)
    
    @staticmethod
    def create_outside_mode_combobox(parent, textvariable=None):
        """Создает выпадающий список для режимов вне диапазона."""
        mode_values = ["Константа", "Исходное"]
        return BaseCombobox(parent, mode_values, textvariable, width=15)
    
    @staticmethod
    def create_kernel_checkboxes(parent, callback=None):
        """Создает чекбоксы для выбора размеров ядер."""
        checkboxes = {}
        for k in SHARPNESS_KERNEL_SIZES:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(parent, text=f"k={k}", variable=var)
            cb.pack(side=tk.LEFT, padx=5)
            if callback:
                cb.configure(command=callback)
            checkboxes[k] = var
        return checkboxes
    
    @staticmethod
    def create_lambda_checkboxes(parent, callback=None):
        """Создает чекбоксы для выбора значений λ."""
        checkboxes = {}
        for lambda_val in SHARPNESS_LAMBDA_VALUES:
            var = tk.BooleanVar(value=True)
            cb = ttk.Checkbutton(parent, text=f"λ={lambda_val}", variable=var)
            cb.pack(side=tk.LEFT, padx=5)
            if callback:
                cb.configure(command=callback)
            checkboxes[lambda_val] = var
        return checkboxes
    
    @staticmethod
    def create_filter_checkboxes(parent, filters, callback=None):
        """Создает чекбоксы для выбора фильтров."""
        checkboxes = {}
        for i, filter_name in enumerate(filters):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(parent, text=filter_name, variable=var)
            cb.grid(row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
            if callback:
                cb.configure(command=callback)
            checkboxes[filter_name] = var
        return checkboxes
