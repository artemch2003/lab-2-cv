"""
Базовые классы для UI компонентов.
Содержит общие компоненты для устранения дублирования кода.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from constants import COLORS, FONTS, DISPLAY_IMAGE_SIZE, MESSAGES


class BaseCanvas:
    """Базовый класс для canvas с изображениями."""
    
    def __init__(self, parent, width=400, height=300):
        self.canvas = tk.Canvas(
            parent, 
            bg=COLORS['canvas_bg'], 
            highlightthickness=0,
            width=width,
            height=height
        )
        self.image = None
        self.photo = None
        
    def pack(self, **kwargs):
        """Упаковывает canvas в родительский контейнер."""
        self.canvas.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Размещает canvas в сетке."""
        self.canvas.grid(**kwargs)
        
    def display_placeholder(self, text):
        """Отображает placeholder текст."""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.canvas.winfo_width() // 2, 
            self.canvas.winfo_height() // 2, 
            text=text, 
            fill=COLORS['placeholder'], 
            font=FONTS['placeholder'], 
            justify=tk.CENTER
        )
        
    def display_image(self, image):
        """Отображает изображение на canvas."""
        if image is None:
            return
            
        # Изменяем размер для отображения
        display_image = image.copy()
        display_image.thumbnail(DISPLAY_IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        # Конвертируем в PhotoImage
        self.photo = ImageTk.PhotoImage(display_image)
        
        # Очищаем canvas и отображаем изображение
        self.canvas.delete("all")
        self.canvas.create_image(
            self.canvas.winfo_width() // 2, 
            self.canvas.winfo_height() // 2, 
            image=self.photo
        )
        self.canvas.image = self.photo  # Сохраняем ссылку


class BaseParameterFrame:
    """Базовый класс для фреймов с параметрами."""
    
    def __init__(self, parent):
        self.frame = ttk.Frame(parent, style='Modern.TFrame')
        self.elements = {}
        
    def pack(self, **kwargs):
        """Упаковывает фрейм в родительский контейнер."""
        self.frame.pack(**kwargs)
        
    def hide_all_elements(self):
        """Скрывает все элементы параметров."""
        for element in self.elements.values():
            if hasattr(element, 'pack_forget'):
                element.pack_forget()
                
    def show_elements(self, element_names):
        """Показывает указанные элементы."""
        self.hide_all_elements()
        for name in element_names:
            if name in self.elements:
                self.elements[name].pack(anchor=tk.W, pady=(5, 0))


class BaseInfoPanel:
    """Базовый класс для информационных панелей."""
    
    def __init__(self, parent, height=3):
        self.text_widget = tk.Text(
            parent, 
            height=height, 
            wrap=tk.WORD, 
            bg=COLORS['panel'], 
            fg=COLORS['text'], 
            font=FONTS['text']
        )
        
    def pack(self, **kwargs):
        """Упаковывает текстовое поле."""
        self.text_widget.pack(**kwargs)
        
    def update_info(self, message):
        """Обновляет информацию в панели."""
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(1.0, message)
        self.text_widget.configure(state=tk.DISABLED)


class BaseButton:
    """Базовый класс для кнопок."""
    
    def __init__(self, parent, text, command, style='Modern.TButton'):
        self.button = ttk.Button(
            parent, 
            text=text, 
            style=style, 
            command=command
        )
        
    def pack(self, **kwargs):
        """Упаковывает кнопку."""
        self.button.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Размещает кнопку в сетке."""
        self.button.grid(**kwargs)


class BaseLabel:
    """Базовый класс для меток."""
    
    def __init__(self, parent, text, style='Modern.TLabel'):
        self.label = ttk.Label(parent, text=text, style=style)
        
    def pack(self, **kwargs):
        """Упаковывает метку."""
        self.label.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Размещает метку в сетке."""
        self.label.grid(**kwargs)


class BaseEntry:
    """Базовый класс для полей ввода."""
    
    def __init__(self, parent, textvariable=None, width=15, style='Modern.TEntry'):
        self.entry = ttk.Entry(
            parent, 
            textvariable=textvariable, 
            width=width, 
            style=style
        )
        
    def pack(self, **kwargs):
        """Упаковывает поле ввода."""
        self.entry.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Размещает поле ввода в сетке."""
        self.entry.grid(**kwargs)


class BaseCombobox:
    """Базовый класс для выпадающих списков."""
    
    def __init__(self, parent, values, textvariable=None, width=20, style='Modern.TCombobox'):
        self.combobox = ttk.Combobox(
            parent,
            values=values,
            textvariable=textvariable,
            state="readonly",
            width=width,
            style=style
        )
        
    def pack(self, **kwargs):
        """Упаковывает выпадающий список."""
        self.combobox.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Размещает выпадающий список в сетке."""
        self.combobox.grid(**kwargs)
        
    def get(self):
        """Возвращает выбранное значение."""
        return self.combobox.get()
        
    def set(self, value):
        """Устанавливает значение."""
        self.combobox.set(value)
        
    def bind(self, event, handler):
        """Привязывает обработчик события."""
        self.combobox.bind(event, handler)


class BaseText:
    """Базовый класс для текстовых областей."""
    
    def __init__(self, parent, height=4, width=30, style='Modern.TText'):
        self.text_widget = tk.Text(
            parent, 
            height=height, 
            width=width, 
            wrap=tk.WORD, 
            bg=COLORS['panel'], 
            fg=COLORS['text'], 
            font=FONTS['text']
        )
        
    def pack(self, **kwargs):
        """Упаковывает текстовую область."""
        self.text_widget.pack(**kwargs)
        
    def insert(self, index, text):
        """Вставляет текст."""
        self.text_widget.insert(index, text)
        
    def delete(self, start, end):
        """Удаляет текст."""
        self.text_widget.delete(start, end)
        
    def configure(self, **kwargs):
        """Настраивает виджет."""
        self.text_widget.configure(**kwargs)


class BaseLabelFrame:
    """Базовый класс для фреймов с заголовками."""
    
    def __init__(self, parent, text, padding="10", style='Modern.TLabelFrame'):
        self.frame = ttk.LabelFrame(
            parent, 
            text=text, 
            style=style, 
            padding=padding
        )
        
    def pack(self, **kwargs):
        """Упаковывает фрейм."""
        self.frame.pack(**kwargs)
        
    def grid(self, **kwargs):
        """Размещает фрейм в сетке."""
        self.frame.grid(**kwargs)
        
    def columnconfigure(self, index, **kwargs):
        """Настраивает колонку."""
        self.frame.columnconfigure(index, **kwargs)
