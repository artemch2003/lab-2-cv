"""
Главное окно приложения с группированными настройками по функциональности.
Сгруппирует UI по цветности, сглаживанию и резкости для удобства пользователя.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import sys
import os
from PIL import Image, ImageTk

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .components.color_transform_settings import ColorTransformSettings
from .components.smoothing_settings import SmoothingSettings
from .components.sharpness_settings import SharpnessSettings
from .components.modern_image_display import ModernImageDisplay
from .components.modern_info_panel import ModernInfoPanel
from .styles.modern_styles import ModernStyles

logger = logging.getLogger(__name__)


class GroupedMainWindow:
    """Главное окно с группированными настройками по функциональности."""
    
    def __init__(self, root):
        """Инициализация главного окна."""
        self.root = root
        self.original_image = None
        self.processed_image = None
        self.setup_window()
        self.setup_styles()
        self.create_interface()
        
    def setup_window(self):
        """Настройка главного окна."""
        self.root.title("Photo Editor Pro - Группированная обработка изображений")
        self.root.geometry("1600x1000")
        self.root.configure(bg="#2b2b2b")
        
        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (1000 // 2)
        self.root.geometry(f"1600x1000+{x}+{y}")
        
    def setup_styles(self):
        """Настройка стилей интерфейса."""
        self.styles = ModernStyles()
        
        # Настройка фона главного окна
        self.root.configure(bg=self.styles.get_color('bg_primary'))
        
        # Инициализируем стили ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Настраиваем стили
        self._setup_ttk_styles()
    
    def _setup_ttk_styles(self):
        """Настраивает стили ttk."""
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
        title_label = ttk.Label(header_frame, text="Photo Editor Pro - Группированная обработка", style='Title.TLabel')
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
        
        # Панель настроек с группировкой
        self.create_grouped_settings_panel(workspace_frame)
    
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
    
    def create_grouped_settings_panel(self, parent):
        """Создает панель настроек с группировкой по функциональности."""
        settings_frame = ttk.LabelFrame(parent, text="Настройки обработки", style='Modern.TLabelFrame', padding="15")
        settings_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        settings_frame.columnconfigure(0, weight=1)
        
        # Создаем скроллируемую область для настроек
        canvas = tk.Canvas(settings_frame, bg="#3c3c3c", highlightthickness=0)
        scrollbar = ttk.Scrollbar(settings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Modern.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Компонент цветовых преобразований
        self.color_settings = ColorTransformSettings(scrollable_frame, self.on_color_transform_change)
        self.color_settings.set_apply_command(self.apply_color_transform)
        
        # Компонент фильтров сглаживания
        self.smoothing_settings = SmoothingSettings(scrollable_frame, self.on_smoothing_filter_change)
        self.smoothing_settings.set_apply_command(self.apply_smoothing_filter)
        
        # Компонент фильтров резкости
        self.sharpness_settings = SharpnessSettings(scrollable_frame, self.on_sharpness_filter_change)
        self.sharpness_settings.set_apply_command(self.apply_sharpness_filter)
        
        # Размещаем компоненты в скроллируемой области
        self.color_settings.settings_container.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.smoothing_settings.settings_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.sharpness_settings.settings_container.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Размещаем canvas и scrollbar
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Настройка прокрутки мышью
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
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
    
    def apply_color_transform(self):
        """Применяет цветовое преобразование."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        try:
            parameters = self.color_settings.get_transform_parameters()
            self.apply_transform(parameters)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def apply_smoothing_filter(self):
        """Применяет фильтр сглаживания."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        try:
            parameters = self.smoothing_settings.get_filter_parameters()
            self.apply_transform(parameters)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def apply_sharpness_filter(self):
        """Применяет фильтр резкости."""
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение")
            return
        
        try:
            parameters = self.sharpness_settings.get_filter_parameters()
            self.apply_transform(parameters)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def apply_transform(self, parameters):
        """Применяет преобразование с заданными параметрами."""
        transform_type = parameters['transform_type']
        self.status_var.set(f"Применение {transform_type.lower()}...")
        
        try:
            # Применяем преобразование с помощью фабрики
            from image_processing.factories.transform_factory import TransformFactory
            
            # Создаем преобразование
            transform = TransformFactory.create_transform(transform_type)
            
            # Конвертируем изображение в numpy array
            import numpy as np
            image_array = np.array(self.original_image)
            
            # Применяем преобразование
            processed_array = transform.apply(image_array, **parameters)
            
            # Конвертируем обратно в PIL Image
            if len(processed_array.shape) == 3:
                self.processed_image = Image.fromarray(processed_array)
            else:
                self.processed_image = Image.fromarray(processed_array, mode='L')
            
            self.display_processed_image()
            
            # Обновляем информацию
            self.update_info(f"Применено преобразование: {transform_type}")
            self.status_var.set(f"{transform_type} применено")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось применить преобразование: {e}")
            self.status_var.set("Ошибка применения преобразования")
    
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
    
    def on_color_transform_change(self, transform_type: str):
        """Обрабатывает изменение типа цветового преобразования."""
        pass
    
    def on_smoothing_filter_change(self, filter_type: str):
        """Обрабатывает изменение типа фильтра сглаживания."""
        pass
    
    def on_sharpness_filter_change(self, filter_type: str):
        """Обрабатывает изменение типа фильтра резкости."""
        pass
    
    def update_info(self, message):
        """Обновляет информационную панель."""
        self.info_text.configure(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, f"Информация об изображении:\n{message}")
        self.info_text.configure(state=tk.DISABLED)


def main():
    """Главная функция запуска приложения."""
    try:
        print("🚀 Запуск Photo Editor Pro с группированным интерфейсом...")
        print("✨ Группировка по функциональности:")
        print("   🎨 Цветовые преобразования")
        print("   🌊 Фильтры сглаживания")
        print("   🔍 Фильтры резкости")
        print()
        
        # Создание главного окна
        root = tk.Tk()
        
        # Создание приложения
        app = GroupedMainWindow(root)
        
        print("✅ Photo Editor Pro запущен успешно!")
        print("📝 Инструкции:")
        print("   1. Нажмите '📁 Загрузить' для выбора изображения")
        print("   2. Выберите нужную группу преобразований в правой панели")
        print("   3. Настройте параметры и нажмите кнопку применения")
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
