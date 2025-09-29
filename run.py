"""
Финальная рабочая версия современного интерфейса Photo Editor Pro.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import sys
import os
from PIL import Image, ImageTk

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class ModernPhotoEditor:
    """Современный фоторедактор с полной функциональностью."""
    
    def __init__(self, root):
        """Инициализация редактора."""
        self.root = root
        self.original_image = None
        self.processed_image = None
        self.setup_window()
        self.setup_styles()
        self.create_interface()
        
    def setup_window(self):
        """Настройка главного окна."""
        self.root.title("Photo Editor Pro - Обработка изображений")
        self.root.geometry("1400x900")
        self.root.configure(bg="#2b2b2b")
        
        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (900 // 2)
        self.root.geometry(f"1400x900+{x}+{y}")
        
    def setup_styles(self):
        """Настройка стилей интерфейса."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Цвета в стиле фоторедактора
        bg_color = "#2b2b2b"
        panel_color = "#3c3c3c"
        accent_color = "#0078d4"
        text_color = "#ffffff"
        
        # Настройка стилей
        self.style.configure('Modern.TFrame', background=bg_color)
        self.style.configure('Modern.TLabelFrame', 
                           background=panel_color, 
                           foreground=text_color,
                           borderwidth=1,
                           relief='solid')
        self.style.configure('Modern.TLabelFrame.Label', 
                           background=panel_color, 
                           foreground=text_color,
                           font=('Segoe UI', 10, 'bold'))
        
        # Настройка layout для LabelFrame
        self.style.layout('Modern.TLabelFrame',
                         [('LabelFrame.border', {'sticky': 'nswe'})])
        self.style.layout('Modern.TLabelFrame.Label',
                         [('LabelFrame.padding', {'sticky': 'nswe'})])
        self.style.configure('Modern.TLabel', 
                           background=panel_color, 
                           foreground=text_color,
                           font=('Segoe UI', 9))
        self.style.configure('Modern.TButton', 
                           background=accent_color,
                           foreground=text_color,
                           font=('Segoe UI', 9, 'bold'),
                           borderwidth=0,
                           focuscolor='none')
        self.style.map('Modern.TButton',
                      background=[('active', '#106ebe'),
                                ('pressed', '#005a9e')])
        self.style.configure('Modern.TCombobox',
                           fieldbackground=panel_color,
                           background=panel_color,
                           foreground=text_color,
                           borderwidth=1,
                           arrowcolor=text_color)
        self.style.map('Modern.TCombobox',
                      fieldbackground=[('readonly', panel_color)],
                      background=[('readonly', panel_color)])
        self.style.configure('Modern.TEntry',
                           fieldbackground=panel_color,
                           background=panel_color,
                           foreground=text_color,
                           borderwidth=1,
                           insertcolor=text_color)
        self.style.configure('Modern.TText',
                           background=panel_color,
                           foreground=text_color,
                           borderwidth=1,
                           insertcolor=text_color)
        self.style.configure('Title.TLabel',
                           background=bg_color,
                           foreground=text_color,
                           font=('Segoe UI', 18, 'bold'))
        self.style.configure('Status.TLabel',
                           background=panel_color,
                           foreground=text_color,
                           font=('Segoe UI', 8),
                           relief='flat')
    
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
        self.create_quality_panel(main_container)
        
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
        load_btn = ttk.Button(control_frame, text="📁 Загрузить", style='Modern.TButton', command=self.load_image)
        load_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = ttk.Button(control_frame, text="💾 Сохранить", style='Modern.TButton', command=self.save_image)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = ttk.Button(control_frame, text="🔄 Сброс", style='Modern.TButton', command=self.reset_image)
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
        display_frame = ttk.LabelFrame(parent, text="Изображения", style='Modern.TLabelFrame', padding="10")
        display_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Исходное изображение
        original_frame = ttk.LabelFrame(display_frame, text="Исходное изображение", style='Modern.TLabelFrame', padding="5")
        original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.original_canvas = tk.Canvas(original_frame, bg="#1e1e1e", highlightthickness=0)
        self.original_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.original_canvas.create_text(200, 150, text="Загрузите изображение\nдля начала работы", 
                                        fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
        
        # Обработанное изображение
        processed_frame = ttk.LabelFrame(display_frame, text="Обработанное изображение", style='Modern.TLabelFrame', padding="5")
        processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.processed_canvas = tk.Canvas(processed_frame, bg="#1e1e1e", highlightthickness=0)
        self.processed_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.processed_canvas.create_text(200, 150, text="Примените преобразование\nдля просмотра результата", 
                                         fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
    
    def create_settings_panel(self, parent):
        """Создает панель настроек."""
        settings_frame = ttk.LabelFrame(parent, text="Настройки преобразования", style='Modern.TLabelFrame', padding="15")
        settings_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        
        # Тип преобразования
        ttk.Label(settings_frame, text="Тип преобразования:", style='Modern.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.transform_combo = ttk.Combobox(settings_frame, 
                                          values=["Логарифмическое", "Степенное", "Бинарное", "Вырезание диапазона яркостей",
                                                 "Прямоугольный фильтр 3x3", "Прямоугольный фильтр 5x5", 
                                                 "Медианный фильтр 3x3", "Медианный фильтр 5x5",
                                                 "Фильтр Гаусса σ=1.0", "Фильтр Гаусса σ=2.0", "Фильтр Гаусса σ=3.0",
                                                 "Сигма-фильтр σ=1.0", "Сигма-фильтр σ=2.0", "Сигма-фильтр σ=3.0",
                                                 "Нерезкое маскирование k=3, λ=0.5", "Нерезкое маскирование k=3, λ=1.0", 
                                                 "Нерезкое маскирование k=3, λ=1.5", "Нерезкое маскирование k=3, λ=2.0",
                                                 "Нерезкое маскирование k=5, λ=0.5", "Нерезкое маскирование k=5, λ=1.0", 
                                                 "Нерезкое маскирование k=5, λ=1.5", "Нерезкое маскирование k=5, λ=2.0",
                                                 "Нерезкое маскирование k=7, λ=0.5", "Нерезкое маскирование k=7, λ=1.0", 
                                                 "Нерезкое маскирование k=7, λ=1.5", "Нерезкое маскирование k=7, λ=2.0"], 
                                          state="readonly", width=20, style='Modern.TCombobox')
        self.transform_combo.pack(fill=tk.X, pady=(0, 10))
        self.transform_combo.set("Логарифмическое")
        self.transform_combo.bind("<<ComboboxSelected>>", self.on_transform_change)
        
        # Описание
        self.desc_text = tk.Text(settings_frame, height=4, width=30, wrap=tk.WORD, 
                               bg="#3c3c3c", fg="#ffffff", font=('Segoe UI', 9))
        self.desc_text.pack(fill=tk.X, pady=(0, 10))
        self.desc_text.insert(1.0, "Логарифмическое преобразование улучшает видимость деталей в темных областях изображения.")
        self.desc_text.configure(state=tk.DISABLED)
        
        # Параметры (скрыты по умолчанию)
        self.params_frame = ttk.Frame(settings_frame, style='Modern.TFrame')
        self.params_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Переменные для параметров
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
        
        # Создаем все элементы параметров
        self.create_parameter_elements()
        
        # Кнопка применения
        apply_btn = ttk.Button(settings_frame, text="✨ Применить преобразование", style='Modern.TButton', command=self.apply_transform)
        apply_btn.pack(fill=tk.X, pady=(10, 0))
    
    def create_parameter_elements(self):
        """Создает все элементы параметров преобразований."""
        # Режим (для логарифмического и степенного)
        self.mode_label = ttk.Label(self.params_frame, text="Режим:", style='Modern.TLabel')
        self.mode_combo = ttk.Combobox(self.params_frame, textvariable=self.mode_var,
                                      values=["Автоматически", "Вручную"], 
                                      state="readonly", width=15, style='Modern.TCombobox')
        self.mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)
        
        # Гамма (для степенного)
        self.gamma_label = ttk.Label(self.params_frame, text="Гамма:", style='Modern.TLabel')
        self.gamma_entry = ttk.Entry(self.params_frame, textvariable=self.gamma_var, width=15, style='Modern.TEntry')
        
        # Коэффициент c (для логарифмического)
        self.c_label = ttk.Label(self.params_frame, text="Коэффициент c:", style='Modern.TLabel')
        self.c_entry = ttk.Entry(self.params_frame, textvariable=self.c_var, width=15, style='Modern.TEntry')
        
        # Пороговое значение (для бинарного)
        self.threshold_mode_label = ttk.Label(self.params_frame, text="Режим порога:", style='Modern.TLabel')
        self.threshold_mode_combo = ttk.Combobox(self.params_frame, textvariable=self.threshold_mode_var,
                                                values=["Произвольный", "Заготовленные"], 
                                                state="readonly", width=15, style='Modern.TCombobox')
        self.threshold_mode_combo.bind("<<ComboboxSelected>>", self.on_threshold_mode_change)
        
        self.threshold_label = ttk.Label(self.params_frame, text="Порог:", style='Modern.TLabel')
        self.threshold_entry = ttk.Entry(self.params_frame, textvariable=self.threshold_var, width=15, style='Modern.TEntry')
        
        # Заготовленные пороги
        self.preset_label = ttk.Label(self.params_frame, text="Заготовка:", style='Modern.TLabel')
        self.preset_combo = ttk.Combobox(self.params_frame, textvariable=self.preset_var,
                                        values=["Очень светлый (64)", "Светлый (96)", "Средний (128)", 
                                               "Темный (160)", "Очень темный (192)", "Максимально темный (224)"],
                                        state="readonly", width=15, style='Modern.TCombobox')
        self.preset_combo.bind("<<ComboboxSelected>>", self.on_preset_change)
        
        # Элементы для вырезания диапазона яркостей
        self.min_brightness_label = ttk.Label(self.params_frame, text="Мин. яркость:", style='Modern.TLabel')
        self.min_brightness_entry = ttk.Entry(self.params_frame, textvariable=self.min_brightness_var, width=15, style='Modern.TEntry')
        
        self.max_brightness_label = ttk.Label(self.params_frame, text="Макс. яркость:", style='Modern.TLabel')
        self.max_brightness_entry = ttk.Entry(self.params_frame, textvariable=self.max_brightness_var, width=15, style='Modern.TEntry')
        
        self.outside_mode_label = ttk.Label(self.params_frame, text="Режим вне диапазона:", style='Modern.TLabel')
        self.outside_mode_combo = ttk.Combobox(self.params_frame, textvariable=self.outside_mode_var,
                                             values=["Константа", "Исходное"], 
                                             state="readonly", width=15, style='Modern.TCombobox')
        self.outside_mode_combo.bind("<<ComboboxSelected>>", self.on_outside_mode_change)
        
        self.constant_value_label = ttk.Label(self.params_frame, text="Константа:", style='Modern.TLabel')
        self.constant_value_entry = ttk.Entry(self.params_frame, textvariable=self.constant_value_var, width=15, style='Modern.TEntry')
        
        # Показываем элементы для логарифмического преобразования по умолчанию
        self.update_ui_for_transform("Логарифмическое")
    
    def create_quality_panel(self, parent):
        """Создает панель оценки качества."""
        quality_frame = ttk.LabelFrame(parent, text="Оценка качества обработки", style='Modern.TLabelFrame', padding="15")
        quality_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        # Кнопки управления качеством
        quality_buttons_frame = ttk.Frame(quality_frame, style='Modern.TFrame')
        quality_buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопка анализа качества
        self.analyze_quality_btn = ttk.Button(quality_buttons_frame, text="📊 Анализ качества", 
                                             style='Modern.TButton', command=self.analyze_quality)
        self.analyze_quality_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Кнопка показа карты разности
        self.show_diff_map_btn = ttk.Button(quality_buttons_frame, text="🗺️ Карта разности", 
                                           style='Modern.TButton', command=self.show_difference_map)
        self.show_diff_map_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка сравнения фильтров
        self.compare_filters_btn = ttk.Button(quality_buttons_frame, text="⚖️ Сравнить фильтры", 
                                             style='Modern.TButton', command=self.compare_filters)
        self.compare_filters_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка сравнения фильтров резкости
        self.compare_sharpness_btn = ttk.Button(quality_buttons_frame, text="🔍 Сравнить резкость", 
                                               style='Modern.TButton', command=self.compare_sharpness_filters)
        self.compare_sharpness_btn.pack(side=tk.LEFT, padx=5)
        
        # Область отображения карты разности
        diff_frame = ttk.LabelFrame(quality_frame, text="Карта абсолютной разности", style='Modern.TLabelFrame', padding="5")
        diff_frame.pack(fill=tk.BOTH, expand=True)
        
        self.diff_canvas = tk.Canvas(diff_frame, bg="#1e1e1e", highlightthickness=0, height=200)
        self.diff_canvas.pack(fill=tk.BOTH, expand=True)
        self.diff_canvas.create_text(200, 100, text="Нажмите 'Анализ качества' для просмотра карты разности", 
                                   fill="#666666", font=("Segoe UI", 10), justify=tk.CENTER)
        
        # Переменные для хранения данных
        self.quality_metrics = None
        self.difference_map = None
        self.quality_assessor = None
    
    def create_bottom_panel(self, parent):
        """Создает нижнюю панель."""
        # Информационная панель
        info_frame = ttk.LabelFrame(parent, text="Информация", style='Modern.TLabelFrame', padding="10")
        info_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        self.info_text = tk.Text(info_frame, height=3, wrap=tk.WORD, 
                               bg="#3c3c3c", fg="#ffffff", font=('Segoe UI', 9))
        self.info_text.pack(fill=tk.X)
        self.info_text.insert(1.0, "Информация об изображении:\nИзображение не загружено")
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(parent, textvariable=self.status_var, style='Status.TLabel')
        status_bar.pack(fill=tk.X, pady=(10, 0), padx=20)
    
    def load_image(self):
        """Загружает изображение."""
        file_types = [
            ("Изображения", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
            ("PNG файлы", "*.png"),
            ("JPEG файлы", "*.jpg *.jpeg"),
            ("Все файлы", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=file_types
        )
        
        if file_path:
            try:
                self.original_image = Image.open(file_path)
                self.display_original_image()
                self.update_info(f"Изображение загружено: {os.path.basename(file_path)}")
                self.status_var.set(f"Изображение загружено: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")
                self.status_var.set("Ошибка загрузки изображения")
    
    def display_original_image(self):
        """Отображает исходное изображение."""
        if self.original_image:
            # Изменяем размер для отображения
            display_size = (400, 300)
            display_image = self.original_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Очищаем canvas и отображаем изображение
            self.original_canvas.delete("all")
            self.original_canvas.create_image(200, 150, image=photo)
            self.original_canvas.image = photo  # Сохраняем ссылку
    
    def apply_transform(self):
        """Применяет преобразование."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        transform_type = self.transform_combo.get()
        self.status_var.set(f"Применение {transform_type.lower()} преобразования...")
        
        try:
            # Получаем параметры преобразования
            params = self.get_transform_parameters()
            
            # Применяем преобразование с помощью фабрики
            from image_processing.factories.transform_factory import TransformFactory
            
            # Создаем преобразование
            transform = TransformFactory.create_transform(transform_type)
            
            # Конвертируем изображение в numpy array
            import numpy as np
            image_array = np.array(self.original_image)
            
            # Применяем преобразование
            processed_array = transform.apply(image_array, **params)
            
            # Конвертируем обратно в PIL Image
            from PIL import Image
            if len(processed_array.shape) == 3:
                self.processed_image = Image.fromarray(processed_array)
            else:
                self.processed_image = Image.fromarray(processed_array, mode='L')
            
            self.display_processed_image()
            
            # Обновляем информацию о примененных параметрах
            param_info = self.format_parameters_info(params)
            self.update_info(f"Применено преобразование: {transform_type}\n{param_info}")
            self.status_var.set(f"{transform_type} преобразование применено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось применить преобразование: {e}")
            self.status_var.set("Ошибка применения преобразования")
    
    def get_transform_parameters(self):
        """Возвращает параметры преобразования."""
        transform_type = self.transform_combo.get()
        params = {'transform_type': transform_type}
        
        if transform_type == "Логарифмическое":
            mode = self.mode_var.get()
            params['mode'] = mode
            if mode == "Вручную":
                try:
                    params['c'] = float(self.c_var.get())
                except ValueError:
                    raise ValueError("Неверное значение коэффициента c")
        
        elif transform_type == "Степенное":
            mode = self.mode_var.get()
            params['mode'] = mode
            if mode == "Вручную":
                try:
                    params['gamma'] = float(self.gamma_var.get())
                except ValueError:
                    raise ValueError("Неверное значение гаммы")
        
        elif transform_type == "Бинарное":
            mode = self.threshold_mode_var.get()
            params['threshold_mode'] = mode
            if mode == "Произвольный":
                try:
                    params['threshold'] = int(self.threshold_var.get())
                except ValueError:
                    raise ValueError("Неверное значение порога")
            else:  # Заготовленные
                preset = self.preset_var.get()
                threshold_map = {
                    "Очень светлый (64)": 64,
                    "Светлый (96)": 96,
                    "Средний (128)": 128,
                    "Темный (160)": 160,
                    "Очень темный (192)": 192,
                    "Максимально темный (224)": 224
                }
                params['threshold'] = threshold_map.get(preset, 128)
        
        elif transform_type == "Вырезание диапазона яркостей":
            try:
                params['min_brightness'] = int(self.min_brightness_var.get())
                params['max_brightness'] = int(self.max_brightness_var.get())
                params['outside_mode'] = self.outside_mode_var.get()
                if self.outside_mode_var.get() == "Константа":
                    params['constant_value'] = int(self.constant_value_var.get())
            except ValueError:
                raise ValueError("Неверные значения параметров яркости")
        
        elif transform_type in ["Прямоугольный фильтр 3x3", "Прямоугольный фильтр 5x5", 
                               "Медианный фильтр 3x3", "Медианный фильтр 5x5",
                               "Фильтр Гаусса σ=1.0", "Фильтр Гаусса σ=2.0", "Фильтр Гаусса σ=3.0",
                               "Сигма-фильтр σ=1.0", "Сигма-фильтр σ=2.0", "Сигма-фильтр σ=3.0"]:
            # Фильтры сглаживания не требуют дополнительных параметров
            pass
        elif transform_type.startswith("Нерезкое маскирование"):
            # Фильтры резкости не требуют дополнительных параметров
            pass
        elif transform_type.startswith("Нерезкое маскирование"):
            # Фильтры резкости не требуют дополнительных параметров
            pass
        
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
            mode = params.get('mode', 'Автоматически')
            info_lines.append(f"Режим: {mode}")
            if mode == "Вручную" and 'gamma' in params:
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
            # Фильтры сглаживания не имеют дополнительных параметров
            info_lines.append("Фильтр сглаживания применен")
        elif transform_type.startswith("Нерезкое маскирование"):
            # Фильтры резкости не имеют дополнительных параметров
            info_lines.append("Фильтр резкости применен")
        
        return "\n".join(info_lines) if info_lines else "Параметры не заданы"
    
    def display_processed_image(self):
        """Отображает обработанное изображение."""
        if self.processed_image:
            # Изменяем размер для отображения
            display_size = (400, 300)
            display_image = self.processed_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Очищаем canvas и отображаем изображение
            self.processed_canvas.delete("all")
            self.processed_canvas.create_image(200, 150, image=photo)
            self.processed_canvas.image = photo  # Сохраняем ссылку
    
    def save_image(self):
        """Сохраняет обработанное изображение."""
        if not self.processed_image:
            messagebox.showwarning("Предупреждение", "Нет обработанного изображения для сохранения")
            return
        
        file_types = [
            ("PNG файлы", "*.png"),
            ("JPEG файлы", "*.jpg"),
            ("Все файлы", "*.*")
        ]
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить обработанное изображение",
            defaultextension=".png",
            filetypes=file_types
        )
        
        if file_path:
            try:
                self.processed_image.save(file_path)
                self.status_var.set(f"Изображение сохранено: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить изображение: {e}")
                self.status_var.set("Ошибка сохранения изображения")
    
    def reset_image(self):
        """Сбрасывает изображение к исходному состоянию."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Нет изображения для сброса")
            return
        
        self.processed_image = None
        self.processed_canvas.delete("all")
        self.processed_canvas.create_text(200, 150, text="Примените преобразование\nдля просмотра результата", 
                                        fill="#666666", font=("Segoe UI", 12), justify=tk.CENTER)
        self.update_info("Изображение сброшено к исходному состоянию")
        self.status_var.set("Изображение сброшено к исходному состоянию")
    
    def on_transform_change(self, event=None):
        """Обрабатывает изменение типа преобразования."""
        transform_type = self.transform_combo.get()
        
        descriptions = {
            "Логарифмическое": "Логарифмическое преобразование улучшает видимость деталей в темных областях изображения.",
            "Степенное": "Степенное преобразование позволяет регулировать контрастность изображения с помощью параметра гамма.",
            "Бинарное": "Бинарное преобразование создает черно-белое изображение на основе порогового значения.",
            "Вырезание диапазона яркостей": "Вырезание диапазона яркостей выделяет определенный диапазон яркостей в изображении.",
            "Прямоугольный фильтр 3x3": "Прямоугольный фильтр 3x3 применяет усреднение по окну 3x3 для сглаживания изображения.",
            "Прямоугольный фильтр 5x5": "Прямоугольный фильтр 5x5 применяет усреднение по окну 5x5 для более сильного сглаживания.",
            "Медианный фильтр 3x3": "Медианный фильтр 3x3 удаляет шум, заменяя каждый пиксель медианой в окне 3x3.",
            "Медианный фильтр 5x5": "Медианный фильтр 5x5 удаляет шум, заменяя каждый пиксель медианой в окне 5x5.",
            "Фильтр Гаусса σ=1.0": "Фильтр Гаусса с σ=1.0 применяет мягкое сглаживание с ядром 7x7 по правилу 3σ.",
            "Фильтр Гаусса σ=2.0": "Фильтр Гаусса с σ=2.0 применяет среднее сглаживание с ядром 13x13 по правилу 3σ.",
            "Фильтр Гаусса σ=3.0": "Фильтр Гаусса с σ=3.0 применяет сильное сглаживание с ядром 19x19 по правилу 3σ.",
            "Сигма-фильтр σ=1.0": "Сигма-фильтр с σ=1.0 удаляет пиксели, отклоняющиеся от среднего более чем на 1σ в окне 5x5.",
            "Сигма-фильтр σ=2.0": "Сигма-фильтр с σ=2.0 удаляет пиксели, отклоняющиеся от среднего более чем на 2σ в окне 5x5.",
            "Сигма-фильтр σ=3.0": "Сигма-фильтр с σ=3.0 удаляет пиксели, отклоняющиеся от среднего более чем на 3σ в окне 5x5.",
            # Описания для фильтров резкости
            "Нерезкое маскирование k=3, λ=0.5": "Нерезкое маскирование с ядром 3x3 и коэффициентом λ=0.5 для мягкого повышения резкости.",
            "Нерезкое маскирование k=3, λ=1.0": "Нерезкое маскирование с ядром 3x3 и коэффициентом λ=1.0 для стандартного повышения резкости.",
            "Нерезкое маскирование k=3, λ=1.5": "Нерезкое маскирование с ядром 3x3 и коэффициентом λ=1.5 для сильного повышения резкости.",
            "Нерезкое маскирование k=3, λ=2.0": "Нерезкое маскирование с ядром 3x3 и коэффициентом λ=2.0 для очень сильного повышения резкости.",
            "Нерезкое маскирование k=5, λ=0.5": "Нерезкое маскирование с ядром 5x5 и коэффициентом λ=0.5 для мягкого повышения резкости.",
            "Нерезкое маскирование k=5, λ=1.0": "Нерезкое маскирование с ядром 5x5 и коэффициентом λ=1.0 для стандартного повышения резкости.",
            "Нерезкое маскирование k=5, λ=1.5": "Нерезкое маскирование с ядром 5x5 и коэффициентом λ=1.5 для сильного повышения резкости.",
            "Нерезкое маскирование k=5, λ=2.0": "Нерезкое маскирование с ядром 5x5 и коэффициентом λ=2.0 для очень сильного повышения резкости.",
            "Нерезкое маскирование k=7, λ=0.5": "Нерезкое маскирование с ядром 7x7 и коэффициентом λ=0.5 для мягкого повышения резкости.",
            "Нерезкое маскирование k=7, λ=1.0": "Нерезкое маскирование с ядром 7x7 и коэффициентом λ=1.0 для стандартного повышения резкости.",
            "Нерезкое маскирование k=7, λ=1.5": "Нерезкое маскирование с ядром 7x7 и коэффициентом λ=1.5 для сильного повышения резкости.",
            "Нерезкое маскирование k=7, λ=2.0": "Нерезкое маскирование с ядром 7x7 и коэффициентом λ=2.0 для очень сильного повышения резкости."
        }
        
        self.desc_text.configure(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(1.0, descriptions.get(transform_type, ""))
        self.desc_text.configure(state=tk.DISABLED)
        
        # Обновляем UI для выбранного типа преобразования
        self.update_ui_for_transform(transform_type)
    
    def update_ui_for_transform(self, transform_type):
        """Обновляет UI в зависимости от типа преобразования."""
        # Скрываем все элементы сначала
        self.hide_all_parameter_elements()
        
        if transform_type == "Логарифмическое":
            # Показываем режим и коэффициент c
            self.mode_label.pack(anchor=tk.W, pady=(5, 0))
            self.mode_combo.pack(anchor=tk.W, pady=(0, 5))
            self.on_mode_change()
        elif transform_type == "Степенное":
            # Показываем режим и гамму
            self.mode_label.pack(anchor=tk.W, pady=(5, 0))
            self.mode_combo.pack(anchor=tk.W, pady=(0, 5))
            self.on_mode_change()
        elif transform_type == "Бинарное":
            # Показываем режим порога
            self.threshold_mode_label.pack(anchor=tk.W, pady=(5, 0))
            self.threshold_mode_combo.pack(anchor=tk.W, pady=(0, 5))
            self.on_threshold_mode_change()
        elif transform_type == "Вырезание диапазона яркостей":
            # Показываем элементы вырезания диапазона
            self.min_brightness_label.pack(anchor=tk.W, pady=(5, 0))
            self.min_brightness_entry.pack(anchor=tk.W, pady=(0, 5))
            self.max_brightness_label.pack(anchor=tk.W, pady=(5, 0))
            self.max_brightness_entry.pack(anchor=tk.W, pady=(0, 5))
            self.outside_mode_label.pack(anchor=tk.W, pady=(5, 0))
            self.outside_mode_combo.pack(anchor=tk.W, pady=(0, 5))
            self.on_outside_mode_change()
        elif transform_type in ["Прямоугольный фильтр 3x3", "Прямоугольный фильтр 5x5", 
                               "Медианный фильтр 3x3", "Медианный фильтр 5x5",
                               "Фильтр Гаусса σ=1.0", "Фильтр Гаусса σ=2.0", "Фильтр Гаусса σ=3.0",
                               "Сигма-фильтр σ=1.0", "Сигма-фильтр σ=2.0", "Сигма-фильтр σ=3.0"]:
            # Фильтры сглаживания не требуют дополнительных параметров
            pass
        elif transform_type.startswith("Нерезкое маскирование"):
            # Фильтры резкости не требуют дополнительных параметров
            pass
    
    def hide_all_parameter_elements(self):
        """Скрывает все элементы параметров."""
        elements = [
            self.mode_label, self.mode_combo,
            self.gamma_label, self.gamma_entry,
            self.c_label, self.c_entry,
            self.threshold_mode_label, self.threshold_mode_combo,
            self.threshold_label, self.threshold_entry,
            self.preset_label, self.preset_combo,
            self.min_brightness_label, self.min_brightness_entry,
            self.max_brightness_label, self.max_brightness_entry,
            self.outside_mode_label, self.outside_mode_combo,
            self.constant_value_label, self.constant_value_entry
        ]
        for element in elements:
            element.pack_forget()
    
    def on_mode_change(self, event=None):
        """Обрабатывает изменение режима."""
        mode = self.mode_var.get()
        transform_type = self.transform_combo.get()
        
        if mode == "Вручную":
            if transform_type == "Логарифмическое":
                self.c_label.pack(anchor=tk.W, pady=(5, 0))
                self.c_entry.pack(anchor=tk.W, pady=(0, 5))
            elif transform_type == "Степенное":
                self.gamma_label.pack(anchor=tk.W, pady=(5, 0))
                self.gamma_entry.pack(anchor=tk.W, pady=(0, 5))
        else:
            self.gamma_label.pack_forget()
            self.gamma_entry.pack_forget()
            self.c_label.pack_forget()
            self.c_entry.pack_forget()
    
    def on_threshold_mode_change(self, event=None):
        """Обрабатывает изменение режима порога."""
        mode = self.threshold_mode_var.get()
        
        if mode == "Произвольный":
            self.threshold_label.pack(anchor=tk.W, pady=(5, 0))
            self.threshold_entry.pack(anchor=tk.W, pady=(0, 5))
            self.preset_label.pack_forget()
            self.preset_combo.pack_forget()
        else:  # Заготовленные
            self.preset_label.pack(anchor=tk.W, pady=(5, 0))
            self.preset_combo.pack(anchor=tk.W, pady=(0, 5))
            self.threshold_label.pack_forget()
            self.threshold_entry.pack_forget()
    
    def on_preset_change(self, event=None):
        """Обрабатывает изменение заготовки порога."""
        # Обновляем порог на основе выбранной заготовки
        preset = self.preset_var.get()
        threshold_map = {
            "Очень светлый (64)": 64,
            "Светлый (96)": 96,
            "Средний (128)": 128,
            "Темный (160)": 160,
            "Очень темный (192)": 192,
            "Максимально темный (224)": 224
        }
        self.threshold_var.set(str(threshold_map.get(preset, 128)))
    
    def on_outside_mode_change(self, event=None):
        """Обрабатывает изменение режима вне диапазона."""
        mode = self.outside_mode_var.get()
        
        if mode == "Константа":
            self.constant_value_label.pack(anchor=tk.W, pady=(5, 0))
            self.constant_value_entry.pack(anchor=tk.W, pady=(0, 5))
        else:
            self.constant_value_label.pack_forget()
            self.constant_value_entry.pack_forget()
    
    def update_info(self, message):
        """Обновляет информационную панель."""
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, f"Информация об изображении:\n{message}")
        self.info_text.configure(state=tk.DISABLED)
    
    def analyze_quality(self):
        """Анализирует качество обработки изображения."""
        if not self.original_image or not self.processed_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение и примените преобразование")
            return
        
        try:
            # Инициализируем оценщик качества
            from image_processing.quality_assessment import QualityAssessment
            self.quality_assessor = QualityAssessment()
            
            # Конвертируем изображения в numpy arrays
            import numpy as np
            original_array = np.array(self.original_image)
            processed_array = np.array(self.processed_image)
            
            # Вычисляем метрики качества
            self.quality_metrics = self.quality_assessor.compute_quality_metrics(original_array, processed_array)
            
            # Вычисляем карту разности
            self.difference_map = self.quality_assessor.compute_absolute_difference_map(original_array, processed_array)
            
            # Отображаем карту разности
            self.display_difference_map()
            
            # Обновляем информацию
            quality_report = self.quality_assessor.format_quality_report(self.quality_metrics)
            self.update_info(f"Анализ качества завершен\n{quality_report}")
            
            self.status_var.set("Анализ качества завершен")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось проанализировать качество: {e}")
            self.status_var.set("Ошибка анализа качества")
    
    def display_difference_map(self):
        """Отображает карту разности."""
        if self.difference_map is None:
            return
        
        try:
            # Создаем визуализацию карты разности
            visualization = self.quality_assessor.create_visualization_map(self.difference_map, 'hot')
            
            # Конвертируем в PIL Image
            from PIL import Image
            if len(visualization.shape) == 3:
                diff_image = Image.fromarray(visualization)
            else:
                diff_image = Image.fromarray(visualization, mode='L')
            
            # Изменяем размер для отображения
            display_size = (400, 200)
            display_image = diff_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Очищаем canvas и отображаем карту
            self.diff_canvas.delete("all")
            self.diff_canvas.create_image(200, 100, image=photo)
            self.diff_canvas.image = photo  # Сохраняем ссылку
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отобразить карту разности: {e}")
    
    def show_difference_map(self):
        """Показывает карту разности в отдельном окне."""
        if self.difference_map is None:
            messagebox.showwarning("Предупреждение", "Сначала выполните анализ качества")
            return
        
        try:
            # Создаем новое окно
            diff_window = tk.Toplevel(self.root)
            diff_window.title("Карта абсолютной разности")
            diff_window.geometry("600x400")
            diff_window.configure(bg="#2b2b2b")
            
            # Создаем canvas для отображения
            canvas = tk.Canvas(diff_window, bg="#1e1e1e", highlightthickness=0)
            canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Создаем визуализацию
            visualization = self.quality_assessor.create_visualization_map(self.difference_map, 'hot')
            
            # Конвертируем в PIL Image
            from PIL import Image
            if len(visualization.shape) == 3:
                diff_image = Image.fromarray(visualization)
            else:
                diff_image = Image.fromarray(visualization, mode='L')
            
            # Изменяем размер для отображения
            display_size = (580, 380)
            display_image = diff_image.copy()
            display_image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Отображаем карту
            canvas.create_image(300, 200, image=photo)
            canvas.image = photo  # Сохраняем ссылку
            
            # Добавляем информацию
            info_text = f"Средняя разность: {self.quality_metrics['mean_difference']:.2f}\n"
            info_text += f"Максимальная разность: {self.quality_metrics['max_difference']}\n"
            info_text += f"Оценка качества: {self.quality_metrics['quality_rating']}"
            
            info_label = tk.Label(diff_window, text=info_text, bg="#2b2b2b", fg="#ffffff", 
                                font=("Segoe UI", 10))
            info_label.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось показать карту разности: {e}")
    
    def compare_filters(self):
        """Сравнивает качество различных фильтров."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        try:
            # Создаем окно сравнения
            compare_window = tk.Toplevel(self.root)
            compare_window.title("Сравнение качества фильтров")
            compare_window.geometry("800x600")
            compare_window.configure(bg="#2b2b2b")
            
            # Список доступных фильтров
            available_filters = [
                "Прямоугольный фильтр 3x3", "Прямоугольный фильтр 5x5",
                "Медианный фильтр 3x3", "Медианный фильтр 5x5",
                "Фильтр Гаусса σ=1.0", "Фильтр Гаусса σ=2.0", "Фильтр Гаусса σ=3.0",
                "Сигма-фильтр σ=1.0", "Сигма-фильтр σ=2.0", "Сигма-фильтр σ=3.0"
            ]
            
            # Создаем интерфейс выбора фильтров
            selection_frame = ttk.LabelFrame(compare_window, text="Выберите фильтры для сравнения", 
                                          style='Modern.TLabelFrame', padding="10")
            selection_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Чекбоксы для выбора фильтров
            self.selected_filters = {}
            for i, filter_name in enumerate(available_filters):
                var = tk.BooleanVar()
                cb = ttk.Checkbutton(selection_frame, text=filter_name, variable=var)
                cb.grid(row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
                self.selected_filters[filter_name] = var
            
            # Кнопка запуска сравнения
            compare_btn = ttk.Button(selection_frame, text="🔄 Сравнить выбранные фильтры", 
                                   style='Modern.TButton', command=lambda: self.run_filter_comparison(compare_window))
            compare_btn.grid(row=len(available_filters)//2 + 1, column=0, columnspan=2, pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать окно сравнения: {e}")
    
    def run_filter_comparison(self, window):
        """Запускает сравнение выбранных фильтров."""
        try:
            # Получаем выбранные фильтры
            selected = [name for name, var in self.selected_filters.items() if var.get()]
            
            if not selected:
                messagebox.showwarning("Предупреждение", "Выберите хотя бы один фильтр")
                return
            
            # Инициализируем оценщик качества
            from image_processing.quality_assessment import FilterQualityComparator
            comparator = FilterQualityComparator()
            
            # Применяем выбранные фильтры
            import numpy as np
            from image_processing.factories.transform_factory import TransformFactory
            
            original_array = np.array(self.original_image)
            filter_results = {}
            
            for filter_name in selected:
                try:
                    transform = TransformFactory.create_transform(filter_name)
                    processed_array = transform.apply(original_array)
                    filter_results[filter_name] = processed_array
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось применить фильтр {filter_name}: {e}")
                    return
            
            # Сравниваем фильтры
            comparison_results = comparator.compare_filters(original_array, filter_results)
            
            # Отображаем результаты
            self.display_comparison_results(window, comparison_results, comparator)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить сравнение: {e}")
    
    def display_comparison_results(self, window, results, comparator):
        """Отображает результаты сравнения фильтров."""
        try:
            # Очищаем окно
            for widget in window.winfo_children():
                if isinstance(widget, ttk.LabelFrame):
                    widget.destroy()
            
            # Создаем область для результатов
            results_frame = ttk.LabelFrame(window, text="Результаты сравнения", 
                                         style='Modern.TLabelFrame', padding="10")
            results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Отчет о сравнении
            report_text = comparator.format_comparison_report()
            
            # Создаем текстовое поле для отчета
            text_widget = tk.Text(results_frame, wrap=tk.WORD, bg="#3c3c3c", fg="#ffffff", 
                                 font=("Segoe UI", 9))
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(1.0, report_text)
            text_widget.configure(state=tk.DISABLED)
            
            # Кнопка закрытия
            close_btn = ttk.Button(results_frame, text="Закрыть", style='Modern.TButton', 
                                  command=window.destroy)
            close_btn.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отобразить результаты: {e}")
    
    def compare_sharpness_filters(self):
        """Сравнивает различные фильтры резкости."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        try:
            # Создаем окно сравнения фильтров резкости
            sharpness_window = tk.Toplevel(self.root)
            sharpness_window.title("Сравнение фильтров резкости")
            sharpness_window.geometry("900x700")
            sharpness_window.configure(bg="#2b2b2b")
            
            # Создаем интерфейс выбора параметров
            selection_frame = ttk.LabelFrame(sharpness_window, text="Параметры сравнения", 
                                          style='Modern.TLabelFrame', padding="10")
            selection_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Выбор размеров ядер
            ttk.Label(selection_frame, text="Размеры ядер (k):", style='Modern.TLabel').pack(anchor=tk.W)
            kernel_frame = ttk.Frame(selection_frame, style='Modern.TFrame')
            kernel_frame.pack(fill=tk.X, pady=(5, 10))
            
            self.kernel_vars = {}
            for k in [3, 5, 7]:
                var = tk.BooleanVar(value=True)  # По умолчанию все выбраны
                cb = ttk.Checkbutton(kernel_frame, text=f"k={k}", variable=var)
                cb.pack(side=tk.LEFT, padx=5)
                self.kernel_vars[k] = var
            
            # Выбор значений λ
            ttk.Label(selection_frame, text="Значения λ:", style='Modern.TLabel').pack(anchor=tk.W)
            lambda_frame = ttk.Frame(selection_frame, style='Modern.TFrame')
            lambda_frame.pack(fill=tk.X, pady=(5, 10))
            
            self.lambda_vars = {}
            for lambda_val in [0.5, 1.0, 1.5, 2.0]:
                var = tk.BooleanVar(value=True)  # По умолчанию все выбраны
                cb = ttk.Checkbutton(lambda_frame, text=f"λ={lambda_val}", variable=var)
                cb.pack(side=tk.LEFT, padx=5)
                self.lambda_vars[lambda_val] = var
            
            # Кнопка запуска сравнения
            compare_btn = ttk.Button(selection_frame, text="🔍 Сравнить фильтры резкости", 
                                   style='Modern.TButton', 
                                   command=lambda: self.run_sharpness_comparison(sharpness_window))
            compare_btn.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать окно сравнения: {e}")
    
    def run_sharpness_comparison(self, window):
        """Запускает сравнение фильтров резкости."""
        try:
            # Получаем выбранные параметры
            selected_kernels = [k for k, var in self.kernel_vars.items() if var.get()]
            selected_lambdas = [lambda_val for lambda_val, var in self.lambda_vars.items() if var.get()]
            
            if not selected_kernels or not selected_lambdas:
                messagebox.showwarning("Предупреждение", "Выберите хотя бы один размер ядра и одно значение λ")
                return
            
            # Инициализируем компаратор
            from image_processing.sharpness_comparator import SharpnessComparator
            comparator = SharpnessComparator()
            
            # Конвертируем изображение в numpy array
            import numpy as np
            original_array = np.array(self.original_image)
            
            # Выполняем сравнение
            results = comparator.compare_sharpness_filters(
                original_array, 
                kernel_sizes=selected_kernels, 
                lambda_values=selected_lambdas
            )
            
            # Отображаем результаты
            self.display_sharpness_comparison_results(window, results, comparator)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить сравнение: {e}")
    
    def display_sharpness_comparison_results(self, window, results, comparator):
        """Отображает результаты сравнения фильтров резкости."""
        try:
            # Очищаем окно
            for widget in window.winfo_children():
                if isinstance(widget, ttk.LabelFrame):
                    widget.destroy()
            
            # Создаем область для результатов
            results_frame = ttk.LabelFrame(window, text="Результаты сравнения фильтров резкости", 
                                         style='Modern.TLabelFrame', padding="10")
            results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Отчет о сравнении
            report_text = comparator.format_comparison_report()
            
            # Добавляем рекомендации
            recommendations = comparator.get_filter_recommendations()
            report_text += "\n\n" + "\n".join(recommendations)
            
            # Создаем текстовое поле для отчета
            text_widget = tk.Text(results_frame, wrap=tk.WORD, bg="#3c3c3c", fg="#ffffff", 
                                 font=("Segoe UI", 9))
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(1.0, report_text)
            text_widget.configure(state=tk.DISABLED)
            
            # Кнопка закрытия
            close_btn = ttk.Button(results_frame, text="Закрыть", style='Modern.TButton', 
                                  command=window.destroy)
            close_btn.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отобразить результаты: {e}")

def main():
    """Главная функция запуска приложения."""
    try:
        print("🚀 Запуск Photo Editor Pro...")
        print("✨ Современный интерфейс в стиле фоторедактора")
        print("🎨 Темная тема с акцентными цветами")
        print("🔄 Удобное сравнение до/после")
        print()
        
        # Создание главного окна
        root = tk.Tk()
        
        # Создание приложения
        app = ModernPhotoEditor(root)
        
        print("✅ Photo Editor Pro запущен успешно!")
        print("📝 Инструкции:")
        print("   1. Нажмите '📁 Загрузить' для выбора изображения")
        print("   2. Выберите тип преобразования в правой панели")
        print("   3. Нажмите '✨ Применить преобразование'")
        print("   4. Сохраните результат с помощью '💾 Сохранить'")
        print("   5. Используйте '🔄 Сброс' для возврата к исходному")
        print()
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
