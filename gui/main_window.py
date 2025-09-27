"""
Главное окно приложения.
Содержит основной интерфейс для работы с изображениями.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import logging
import os

from image_processing.image_processor import ImageProcessor

logger = logging.getLogger(__name__)


class MainWindow:
    """Главное окно приложения."""
    
    def __init__(self, root):
        """
        Инициализация главного окна.
        
        Args:
            root: Корневое окно tkinter
        """
        self.root = root
        self.image_processor = ImageProcessor()
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """Настройка параметров окна."""
        self.root.title("Обработка изображений - Преобразования")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
    def create_widgets(self):
        """Создание виджетов интерфейса."""
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Настройка растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Обработка изображений", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Кнопки управления
        ttk.Button(control_frame, text="Загрузить изображение", 
                  command=self.load_image).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(control_frame, text="Применить преобразование", 
                  command=self.apply_transform).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(control_frame, text="Сохранить результат", 
                  command=self.save_image).grid(row=0, column=2, padx=(0, 10))
        
        # Настройки преобразования
        settings_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="10")
        settings_frame.grid(row=1, column=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Тип преобразования
        ttk.Label(settings_frame, text="Тип преобразования:").grid(row=0, column=0, sticky=tk.W)
        self.transform_type_var = tk.StringVar(value="Логарифмическое")
        transform_combo = ttk.Combobox(settings_frame, textvariable=self.transform_type_var, 
                                      values=["Логарифмическое", "Степенное", "Бинарное"], 
                                      state="readonly", width=15)
        transform_combo.grid(row=0, column=1, padx=(5, 0))
        transform_combo.bind("<<ComboboxSelected>>", self.on_transform_type_change)
        
        # Гамма (для степенного преобразования) - скрыта по умолчанию
        self.gamma_label = ttk.Label(settings_frame, text="Гамма γ:")
        self.gamma_var = tk.StringVar(value="1.0")
        self.gamma_entry = ttk.Entry(settings_frame, textvariable=self.gamma_var, width=15)
        
        # Режим настройки коэффициента
        self.mode_label = ttk.Label(settings_frame, text="Режим:")
        self.mode_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.mode_var = tk.StringVar(value="Автоматически")
        self.mode_combo = ttk.Combobox(settings_frame, textvariable=self.mode_var, 
                                      values=["Автоматически", "Вручную"], 
                                      state="readonly", width=12)
        self.mode_combo.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
        self.mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)
        
        # Коэффициент c (скрыт по умолчанию)
        self.c_label = ttk.Label(settings_frame, text="Коэффициент c:")
        self.c_var = tk.StringVar(value="1.0")
        self.c_entry = ttk.Entry(settings_frame, textvariable=self.c_var, width=15)
        
        # Пороговое значение (для бинарного преобразования) - скрыто по умолчанию
        self.threshold_label = ttk.Label(settings_frame, text="Порог:")
        self.threshold_var = tk.StringVar(value="128")
        self.threshold_entry = ttk.Entry(settings_frame, textvariable=self.threshold_var, width=15)
        
        # Кнопка применения
        self.apply_button = ttk.Button(settings_frame, text="Применить", 
                                      command=self.apply_transform)
        self.apply_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Область отображения изображений
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S))
        display_frame.columnconfigure(0, weight=1)
        display_frame.columnconfigure(1, weight=1)
        
        # Исходное изображение
        original_frame = ttk.LabelFrame(display_frame, text="Исходное изображение", padding="5")
        original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        original_frame.rowconfigure(0, weight=1)
        
        self.original_label = ttk.Label(original_frame, text="Изображение не загружено", 
                                       anchor="center", background="lightgray")
        self.original_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Обработанное изображение
        processed_frame = ttk.LabelFrame(display_frame, text="Обработанное изображение", padding="5")
        processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        processed_frame.rowconfigure(0, weight=1)
        
        self.processed_label = ttk.Label(processed_frame, text="Результат обработки", 
                                       anchor="center", background="lightgray")
        self.processed_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Информация", padding="10")
        info_frame.grid(row=3, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.info_text = tk.Text(info_frame, height=4, width=80, wrap=tk.WORD)
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def load_image(self):
        """Загружает изображение из файла."""
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
            self.status_var.set("Загрузка изображения...")
            self.root.update()
            
            if self.image_processor.load_image(file_path):
                self.display_original_image()
                self.update_info()
                self.status_var.set(f"Изображение загружено: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("Ошибка", "Не удалось загрузить изображение")
                self.status_var.set("Ошибка загрузки изображения")
    
    def display_original_image(self):
        """Отображает исходное изображение."""
        if self.image_processor.original_image:
            display_image = self.image_processor.get_image_for_display(
                self.image_processor.original_image
            )
            if display_image:
                self.original_label.configure(image=display_image, text="")
                self.original_label.image = display_image  # Сохраняем ссылку
    
    def on_transform_type_change(self, event=None):
        """Обрабатывает изменение типа преобразования."""
        transform_type = self.transform_type_var.get()
        
        if transform_type == "Степенное":
            # Для степенного преобразования показываем режим и влияет на отображение гаммы
            self.mode_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
            self.mode_combo.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
            self.threshold_label.grid_remove()
            self.threshold_entry.grid_remove()
            self.on_mode_change()
        elif transform_type == "Бинарное":
            # Для бинарного преобразования скрываем гамму, режим и коэффициент c
            self.gamma_label.grid_remove()
            self.gamma_entry.grid_remove()
            self.c_label.grid_remove()
            self.c_entry.grid_remove()
            # Скрываем элементы режима
            self.mode_label.grid_remove()
            self.mode_combo.grid_remove()
            # Показываем пороговое значение
            self.threshold_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
            self.threshold_entry.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
        else:
            # Для логарифмического преобразования скрываем гамму и порог
            self.gamma_label.grid_remove()
            self.gamma_entry.grid_remove()
            self.threshold_label.grid_remove()
            self.threshold_entry.grid_remove()
            # Показываем режим для коэффициента c
            self.mode_label.grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
            self.mode_combo.grid(row=2, column=1, padx=(5, 0), pady=(5, 0))
            self.on_mode_change()
    
    def on_mode_change(self, event=None):
        """Обрабатывает изменение режима настройки."""
        transform_type = self.transform_type_var.get()
        mode = self.mode_var.get()
        
        if transform_type == "Степенное":
            # Для степенного преобразования
            if mode == "Вручную":
                # Показываем поле для гаммы под режимом
                self.gamma_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
                self.gamma_entry.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
                self.gamma_var.set("1.0")
                # Скрываем поле для коэффициента c
                self.c_label.grid_remove()
                self.c_entry.grid_remove()
            else:  # Автоматически
                # Скрываем поле для гаммы
                self.gamma_label.grid_remove()
                self.gamma_entry.grid_remove()
                # Скрываем поле для коэффициента c
                self.c_label.grid_remove()
                self.c_entry.grid_remove()
        else:
            # Для логарифмического преобразования
            if mode == "Вручную":
                # Показываем поле для коэффициента c
                self.c_label.grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
                self.c_entry.grid(row=3, column=1, padx=(5, 0), pady=(5, 0))
                self.c_var.set("1.0")
            else:
                # Скрываем поле для коэффициента c
                self.c_label.grid_remove()
                self.c_entry.grid_remove()
    
    def apply_logarithmic_transform(self):
        """Применяет логарифмическое преобразование с автоматическим коэффициентом."""
        if self.image_processor.original_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        self.status_var.set("Применение логарифмического преобразования...")
        self.root.update()
        
        if self.image_processor.apply_logarithmic_transform():
            self.display_processed_image()
            self.update_info()
            # Получаем информацию о коэффициенте
            info = self.image_processor.get_image_info()
            c_value = info.get('last_coefficient_c', 'неизвестно')
            self.status_var.set(f"Логарифмическое преобразование применено (c={c_value})")
        else:
            messagebox.showerror("Ошибка", "Не удалось применить преобразование")
            self.status_var.set("Ошибка применения преобразования")
    
    def apply_transform(self):
        """Применяет преобразование в зависимости от выбранного типа и режима."""
        if self.image_processor.original_image is None:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        transform_type = self.transform_type_var.get()
        mode = self.mode_var.get()
        
        if transform_type == "Логарифмическое":
            self._apply_logarithmic_transform(mode)
        elif transform_type == "Степенное":
            self._apply_power_transform(mode)
        else:  # Бинарное
            self._apply_binary_transform()
    
    def _apply_logarithmic_transform(self, mode: str):
        """Применяет логарифмическое преобразование."""
        if mode == "Автоматически":
            # Используем автоматический режим
            self.status_var.set("Применение логарифмического преобразования (автоматический режим)...")
            self.root.update()
            
            if self.image_processor.apply_logarithmic_transform():
                self.display_processed_image()
                self.update_info()
                # Получаем информацию о коэффициенте
                info = self.image_processor.get_image_info()
                c_value = info.get('last_coefficient_c', 'неизвестно')
                self.status_var.set(f"Логарифмическое преобразование применено (автоматический режим, c={c_value})")
            else:
                messagebox.showerror("Ошибка", "Не удалось применить преобразование")
                self.status_var.set("Ошибка применения преобразования")
        else:
            # Используем ручной режим
            try:
                c_value = self.c_var.get().strip()
                if not c_value:
                    raise ValueError("Введите значение коэффициента")
                
                c = float(c_value)
                if c <= 0:
                    raise ValueError("Коэффициент должен быть положительным")
                
                self.status_var.set(f"Применение логарифмического преобразования (c={c})...")
                self.root.update()
                
                if self.image_processor.apply_logarithmic_transform(c):
                    self.display_processed_image()
                    self.update_info()
                    self.status_var.set(f"Логарифмическое преобразование применено (c={c})")
                else:
                    messagebox.showerror("Ошибка", "Не удалось применить преобразование")
                    self.status_var.set("Ошибка применения преобразования")
                    
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Неверное значение коэффициента: {e}")
                return
    
    def _apply_power_transform(self, mode: str):
        """Применяет степенное преобразование."""
        try:
            if mode == "Автоматически":
                # Автоматический режим - используем гамму по умолчанию (1.0)
                gamma = 1.0
                self.status_var.set("Применение степенного преобразования (автоматический режим)...")
                self.root.update()
                
                if self.image_processor.apply_power_transform(gamma):
                    self.display_processed_image()
                    self.update_info()
                    # Получаем информацию о коэффициенте
                    info = self.image_processor.get_image_info()
                    c_value = info.get('last_coefficient_c', 'неизвестно')
                    self.status_var.set(f"Степенное преобразование применено (автоматический режим, γ={gamma}, c={c_value})")
                else:
                    messagebox.showerror("Ошибка", "Не удалось применить преобразование")
                    self.status_var.set("Ошибка применения преобразования")
            else:
                # Ручной режим - получаем гамму от пользователя
                gamma_value = self.gamma_var.get().strip()
                if not gamma_value:
                    raise ValueError("Введите значение гаммы")
                
                gamma = float(gamma_value)
                if gamma <= 0:
                    raise ValueError("Гамма должна быть положительной")
                
                self.status_var.set(f"Применение степенного преобразования (γ={gamma}, автоматический режим)...")
                self.root.update()
                
                if self.image_processor.apply_power_transform(gamma):
                    self.display_processed_image()
                    self.update_info()
                    # Получаем информацию о коэффициенте
                    info = self.image_processor.get_image_info()
                    c_value = info.get('last_coefficient_c', 'неизвестно')
                    self.status_var.set(f"Степенное преобразование применено (γ={gamma}, c={c_value})")
                else:
                    messagebox.showerror("Ошибка", "Не удалось применить преобразование")
                    self.status_var.set("Ошибка применения преобразования")
                    
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверное значение параметра: {e}")
            return
    
    def _apply_binary_transform(self):
        """Применяет бинарное преобразование."""
        try:
            threshold_value = self.threshold_var.get().strip()
            if not threshold_value:
                raise ValueError("Введите значение порога")
            
            threshold = float(threshold_value)
            if threshold < 0 or threshold > 255:
                raise ValueError("Порог должен быть в диапазоне от 0 до 255")
            
            self.status_var.set(f"Применение бинарного преобразования (порог={threshold})...")
            self.root.update()
            
            if self.image_processor.apply_binary_transform(threshold):
                self.display_processed_image()
                self.update_info()
                self.status_var.set(f"Бинарное преобразование применено (порог={threshold})")
            else:
                messagebox.showerror("Ошибка", "Не удалось применить преобразование")
                self.status_var.set("Ошибка применения преобразования")
                
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверное значение порога: {e}")
            return
    
    def display_processed_image(self):
        """Отображает обработанное изображение."""
        if self.image_processor.processed_image:
            display_image = self.image_processor.get_image_for_display(
                self.image_processor.processed_image
            )
            if display_image:
                self.processed_label.configure(image=display_image, text="")
                self.processed_label.image = display_image  # Сохраняем ссылку
    
    def save_image(self):
        """Сохраняет обработанное изображение."""
        if self.image_processor.processed_image is None:
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
            self.status_var.set("Сохранение изображения...")
            self.root.update()
            
            if self.image_processor.save_image(file_path):
                self.status_var.set(f"Изображение сохранено: {os.path.basename(file_path)}")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить изображение")
                self.status_var.set("Ошибка сохранения изображения")
    
    def update_info(self):
        """Обновляет информационную панель."""
        info = self.image_processor.get_image_info()
        
        info_text = "Информация об изображении:\n"
        if info:
            info_text += f"Размер: {info.get('size', 'Неизвестно')}\n"
            info_text += f"Режим: {info.get('mode', 'Неизвестно')}\n"
            info_text += f"Формат: {info.get('format', 'Неизвестно')}\n"
            info_text += f"Обработано: {'Да' if info.get('has_processed', False) else 'Нет'}\n"
            
            # Добавляем информацию о коэффициенте, если он был использован
            if 'last_coefficient_c' in info:
                info_text += f"Коэффициент c: {info.get('last_coefficient_c')}\n"
            
            # Добавляем информацию о гамме, если она была использована
            if 'last_gamma' in info:
                info_text += f"Гамма γ: {info.get('last_gamma')}\n"
            
            # Добавляем информацию о пороговом значении, если оно было использовано
            if 'last_threshold' in info:
                info_text += f"Порог: {info.get('last_threshold')}\n"
        else:
            info_text += "Изображение не загружено"
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_text)
