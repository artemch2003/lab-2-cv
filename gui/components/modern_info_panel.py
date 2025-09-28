"""
Современная информационная панель в стиле фоторедактора.
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ModernInfoPanel:
    """Современная информационная панель."""
    
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
        # Главный контейнер
        info_container = ttk.LabelFrame(self.parent_frame, 
                                      text="Информация об изображении", 
                                      style='Modern.TLabelFrame',
                                      padding="15")
        info_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_container.columnconfigure(0, weight=1)
        info_container.rowconfigure(0, weight=1)
        
        # Создаем notebook для вкладок
        self.notebook = ttk.Notebook(info_container)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Вкладка основной информации
        self.create_basic_info_tab()
        
        # Вкладка параметров преобразования
        self.create_transform_info_tab()
        
        # Вкладка статистики
        self.create_statistics_tab()
    
    def create_basic_info_tab(self):
        """Создает вкладку основной информации."""
        basic_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(basic_frame, text="📊 Основная информация")
        basic_frame.columnconfigure(1, weight=1)
        
        # Информационные метки
        self.basic_info_labels = {}
        
        # Размер изображения
        ttk.Label(basic_frame, text="Размер:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.basic_info_labels['size'] = ttk.Label(basic_frame, text="Не загружено", style='Modern.TLabel')
        self.basic_info_labels['size'].grid(row=0, column=1, sticky=tk.W)
        
        # Формат
        ttk.Label(basic_frame, text="Формат:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.basic_info_labels['format'] = ttk.Label(basic_frame, text="Не загружено", style='Modern.TLabel')
        self.basic_info_labels['format'].grid(row=1, column=1, sticky=tk.W)
        
        # Режим
        ttk.Label(basic_frame, text="Режим:", style='Modern.TLabel').grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.basic_info_labels['mode'] = ttk.Label(basic_frame, text="Не загружено", style='Modern.TLabel')
        self.basic_info_labels['mode'].grid(row=2, column=1, sticky=tk.W)
        
        # Размер файла
        ttk.Label(basic_frame, text="Размер файла:", style='Modern.TLabel').grid(row=3, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.basic_info_labels['file_size'] = ttk.Label(basic_frame, text="Не загружено", style='Modern.TLabel')
        self.basic_info_labels['file_size'].grid(row=3, column=1, sticky=tk.W)
        
        # Статус обработки
        ttk.Label(basic_frame, text="Статус:", style='Modern.TLabel').grid(row=4, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.basic_info_labels['status'] = ttk.Label(basic_frame, text="Не загружено", style='Modern.TLabel')
        self.basic_info_labels['status'].grid(row=4, column=1, sticky=tk.W)
    
    def create_transform_info_tab(self):
        """Создает вкладку информации о преобразовании."""
        transform_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(transform_frame, text="⚙️ Параметры преобразования")
        transform_frame.columnconfigure(1, weight=1)
        
        # Информация о преобразовании
        self.transform_info_labels = {}
        
        # Тип преобразования
        ttk.Label(transform_frame, text="Тип преобразования:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.transform_info_labels['transform_name'] = ttk.Label(transform_frame, text="Не применено", style='Modern.TLabel')
        self.transform_info_labels['transform_name'].grid(row=0, column=1, sticky=tk.W)
        
        # Параметры преобразования
        self.parameters_text = tk.Text(transform_frame, 
                                     height=8, 
                                     width=40, 
                                     wrap=tk.WORD,
                                     style='Modern.TText',
                                     state=tk.DISABLED)
        self.parameters_text.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Скроллбар для текста параметров
        parameters_scrollbar = ttk.Scrollbar(transform_frame, 
                                           orient=tk.VERTICAL, 
                                           command=self.parameters_text.yview)
        parameters_scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S), pady=(10, 0))
        self.parameters_text.configure(yscrollcommand=parameters_scrollbar.set)
        
        transform_frame.rowconfigure(1, weight=1)
    
    def create_statistics_tab(self):
        """Создает вкладку статистики."""
        stats_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(stats_frame, text="📈 Статистика")
        stats_frame.columnconfigure(1, weight=1)
        
        # Статистические метки
        self.stats_labels = {}
        
        # Средняя яркость
        ttk.Label(stats_frame, text="Средняя яркость:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.stats_labels['avg_brightness'] = ttk.Label(stats_frame, text="Не рассчитано", style='Modern.TLabel')
        self.stats_labels['avg_brightness'].grid(row=0, column=1, sticky=tk.W)
        
        # Контрастность
        ttk.Label(stats_frame, text="Контрастность:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=2)
        self.stats_labels['contrast'] = ttk.Label(stats_frame, text="Не рассчитано", style='Modern.TLabel')
        self.stats_labels['contrast'].grid(row=1, column=1, sticky=tk.W)
        
        # Гистограмма (текстовое представление)
        ttk.Label(stats_frame, text="Гистограмма:", style='Modern.TLabel').grid(row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 2))
        
        self.histogram_text = tk.Text(stats_frame, 
                                     height=6, 
                                     width=40, 
                                     wrap=tk.WORD,
                                     style='Modern.TText',
                                     state=tk.DISABLED)
        self.histogram_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Скроллбар для гистограммы
        histogram_scrollbar = ttk.Scrollbar(stats_frame, 
                                          orient=tk.VERTICAL, 
                                          command=self.histogram_text.yview)
        histogram_scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.histogram_text.configure(yscrollcommand=histogram_scrollbar.set)
        
        stats_frame.rowconfigure(3, weight=1)
    
    def update_info(self, info: Dict[str, Any]):
        """
        Обновляет информацию в панели.
        
        Args:
            info: Словарь с информацией об изображении
        """
        if not info:
            self._clear_all_info()
            return
        
        # Обновляем основную информацию
        self._update_basic_info(info)
        
        # Обновляем информацию о преобразовании
        self._update_transform_info(info)
        
        # Обновляем статистику
        self._update_statistics(info)
    
    def _clear_all_info(self):
        """Очищает всю информацию."""
        # Очищаем основную информацию
        for label in self.basic_info_labels.values():
            label.configure(text="Не загружено")
        
        # Очищаем информацию о преобразовании
        for label in self.transform_info_labels.values():
            label.configure(text="Не применено")
        
        self.parameters_text.configure(state=tk.NORMAL)
        self.parameters_text.delete(1.0, tk.END)
        self.parameters_text.configure(state=tk.DISABLED)
        
        # Очищаем статистику
        for label in self.stats_labels.values():
            label.configure(text="Не рассчитано")
        
        self.histogram_text.configure(state=tk.NORMAL)
        self.histogram_text.delete(1.0, tk.END)
        self.histogram_text.configure(state=tk.DISABLED)
    
    def _update_basic_info(self, info: Dict[str, Any]):
        """Обновляет основную информацию."""
        self.basic_info_labels['size'].configure(text=info.get('size', 'Неизвестно'))
        self.basic_info_labels['format'].configure(text=info.get('format', 'Неизвестно'))
        self.basic_info_labels['mode'].configure(text=info.get('mode', 'Неизвестно'))
        self.basic_info_labels['file_size'].configure(text=info.get('file_size', 'Неизвестно'))
        self.basic_info_labels['status'].configure(text='Обработано' if info.get('has_processed', False) else 'Не обработано')
    
    def _update_transform_info(self, info: Dict[str, Any]):
        """Обновляет информацию о преобразовании."""
        transform_name = info.get('transform_name', 'Не применено')
        self.transform_info_labels['transform_name'].configure(text=transform_name)
        
        # Обновляем параметры преобразования
        self.parameters_text.configure(state=tk.NORMAL)
        self.parameters_text.delete(1.0, tk.END)
        
        if 'detailed_parameters' in info:
            params = info['detailed_parameters']
            parameters_text = "Параметры преобразования:\n\n"
            
            for key, value in params.items():
                if key == 'c':
                    parameters_text += f"Коэффициент c: {round(value, 4)}\n"
                elif key == 'gamma':
                    parameters_text += f"Гамма γ: {round(value, 4)}\n"
                elif key == 'threshold':
                    parameters_text += f"Порог: {round(value, 1)}\n"
                elif key == 'min_brightness':
                    parameters_text += f"Минимальная яркость: {round(value, 1)}\n"
                elif key == 'max_brightness':
                    parameters_text += f"Максимальная яркость: {round(value, 1)}\n"
                elif key == 'outside_mode':
                    parameters_text += f"Режим вне диапазона: {value}\n"
                elif key == 'constant_value' and value is not None:
                    parameters_text += f"Константа: {round(value, 1)}\n"
                elif key == 'mode':
                    parameters_text += f"Режим: {value}\n"
        else:
            parameters_text = "Параметры преобразования не доступны"
        
        self.parameters_text.insert(1.0, parameters_text)
        self.parameters_text.configure(state=tk.DISABLED)
    
    def _update_statistics(self, info: Dict[str, Any]):
        """Обновляет статистику."""
        # Обновляем статистические метки
        self.stats_labels['avg_brightness'].configure(text=f"{info.get('avg_brightness', 'Не рассчитано')}")
        self.stats_labels['contrast'].configure(text=f"{info.get('contrast', 'Не рассчитано')}")
        
        # Обновляем гистограмму
        self.histogram_text.configure(state=tk.NORMAL)
        self.histogram_text.delete(1.0, tk.END)
        
        if 'histogram' in info:
            histogram_text = "Распределение яркостей:\n\n"
            histogram = info['histogram']
            
            # Создаем текстовое представление гистограммы
            max_count = max(histogram) if histogram else 1
            for i, count in enumerate(histogram):
                if i % 32 == 0:  # Показываем каждые 32 значения
                    bar_length = int((count / max_count) * 20) if max_count > 0 else 0
                    bar = "█" * bar_length
                    histogram_text += f"{i:3d}: {bar} ({count})\n"
        else:
            histogram_text = "Гистограмма не рассчитана"
        
        self.histogram_text.insert(1.0, histogram_text)
        self.histogram_text.configure(state=tk.DISABLED)
    
    def clear_info(self):
        """Очищает информационную панель."""
        self._clear_all_info()
