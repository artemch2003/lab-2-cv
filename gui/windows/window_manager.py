"""
Менеджер окон для приложения.
Содержит логику создания и управления окнами.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, COLORS, 
    COMPARISON_WINDOW_SIZE, SHARPNESS_WINDOW_SIZE, DIFF_WINDOW_SIZE,
    DISPLAY_IMAGE_SIZE, FULL_DIFF_MAP_SIZE
)
from gui.components.ui_factory import UIFactory


class WindowManager:
    """Менеджер окон для создания и управления окнами."""
    
    def __init__(self, root):
        self.root = root
        self.ui_factory = UIFactory()
    
    def setup_main_window(self):
        """Настраивает главное окно."""
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLORS['background'])
        
        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (WINDOW_HEIGHT // 2)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    
    def create_comparison_window(self, title="Сравнение качества фильтров"):
        """Создает окно для сравнения фильтров."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(COMPARISON_WINDOW_SIZE)
        window.configure(bg=COLORS['background'])
        return window
    
    def create_sharpness_window(self, title="Сравнение фильтров резкости"):
        """Создает окно для сравнения фильтров резкости."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(SHARPNESS_WINDOW_SIZE)
        window.configure(bg=COLORS['background'])
        return window
    
    def create_diff_window(self, title="Карта абсолютной разности"):
        """Создает окно для отображения карты разности."""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry(DIFF_WINDOW_SIZE)
        window.configure(bg=COLORS['background'])
        return window
    
    def create_canvas_for_window(self, window, size=DISPLAY_IMAGE_SIZE):
        """Создает canvas для отображения изображений в окне."""
        canvas = tk.Canvas(window, bg=COLORS['canvas_bg'], highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        return canvas
    
    def display_image_in_canvas(self, canvas, image, size=None):
        """Отображает изображение в canvas."""
        if image is None:
            return
            
        if size is None:
            size = DISPLAY_IMAGE_SIZE
            
        # Изменяем размер для отображения
        display_image = image.copy()
        display_image.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Конвертируем в PhotoImage
        photo = ImageTk.PhotoImage(display_image)
        
        # Очищаем canvas и отображаем изображение (якорь в левом верхнем углу)
        canvas.delete("all")
        canvas.create_image(
            0,
            0,
            image=photo,
            anchor='nw'
        )
        canvas.image = photo  # Сохраняем ссылку
        
        return photo
    
    def show_error(self, title, message):
        """Показывает диалог ошибки."""
        messagebox.showerror(title, message)
    
    def show_warning(self, title, message):
        """Показывает диалог предупреждения."""
        messagebox.showwarning(title, message)
    
    def show_info(self, title, message):
        """Показывает информационный диалог."""
        messagebox.showinfo(title, message)
