"""
Современные стили для интерфейса в стиле фоторедактора.
"""

import tkinter as tk
from tkinter import ttk


class ModernStyles:
    """Класс для управления современными стилями интерфейса."""
    
    def __init__(self):
        """Инициализация стилей."""
        self.style = ttk.Style()
        self.setup_styles()
    
    def setup_styles(self):
        """Настраивает все стили интерфейса."""
        # Основная тема
        self.style.theme_use('clam')
        
        # Цветовая схема в стиле фоторедактора
        self.colors = {
            'bg_primary': '#2b2b2b',      # Основной фон
            'bg_secondary': '#3c3c3c',    # Вторичный фон (панели)
            'bg_tertiary': '#1e1e1e',     # Третичный фон (canvas)
            'accent_primary': '#0078d4',  # Основной акцент
            'accent_secondary': '#106ebe', # Вторичный акцент
            'accent_hover': '#005a9e',     # Акцент при наведении
            'text_primary': '#ffffff',     # Основной текст
            'text_secondary': '#cccccc',  # Вторичный текст
            'text_muted': '#999999',       # Приглушенный текст
            'border': '#555555',          # Границы
            'success': '#28a745',         # Успех
            'warning': '#ffc107',         # Предупреждение
            'error': '#dc3545',           # Ошибка
            'info': '#17a2b8'             # Информация
        }
        
        # Настройка основных стилей
        self._setup_frame_styles()
        self._setup_label_styles()
        self._setup_button_styles()
        self._setup_entry_styles()
        self._setup_combobox_styles()
        self._setup_text_styles()
        self._setup_scrollbar_styles()
        self._setup_notebook_styles()
        self._setup_radiobutton_styles()
        self._setup_checkbutton_styles()
    
    def _setup_frame_styles(self):
        """Настраивает стили фреймов."""
        self.style.configure('Modern.TFrame', 
                           background=self.colors['bg_primary'])
        
        self.style.configure('Modern.TLabelFrame', 
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           relief='solid')
        
        self.style.configure('Modern.TLabelFrame.Label', 
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 10, 'bold'))
    
    def _setup_label_styles(self):
        """Настраивает стили меток."""
        self.style.configure('Modern.TLabel', 
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9))
        
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 18, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 11, 'bold'))
        
        self.style.configure('Status.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 8),
                           relief='flat')
    
    def _setup_button_styles(self):
        """Настраивает стили кнопок."""
        # Основные кнопки
        self.style.configure('Modern.TButton', 
                           background=self.colors['accent_primary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9, 'bold'),
                           borderwidth=0,
                           focuscolor='none',
                           padding=(10, 5))
        
        self.style.map('Modern.TButton',
                      background=[('active', self.colors['accent_secondary']),
                                ('pressed', self.colors['accent_hover'])])
        
        # Вторичные кнопки
        self.style.configure('Secondary.TButton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9),
                           borderwidth=1,
                           relief='solid')
        
        self.style.map('Secondary.TButton',
                      background=[('active', self.colors['accent_primary']),
                                ('pressed', self.colors['accent_secondary'])])
        
        # Кнопки действий
        self.style.configure('Action.TButton',
                           background=self.colors['success'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9, 'bold'))
        
        self.style.map('Action.TButton',
                      background=[('active', '#218838'),
                                ('pressed', '#1e7e34')])
    
    def _setup_entry_styles(self):
        """Настраивает стили полей ввода."""
        self.style.configure('Modern.TEntry',
                           fieldbackground=self.colors['bg_secondary'],
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           insertcolor=self.colors['text_primary'],
                           font=('Segoe UI', 9))
        
        self.style.map('Modern.TEntry',
                      fieldbackground=[('focus', self.colors['bg_tertiary'])])
    
    def _setup_combobox_styles(self):
        """Настраивает стили выпадающих списков."""
        self.style.configure('Modern.TCombobox',
                           fieldbackground=self.colors['bg_secondary'],
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           arrowcolor=self.colors['text_primary'],
                           font=('Segoe UI', 9))
        
        self.style.map('Modern.TCombobox',
                      fieldbackground=[('focus', self.colors['bg_tertiary'])])
    
    def _setup_text_styles(self):
        """Настраивает стили текстовых виджетов."""
        self.style.configure('Modern.TText',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           insertcolor=self.colors['text_primary'],
                           font=('Segoe UI', 9))
    
    def _setup_scrollbar_styles(self):
        """Настраивает стили скроллбаров."""
        self.style.configure('Modern.TScrollbar',
                           background=self.colors['bg_secondary'],
                           troughcolor=self.colors['bg_primary'],
                           borderwidth=0,
                           arrowcolor=self.colors['text_primary'])
        
        self.style.map('Modern.TScrollbar',
                      background=[('active', self.colors['accent_primary'])])
    
    def _setup_notebook_styles(self):
        """Настраивает стили notebook."""
        self.style.configure('Modern.TNotebook',
                           background=self.colors['bg_primary'],
                           borderwidth=0)
        
        self.style.configure('Modern.TNotebook.Tab',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           padding=(10, 5),
                           font=('Segoe UI', 9))
        
        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', self.colors['accent_primary']),
                                ('active', self.colors['accent_secondary'])])
    
    def _setup_radiobutton_styles(self):
        """Настраивает стили радиокнопок."""
        self.style.configure('Modern.TRadiobutton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9),
                           focuscolor='none')
        
        self.style.map('Modern.TRadiobutton',
                      background=[('active', self.colors['accent_primary'])])
    
    def _setup_checkbutton_styles(self):
        """Настраивает стили чекбоксов."""
        self.style.configure('Modern.TCheckbutton',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9),
                           focuscolor='none')
        
        self.style.map('Modern.TCheckbutton',
                      background=[('active', self.colors['accent_primary'])])
    
    def get_color(self, color_name: str) -> str:
        """
        Возвращает цвет по имени.
        
        Args:
            color_name: Имя цвета
            
        Returns:
            str: HEX код цвета
        """
        return self.colors.get(color_name, '#000000')
    
    def create_gradient_frame(self, parent, colors: list, direction: str = 'horizontal'):
        """
        Создает фрейм с градиентом.
        
        Args:
            parent: Родительский виджет
            colors: Список цветов для градиента
            direction: Направление градиента ('horizontal' или 'vertical')
            
        Returns:
            tk.Canvas: Canvas с градиентом
        """
        canvas = tk.Canvas(parent, highlightthickness=0)
        
        def draw_gradient():
            canvas.delete("gradient")
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            if width <= 1 or height <= 1:
                canvas.after(10, draw_gradient)
                return
            
            if direction == 'horizontal':
                for i in range(width):
                    ratio = i / width
                    color = self._interpolate_color(colors[0], colors[1], ratio)
                    canvas.create_line(i, 0, i, height, fill=color, tags="gradient")
            else:
                for i in range(height):
                    ratio = i / height
                    color = self._interpolate_color(colors[0], colors[1], ratio)
                    canvas.create_line(0, i, width, i, fill=color, tags="gradient")
        
        canvas.bind('<Configure>', lambda e: draw_gradient())
        return canvas
    
    def _interpolate_color(self, color1: str, color2: str, ratio: float) -> str:
        """
        Интерполирует между двумя цветами.
        
        Args:
            color1: Первый цвет (HEX)
            color2: Второй цвет (HEX)
            ratio: Коэффициент интерполяции (0-1)
            
        Returns:
            str: Интерполированный цвет (HEX)
        """
        # Убираем # если есть
        color1 = color1.lstrip('#')
        color2 = color2.lstrip('#')
        
        # Конвертируем в RGB
        r1, g1, b1 = int(color1[0:2], 16), int(color1[2:4], 16), int(color1[4:6], 16)
        r2, g2, b2 = int(color2[0:2], 16), int(color2[2:4], 16), int(color2[4:6], 16)
        
        # Интерполируем
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        
        return f"#{r:02x}{g:02x}{b:02x}"
