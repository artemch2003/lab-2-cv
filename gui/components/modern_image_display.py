"""
Современный компонент для отображения изображений с удобным сравнением до/после.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, Callable
import os
import logging
from PIL import Image, ImageTk

logger = logging.getLogger(__name__)


class ModernImageDisplay:
    """Современный компонент для отображения изображений с сравнением до/после."""
    
    def __init__(self, parent_frame: ttk.Frame, on_image_loaded: Callable[[str], None]):
        """
        Инициализация компонента отображения.
        
        Args:
            parent_frame: Родительский фрейм
            on_image_loaded: Callback для загрузки изображения
        """
        self.parent_frame = parent_frame
        self.on_image_loaded = on_image_loaded
        
        # Переменные для изображений
        self.original_image = None
        self.processed_image = None
        self.display_mode = "split"  # "split", "before", "after", "overlay"
        
        self._create_widgets()
        self._setup_bindings()
    
    def _create_widgets(self):
        """Создает виджеты отображения."""
        # Главный контейнер для отображения
        display_container = ttk.Frame(self.parent_frame, style='Modern.TFrame')
        display_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        display_container.columnconfigure(0, weight=1)
        display_container.rowconfigure(1, weight=1)
        
        # Панель управления отображением
        self.create_display_controls(display_container)
        
        # Область отображения изображений
        self.create_image_area(display_container)
        
        # Панель информации об изображении
        self.create_image_info_panel(display_container)
    
    def create_display_controls(self, parent):
        """Создает панель управления отображением."""
        controls_frame = ttk.LabelFrame(parent, 
                                       text="Режим отображения", 
                                       style='Modern.TLabelFrame',
                                       padding="10")
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        controls_frame.columnconfigure(0, weight=1)
        
        # Кнопки режимов отображения
        mode_frame = ttk.Frame(controls_frame, style='Modern.TFrame')
        mode_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.mode_var = tk.StringVar(value="split")
        
        ttk.Radiobutton(mode_frame, 
                       text="Разделение", 
                       variable=self.mode_var, 
                       value="split",
                       style='Modern.TRadiobutton',
                       command=self.on_mode_change).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Radiobutton(mode_frame, 
                       text="Только исходное", 
                       variable=self.mode_var, 
                       value="before",
                       style='Modern.TRadiobutton',
                       command=self.on_mode_change).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Radiobutton(mode_frame, 
                       text="Только результат", 
                       variable=self.mode_var, 
                       value="after",
                       style='Modern.TRadiobutton',
                       command=self.on_mode_change).grid(row=0, column=2, padx=(0, 10))
        
        ttk.Radiobutton(mode_frame, 
                       text="Наложение", 
                       variable=self.mode_var, 
                       value="overlay",
                       style='Modern.TRadiobutton',
                       command=self.on_mode_change).grid(row=0, column=3, padx=(0, 10))
        
        # Кнопка переключения полноэкранного режима
        self.fullscreen_btn = ttk.Button(mode_frame, 
                                        text="⛶ Полный экран", 
                                        style='Modern.TButton',
                                        command=self.toggle_fullscreen)
        self.fullscreen_btn.grid(row=0, column=4, padx=(20, 0))
    
    def create_image_area(self, parent):
        """Создает область отображения изображений."""
        # Контейнер для изображений
        self.image_container = ttk.Frame(parent, style='Modern.TFrame')
        self.image_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.image_container.columnconfigure(0, weight=1)
        self.image_container.columnconfigure(1, weight=1)
        self.image_container.rowconfigure(0, weight=1)
        
        # Исходное изображение
        self.original_frame = ttk.LabelFrame(self.image_container, 
                                            text="Исходное изображение", 
                                            style='Modern.TLabelFrame',
                                            padding="5")
        self.original_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        self.original_frame.rowconfigure(0, weight=1)
        
        # Canvas для исходного изображения
        self.original_canvas = tk.Canvas(self.original_frame, 
                                        bg="#1e1e1e", 
                                        highlightthickness=0)
        self.original_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Скроллбары для исходного изображения
        self.original_v_scroll = ttk.Scrollbar(self.original_frame, 
                                              orient=tk.VERTICAL, 
                                              command=self.original_canvas.yview)
        self.original_v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.original_canvas.configure(yscrollcommand=self.original_v_scroll.set)
        
        self.original_h_scroll = ttk.Scrollbar(self.original_frame, 
                                              orient=tk.HORIZONTAL, 
                                              command=self.original_canvas.xview)
        self.original_h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.original_canvas.configure(xscrollcommand=self.original_h_scroll.set)
        
        # Обработанное изображение
        self.processed_frame = ttk.LabelFrame(self.image_container, 
                                             text="Обработанное изображение", 
                                             style='Modern.TLabelFrame',
                                             padding="5")
        self.processed_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        self.processed_frame.rowconfigure(0, weight=1)
        
        # Canvas для обработанного изображения
        self.processed_canvas = tk.Canvas(self.processed_frame, 
                                         bg="#1e1e1e", 
                                         highlightthickness=0)
        self.processed_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Скроллбары для обработанного изображения
        self.processed_v_scroll = ttk.Scrollbar(self.processed_frame, 
                                               orient=tk.VERTICAL, 
                                               command=self.processed_canvas.yview)
        self.processed_v_scroll.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.processed_canvas.configure(yscrollcommand=self.processed_v_scroll.set)
        
        self.processed_h_scroll = ttk.Scrollbar(self.processed_frame, 
                                               orient=tk.HORIZONTAL, 
                                               command=self.processed_canvas.xview)
        self.processed_h_scroll.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.processed_canvas.configure(xscrollcommand=self.processed_h_scroll.set)
        
        # Начальные сообщения
        self.show_placeholder_messages()
    
    def create_image_info_panel(self, parent):
        """Создает панель информации об изображении."""
        info_frame = ttk.LabelFrame(parent, 
                                   text="Информация об изображении", 
                                   style='Modern.TLabelFrame',
                                   padding="10")
        info_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        info_frame.columnconfigure(0, weight=1)
        
        # Информационные метки
        self.info_labels = {}
        
        info_grid = ttk.Frame(info_frame, style='Modern.TFrame')
        info_grid.grid(row=0, column=0, sticky=(tk.W, tk.E))
        info_grid.columnconfigure(1, weight=1)
        
        # Размер изображения
        ttk.Label(info_grid, text="Размер:", style='Modern.TLabel').grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.info_labels['size'] = ttk.Label(info_grid, text="Не загружено", style='Modern.TLabel')
        self.info_labels['size'].grid(row=0, column=1, sticky=tk.W)
        
        # Формат
        ttk.Label(info_grid, text="Формат:", style='Modern.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.info_labels['format'] = ttk.Label(info_grid, text="Не загружено", style='Modern.TLabel')
        self.info_labels['format'].grid(row=1, column=1, sticky=tk.W)
        
        # Режим
        ttk.Label(info_grid, text="Режим:", style='Modern.TLabel').grid(row=2, column=0, sticky=tk.W, padx=(0, 10))
        self.info_labels['mode'] = ttk.Label(info_grid, text="Не загружено", style='Modern.TLabel')
        self.info_labels['mode'].grid(row=2, column=1, sticky=tk.W)
    
    def _setup_bindings(self):
        """Настраивает привязки событий."""
        # Привязка событий мыши для масштабирования
        self.original_canvas.bind("<MouseWheel>", self.on_mousewheel_original)
        self.processed_canvas.bind("<MouseWheel>", self.on_mousewheel_processed)
        
        # Привязка событий для перетаскивания
        self.original_canvas.bind("<Button-1>", self.start_drag_original)
        self.original_canvas.bind("<B1-Motion>", self.drag_original)
        
        self.processed_canvas.bind("<Button-1>", self.start_drag_processed)
        self.processed_canvas.bind("<B1-Motion>", self.drag_processed)
    
    def show_placeholder_messages(self):
        """Показывает сообщения-заглушки."""
        # Сообщение для исходного изображения
        self.original_canvas.create_text(
            self.original_canvas.winfo_width() // 2,
            self.original_canvas.winfo_height() // 2,
            text="Загрузите изображение\nдля начала работы",
            fill="#666666",
            font=("Segoe UI", 12),
            justify=tk.CENTER
        )
        
        # Сообщение для обработанного изображения
        self.processed_canvas.create_text(
            self.processed_canvas.winfo_width() // 2,
            self.processed_canvas.winfo_height() // 2,
            text="Примените преобразование\nдля просмотра результата",
            fill="#666666",
            font=("Segoe UI", 12),
            justify=tk.CENTER
        )
    
    def on_mode_change(self):
        """Обрабатывает изменение режима отображения."""
        mode = self.mode_var.get()
        self.display_mode = mode
        
        if mode == "split":
            self.show_split_view()
        elif mode == "before":
            self.show_before_only()
        elif mode == "after":
            self.show_after_only()
        elif mode == "overlay":
            self.show_overlay_view()
    
    def show_split_view(self):
        """Показывает разделенный вид."""
        self.original_frame.grid()
        self.processed_frame.grid()
        self.image_container.columnconfigure(0, weight=1)
        self.image_container.columnconfigure(1, weight=1)
    
    def show_before_only(self):
        """Показывает только исходное изображение."""
        self.original_frame.grid()
        self.processed_frame.grid_remove()
        self.image_container.columnconfigure(0, weight=1)
        self.image_container.columnconfigure(1, weight=0)
    
    def show_after_only(self):
        """Показывает только обработанное изображение."""
        self.original_frame.grid_remove()
        self.processed_frame.grid()
        self.image_container.columnconfigure(0, weight=0)
        self.image_container.columnconfigure(1, weight=1)
    
    def show_overlay_view(self):
        """Показывает наложенный вид."""
        # Показываем оба фрейма, но обработанное поверх исходного
        self.original_frame.grid()
        self.processed_frame.grid()
        self.image_container.columnconfigure(0, weight=1)
        self.image_container.columnconfigure(1, weight=1)
        # TODO: Реализовать наложение изображений
    
    def display_original_image(self, image):
        """
        Отображает исходное изображение.
        
        Args:
            image: Изображение для отображения
        """
        if image:
            self.original_image = image
            self.display_image_on_canvas(self.original_canvas, image)
            self.update_image_info()
        else:
            self.clear_canvas(self.original_canvas)
            self.show_placeholder_messages()
    
    def display_processed_image(self, image):
        """
        Отображает обработанное изображение.
        
        Args:
            image: Изображение для отображения
        """
        if image:
            self.processed_image = image
            self.display_image_on_canvas(self.processed_canvas, image)
        else:
            self.clear_canvas(self.processed_canvas)
            self.show_placeholder_messages()
    
    def display_image_on_canvas(self, canvas, image):
        """Отображает изображение на canvas."""
        # Очищаем canvas
        canvas.delete("all")
        
        # Получаем размеры canvas
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            # Canvas еще не инициализирован, откладываем отображение
            canvas.after(100, lambda: self.display_image_on_canvas(canvas, image))
            return
        
        # Получаем размеры изображения
        img_width, img_height = image.size
        
        # Вычисляем масштаб для вписывания в canvas
        scale_x = canvas_width / img_width
        scale_y = canvas_height / img_height
        scale = min(scale_x, scale_y, 1.0)  # Не увеличиваем изображение
        
        # Вычисляем новые размеры
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Изменяем размер изображения
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Конвертируем в PhotoImage
        photo = ImageTk.PhotoImage(resized_image)
        
        # Отображаем изображение по центру canvas
        x = (canvas_width - new_width) // 2
        y = (canvas_height - new_height) // 2
        
        canvas.create_image(x, y, anchor=tk.NW, image=photo)
        
        # Сохраняем ссылку на изображение
        canvas.image = photo
        
        # Настраиваем скроллинг
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def clear_canvas(self, canvas):
        """Очищает canvas."""
        canvas.delete("all")
        canvas.image = None
    
    def update_image_info(self):
        """Обновляет информацию об изображении."""
        if self.original_image:
            self.info_labels['size'].configure(text=f"{self.original_image.size[0]} × {self.original_image.size[1]}")
            self.info_labels['format'].configure(text=self.original_image.format or "Неизвестно")
            self.info_labels['mode'].configure(text=self.original_image.mode)
        else:
            self.info_labels['size'].configure(text="Не загружено")
            self.info_labels['format'].configure(text="Не загружено")
            self.info_labels['mode'].configure(text="Не загружено")
    
    def on_mousewheel_original(self, event):
        """Обрабатывает прокрутку колесика мыши для исходного изображения."""
        self.original_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def on_mousewheel_processed(self, event):
        """Обрабатывает прокрутку колесика мыши для обработанного изображения."""
        self.processed_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def start_drag_original(self, event):
        """Начинает перетаскивание для исходного изображения."""
        self.original_canvas.scan_mark(event.x, event.y)
    
    def drag_original(self, event):
        """Перетаскивает исходное изображение."""
        self.original_canvas.scan_dragto(event.x, event.y, gain=1)
    
    def start_drag_processed(self, event):
        """Начинает перетаскивание для обработанного изображения."""
        self.processed_canvas.scan_mark(event.x, event.y)
    
    def drag_processed(self, event):
        """Перетаскивает обработанное изображение."""
        self.processed_canvas.scan_dragto(event.x, event.y, gain=1)
    
    def toggle_fullscreen(self):
        """Переключает полноэкранный режим."""
        # TODO: Реализовать полноэкранный режим
        pass
    
    def load_image_dialog(self) -> Optional[str]:
        """
        Открывает диалог загрузки изображения.
        
        Returns:
            Optional[str]: Путь к выбранному файлу или None
        """
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
            self.on_image_loaded(file_path)
            return file_path
        
        return None
    
    def save_image_dialog(self) -> Optional[str]:
        """
        Открывает диалог сохранения изображения.
        
        Returns:
            Optional[str]: Путь для сохранения или None
        """
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
        
        return file_path if file_path else None
