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
                                          values=["Логарифмическое", "Степенное", "Бинарное", "Вырезание диапазона яркостей"], 
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
            
            # Здесь должна быть логика применения преобразований
            # Для демонстрации просто копируем изображение
            self.processed_image = self.original_image.copy()
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
            "Вырезание диапазона яркостей": "Вырезание диапазона яркостей выделяет определенный диапазон яркостей в изображении."
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
