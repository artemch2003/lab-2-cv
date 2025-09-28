"""
Компонент информационной панели.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class InfoPanel:
    """Компонент информационной панели."""
    
    def __init__(self, parent_frame: ttk.Frame):
        """
        Инициализация информационной панели.
        
        Args:
            parent_frame: Родительский фрейм
        """
        self.parent_frame = parent_frame
        self._create_widgets()
    
    def _create_widgets(self):
        """Создает виджеты информационной панели."""
        # Информационная панель
        info_frame = ttk.LabelFrame(self.parent_frame, text="Информация", padding="10")
        info_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=4, width=80, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
    
    def update_info(self, info: Dict[str, Any]):
        """
        Обновляет информацию в панели.
        
        Args:
            info: Словарь с информацией об изображении
        """
        info_text = "Информация об изображении:\n"
        
        if info:
            info_text += f"Размер: {info.get('size', 'Неизвестно')}\n"
            info_text += f"Режим: {info.get('mode', 'Неизвестно')}\n"
            info_text += f"Формат: {info.get('format', 'Неизвестно')}\n"
            info_text += f"Обработано: {'Да' if info.get('has_processed', False) else 'Нет'}\n"
            
            # Добавляем информацию о преобразовании
            if 'transform_name' in info:
                info_text += f"Преобразование: {info.get('transform_name')}\n"
            
            # Добавляем информацию о параметрах
            if 'detailed_parameters' in info:
                params = info['detailed_parameters']
                for key, value in params.items():
                    if key == 'c':
                        info_text += f"Коэффициент c: {round(value, 4)}\n"
                    elif key == 'gamma':
                        info_text += f"Гамма γ: {round(value, 4)}\n"
                    elif key == 'threshold':
                        info_text += f"Порог: {round(value, 1)}\n"
                    elif key == 'min_brightness':
                        info_text += f"Мин. яркость: {round(value, 1)}\n"
                    elif key == 'max_brightness':
                        info_text += f"Макс. яркость: {round(value, 1)}\n"
                    elif key == 'outside_mode':
                        info_text += f"Режим вне диапазона: {value}\n"
                    elif key == 'constant_value' and value is not None:
                        info_text += f"Константа: {round(value, 1)}\n"
        else:
            info_text += "Изображение не загружено"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_text)
    
    def clear_info(self):
        """Очищает информационную панель."""
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, "Информация об изображении:\nИзображение не загружено")
