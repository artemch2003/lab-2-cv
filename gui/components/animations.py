"""
Компоненты для анимаций и визуальных эффектов.
"""

import tkinter as tk
from typing import Callable, Optional
import math
import time


class AnimationManager:
    """Менеджер анимаций для интерфейса."""
    
    def __init__(self):
        """Инициализация менеджера анимаций."""
        self.active_animations = {}
        self.animation_id = 0
    
    def fade_in(self, widget: tk.Widget, duration: int = 300, callback: Optional[Callable] = None):
        """
        Анимация появления виджета.
        
        Args:
            widget: Виджет для анимации
            duration: Длительность анимации в миллисекундах
            callback: Callback после завершения анимации
        """
        animation_id = self._get_next_animation_id()
        self.active_animations[animation_id] = {
            'widget': widget,
            'type': 'fade_in',
            'duration': duration,
            'start_time': 0,
            'callback': callback
        }
        self._start_animation(animation_id)
    
    def fade_out(self, widget: tk.Widget, duration: int = 300, callback: Optional[Callable] = None):
        """
        Анимация исчезновения виджета.
        
        Args:
            widget: Виджет для анимации
            duration: Длительность анимации в миллисекундах
            callback: Callback после завершения анимации
        """
        animation_id = self._get_next_animation_id()
        self.active_animations[animation_id] = {
            'widget': widget,
            'type': 'fade_out',
            'duration': duration,
            'start_time': 0,
            'callback': callback
        }
        self._start_animation(animation_id)
    
    def slide_in(self, widget: tk.Widget, direction: str = 'left', duration: int = 300, callback: Optional[Callable] = None):
        """
        Анимация входа виджета.
        
        Args:
            widget: Виджет для анимации
            direction: Направление ('left', 'right', 'top', 'bottom')
            duration: Длительность анимации в миллисекундах
            callback: Callback после завершения анимации
        """
        animation_id = self._get_next_animation_id()
        self.active_animations[animation_id] = {
            'widget': widget,
            'type': 'slide_in',
            'direction': direction,
            'duration': duration,
            'start_time': 0,
            'callback': callback
        }
        self._start_animation(animation_id)
    
    def slide_out(self, widget: tk.Widget, direction: str = 'left', duration: int = 300, callback: Optional[Callable] = None):
        """
        Анимация выхода виджета.
        
        Args:
            widget: Виджет для анимации
            direction: Направление ('left', 'right', 'top', 'bottom')
            duration: Длительность анимации в миллисекундах
            callback: Callback после завершения анимации
        """
        animation_id = self._get_next_animation_id()
        self.active_animations[animation_id] = {
            'widget': widget,
            'type': 'slide_out',
            'direction': direction,
            'duration': duration,
            'start_time': 0,
            'callback': callback
        }
        self._start_animation(animation_id)
    
    def pulse(self, widget: tk.Widget, duration: int = 1000, callback: Optional[Callable] = None):
        """
        Анимация пульсации виджета.
        
        Args:
            widget: Виджет для анимации
            duration: Длительность анимации в миллисекундах
            callback: Callback после завершения анимации
        """
        animation_id = self._get_next_animation_id()
        self.active_animations[animation_id] = {
            'widget': widget,
            'type': 'pulse',
            'duration': duration,
            'start_time': 0,
            'callback': callback
        }
        self._start_animation(animation_id)
    
    def shake(self, widget: tk.Widget, intensity: int = 10, duration: int = 500, callback: Optional[Callable] = None):
        """
        Анимация тряски виджета.
        
        Args:
            widget: Виджет для анимации
            intensity: Интенсивность тряски
            duration: Длительность анимации в миллисекундах
            callback: Callback после завершения анимации
        """
        animation_id = self._get_next_animation_id()
        self.active_animations[animation_id] = {
            'widget': widget,
            'type': 'shake',
            'intensity': intensity,
            'duration': duration,
            'start_time': 0,
            'callback': callback
        }
        self._start_animation(animation_id)
    
    def _get_next_animation_id(self) -> int:
        """Возвращает следующий ID анимации."""
        self.animation_id += 1
        return self.animation_id
    
    def _start_animation(self, animation_id: int):
        """Запускает анимацию."""
        if animation_id not in self.active_animations:
            return
        
        animation = self.active_animations[animation_id]
        animation['start_time'] = time.time() * 1000  # В миллисекундах
        self._update_animation(animation_id)
    
    def _update_animation(self, animation_id: int):
        """Обновляет анимацию."""
        if animation_id not in self.active_animations:
            return
        
        animation = self.active_animations[animation_id]
        widget = animation['widget']
        current_time = time.time() * 1000
        elapsed = current_time - animation['start_time']
        progress = min(elapsed / animation['duration'], 1.0)
        
        if progress >= 1.0:
            # Анимация завершена
            self._finish_animation(animation_id)
            return
        
        # Применяем анимацию в зависимости от типа
        if animation['type'] == 'fade_in':
            self._apply_fade_in(widget, progress)
        elif animation['type'] == 'fade_out':
            self._apply_fade_out(widget, progress)
        elif animation['type'] == 'slide_in':
            self._apply_slide_in(widget, animation['direction'], progress)
        elif animation['type'] == 'slide_out':
            self._apply_slide_out(widget, animation['direction'], progress)
        elif animation['type'] == 'pulse':
            self._apply_pulse(widget, progress)
        elif animation['type'] == 'shake':
            self._apply_shake(widget, animation['intensity'], progress)
        
        # Планируем следующий кадр
        widget.after(16, lambda: self._update_animation(animation_id))  # ~60 FPS
    
    def _apply_fade_in(self, widget: tk.Widget, progress: float):
        """Применяет анимацию появления."""
        # Для tkinter виджетов используем изменение прозрачности через атрибуты
        # Это упрощенная версия, в реальности может потребоваться более сложная реализация
        pass
    
    def _apply_fade_out(self, widget: tk.Widget, progress: float):
        """Применяет анимацию исчезновения."""
        pass
    
    def _apply_slide_in(self, widget: tk.Widget, direction: str, progress: float):
        """Применяет анимацию входа."""
        # Получаем текущую позицию
        x, y = widget.winfo_x(), widget.winfo_y()
        
        # Вычисляем смещение
        if direction == 'left':
            offset = int((1 - progress) * -widget.winfo_width())
        elif direction == 'right':
            offset = int((1 - progress) * widget.winfo_width())
        elif direction == 'top':
            offset = int((1 - progress) * -widget.winfo_height())
        elif direction == 'bottom':
            offset = int((1 - progress) * widget.winfo_height())
        else:
            offset = 0
        
        # Применяем смещение
        if direction in ['left', 'right']:
            widget.place(x=x + offset, y=y)
        else:
            widget.place(x=x, y=y + offset)
    
    def _apply_slide_out(self, widget: tk.Widget, direction: str, progress: float):
        """Применяет анимацию выхода."""
        # Аналогично slide_in, но в обратном направлении
        pass
    
    def _apply_pulse(self, widget: tk.Widget, progress: float):
        """Применяет анимацию пульсации."""
        # Создаем эффект пульсации через изменение размера
        scale = 1.0 + 0.1 * math.sin(progress * math.pi * 2)
        # Здесь можно изменить размер виджета
        pass
    
    def _apply_shake(self, widget: tk.Widget, intensity: int, progress: float):
        """Применяет анимацию тряски."""
        # Создаем случайное смещение
        import random
        shake_x = random.randint(-intensity, intensity) * (1 - progress)
        shake_y = random.randint(-intensity, intensity) * (1 - progress)
        
        x, y = widget.winfo_x(), widget.winfo_y()
        widget.place(x=x + shake_x, y=y + shake_y)
    
    def _finish_animation(self, animation_id: int):
        """Завершает анимацию."""
        if animation_id not in self.active_animations:
            return
        
        animation = self.active_animations[animation_id]
        
        # Вызываем callback если есть
        if animation['callback']:
            animation['callback']()
        
        # Удаляем анимацию из активных
        del self.active_animations[animation_id]
    
    def stop_all_animations(self):
        """Останавливает все активные анимации."""
        self.active_animations.clear()
    
    def stop_animation(self, animation_id: int):
        """Останавливает конкретную анимацию."""
        if animation_id in self.active_animations:
            del self.active_animations[animation_id]


