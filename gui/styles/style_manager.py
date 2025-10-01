"""
Менеджер стилей для приложения.
Содержит настройку всех стилей интерфейса.
"""

from tkinter import ttk
from constants import COLORS, FONTS, TTK_STYLES


class StyleManager:
    """Менеджер стилей для настройки интерфейса."""
    
    def __init__(self):
        self.style = ttk.Style()
        self.setup_styles()
    
    def setup_styles(self):
        """Настраивает все стили интерфейса."""
        self.style.theme_use('clam')
        self._setup_frame_styles()
        self._setup_label_styles()
        self._setup_button_styles()
        self._setup_input_styles()
        self._setup_text_styles()
        self._setup_title_styles()
        self._setup_status_styles()
    
    def _setup_frame_styles(self):
        """Настраивает стили фреймов."""
        self.style.configure(
            TTK_STYLES['Modern.TFrame'], 
            background=COLORS['background']
        )
        
        self.style.configure(
            TTK_STYLES['Modern.TLabelFrame'], 
            background=COLORS['panel'], 
            foreground=COLORS['text'],
            borderwidth=1,
            relief='solid'
        )
        
        self.style.configure(
            'Modern.TLabelFrame.Label', 
            background=COLORS['panel'], 
            foreground=COLORS['text'],
            font=FONTS['label']
        )
        
        # Настройка layout для LabelFrame
        self.style.layout(
            TTK_STYLES['Modern.TLabelFrame'],
            [('LabelFrame.border', {'sticky': 'nswe'})]
        )
        self.style.layout(
            'Modern.TLabelFrame.Label',
            [('LabelFrame.padding', {'sticky': 'nswe'})]
        )
    
    def _setup_label_styles(self):
        """Настраивает стили меток."""
        self.style.configure(
            TTK_STYLES['Modern.TLabel'], 
            background=COLORS['panel'], 
            foreground=COLORS['text'],
            font=FONTS['text']
        )
    
    def _setup_button_styles(self):
        """Настраивает стили кнопок."""
        self.style.configure(
            TTK_STYLES['Modern.TButton'], 
            background=COLORS['accent'],
            foreground=COLORS['text'],
            font=FONTS['text'],
            borderwidth=0,
            focuscolor='none'
        )
        
        self.style.map(
            TTK_STYLES['Modern.TButton'],
            background=[
                ('active', '#106ebe'),
                ('pressed', '#005a9e')
            ]
        )
    
    def _setup_input_styles(self):
        """Настраивает стили полей ввода."""
        self.style.configure(
            TTK_STYLES['Modern.TCombobox'],
            fieldbackground=COLORS['panel'],
            background=COLORS['panel'],
            foreground=COLORS['text'],
            borderwidth=1,
            arrowcolor=COLORS['text']
        )
        
        self.style.map(
            TTK_STYLES['Modern.TCombobox'],
            fieldbackground=[('readonly', COLORS['panel'])],
            background=[('readonly', COLORS['panel'])]
        )
        
        self.style.configure(
            TTK_STYLES['Modern.TEntry'],
            fieldbackground=COLORS['panel'],
            background=COLORS['panel'],
            foreground=COLORS['text'],
            borderwidth=1,
            insertcolor=COLORS['text']
        )
    
    def _setup_text_styles(self):
        """Настраивает стили текстовых областей."""
        self.style.configure(
            TTK_STYLES['Modern.TText'],
            background=COLORS['panel'],
            foreground=COLORS['text'],
            borderwidth=1,
            insertcolor=COLORS['text']
        )
    
    def _setup_title_styles(self):
        """Настраивает стили заголовков."""
        self.style.configure(
            TTK_STYLES['Title.TLabel'],
            background=COLORS['background'],
            foreground=COLORS['text'],
            font=FONTS['title']
        )
    
    def _setup_status_styles(self):
        """Настраивает стили статусной строки."""
        self.style.configure(
            TTK_STYLES['Status.TLabel'],
            background=COLORS['panel'],
            foreground=COLORS['text'],
            font=FONTS['status'],
            relief='flat'
        )