class LoadingSpinner:
    """Спиннер загрузки."""
    
    def __init__(self, parent: tk.Widget, size: int = 40, color: str = '#0078d4'):
        """
        Инициализация спиннера.
        
        Args:
            parent: Родительский виджет
            size: Размер спиннера
            color: Цвет спиннера
        """
        self.parent = parent
        self.size = size
        self.color = color
        self.canvas = tk.Canvas(parent, width=size, height=size, highlightthickness=0, bg='#2b2b2b')
        self.angle = 0
        self.animation_id = None
    
    def start(self):
        """Запускает анимацию спиннера."""
        self._animate()
    
    def stop(self):
        """Останавливает анимацию спиннера."""
        if self.animation_id:
            self.parent.after_cancel(self.animation_id)
            self.animation_id = None
    
    def _animate(self):
        """Анимирует спиннер."""
        self.canvas.delete("all")
        
        # Рисуем спиннер
        center_x, center_y = self.size // 2, self.size // 2
        radius = self.size // 2 - 5
        
        for i in range(8):
            angle = (self.angle + i * 45) % 360
            x = center_x + radius * math.cos(math.radians(angle))
            y = center_y + radius * math.sin(math.radians(angle))
            
            # Прозрачность зависит от позиции
            alpha = 1.0 - (i / 8.0)
            color = self._adjust_alpha(self.color, alpha)
            
            self.canvas.create_oval(x-3, y-3, x+3, y+3, fill=color, outline="")
        
        self.angle = (self.angle + 10) % 360
        self.animation_id = self.parent.after(50, self._animate)
    
    def _adjust_alpha(self, color: str, alpha: float) -> str:
        """
        Регулирует прозрачность цвета.
        
        Args:
            color: HEX цвет
            alpha: Прозрачность (0-1)
            
        Returns:
            str: Цвет с прозрачностью
        """
        # Упрощенная версия, в реальности может потребоваться более сложная реализация
        return color
    
    def pack(self, **kwargs):
        """Упаковывает спиннер."""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Размещает спиннер в сетке."""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        """Размещает спиннер."""
        self.canvas.place(**kwargs)


class ProgressBar:
    """Современная прогресс-бар."""
    
    def __init__(self, parent: tk.Widget, width: int = 200, height: int = 20, 
                 bg_color: str = '#3c3c3c', fill_color: str = '#0078d4'):
        """
        Инициализация прогресс-бара.
        
        Args:
            parent: Родительский виджет
            width: Ширина прогресс-бара
            height: Высота прогресс-бара
            bg_color: Цвет фона
            fill_color: Цвет заполнения
        """
        self.parent = parent
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.progress = 0
        
        self.canvas = tk.Canvas(parent, width=width, height=height, 
                               highlightthickness=0, bg=bg_color)
        self._draw()
    
    def _draw(self):
        """Рисует прогресс-бар."""
        self.canvas.delete("all")
        
        # Фон
        self.canvas.create_rectangle(0, 0, self.width, self.height, 
                                   fill=self.bg_color, outline="")
        
        # Заполнение
        fill_width = int(self.width * self.progress / 100)
        if fill_width > 0:
            self.canvas.create_rectangle(0, 0, fill_width, self.height, 
                                       fill=self.fill_color, outline="")
        
        # Текст прогресса
        text = f"{int(self.progress)}%"
        self.canvas.create_text(self.width // 2, self.height // 2, 
                              text=text, fill='#ffffff', font=('Segoe UI', 9))
    
    def set_progress(self, progress: int):
        """
        Устанавливает прогресс.
        
        Args:
            progress: Прогресс в процентах (0-100)
        """
        self.progress = max(0, min(100, progress))
        self._draw()
    
    def pack(self, **kwargs):
        """Упаковывает прогресс-бар."""
        self.canvas.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Размещает прогресс-бар в сетке."""
        self.canvas.grid(**kwargs)
    
    def place(self, **kwargs):
        """Размещает прогресс-бар."""
        self.canvas.place(**kwargs)
