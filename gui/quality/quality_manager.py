"""
Менеджер качества для приложения.
Содержит логику анализа качества и сравнения фильтров.
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image
from constants import AVAILABLE_FILTERS, SHARPNESS_KERNEL_SIZES, SHARPNESS_LAMBDA_VALUES
from gui.components.ui_factory import UIFactory
from gui.windows.window_manager import WindowManager


class QualityManager:
    """Менеджер качества для анализа и сравнения фильтров."""
    
    def __init__(self, parent, window_manager):
        self.parent = parent
        self.window_manager = window_manager
        self.ui_factory = UIFactory()
        self.quality_assessor = None
        self.quality_metrics = None
        self.difference_map = None
    
    def create_quality_panel(self, parent):
        """Создает панель оценки качества."""
        quality_frame = self.ui_factory.create_label_frame(
            parent, "Оценка качества обработки", padding="15"
        )
        quality_frame.pack(fill=tk.X, pady=(10, 0), padx=20)
        
        # Кнопки управления качеством
        self._create_quality_buttons(quality_frame.frame)
        
        # Область отображения карты разности
        self._create_difference_map_area(quality_frame.frame)
        
        return quality_frame
    
    def _create_quality_buttons(self, parent):
        """Создает кнопки управления качеством."""
        buttons_frame = ttk.Frame(parent, style='Modern.TFrame')
        buttons_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопка анализа качества
        self.analyze_quality_btn = self.ui_factory.create_button(
            buttons_frame, "📊 Анализ качества", self.analyze_quality
        )
        self.analyze_quality_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # Кнопка показа карты разности
        self.show_diff_map_btn = self.ui_factory.create_button(
            buttons_frame, "🗺️ Карта разности", self.show_difference_map
        )
        self.show_diff_map_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка сравнения фильтров
        self.compare_filters_btn = self.ui_factory.create_button(
            buttons_frame, "⚖️ Сравнить фильтры", self.compare_filters
        )
        self.compare_filters_btn.pack(side=tk.LEFT, padx=5)
        
        # Кнопка сравнения фильтров резкости
        self.compare_sharpness_btn = self.ui_factory.create_button(
            buttons_frame, "🔍 Сравнить резкость", self.compare_sharpness_filters
        )
        self.compare_sharpness_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_difference_map_area(self, parent):
        """Создает область отображения карты разности."""
        diff_frame = self.ui_factory.create_label_frame(
            parent, "Карта абсолютной разности", padding="5"
        )
        diff_frame.pack(fill=tk.BOTH, expand=True)
        
        self.diff_canvas = tk.Canvas(
            diff_frame.frame, 
            bg="#1e1e1e", 
            highlightthickness=0, 
            height=200
        )
        self.diff_canvas.pack(fill=tk.BOTH, expand=True)
        self.diff_canvas.create_text(
            200, 100, 
            text="Нажмите 'Анализ качества' для просмотра карты разности", 
            fill="#666666", 
            font=("Segoe UI", 10), 
            justify=tk.CENTER
        )
    
    def analyze_quality(self, original_image, processed_image, update_info_callback):
        """Анализирует качество обработки изображения."""
        if not original_image or not processed_image:
            self.window_manager.show_warning(
                "Предупреждение", 
                "Сначала загрузите изображение и примените преобразование"
            )
            return
        
        try:
            # Инициализируем оценщик качества
            from image_processing.quality_assessment import QualityAssessment
            self.quality_assessor = QualityAssessment()
            
            # Конвертируем изображения в numpy arrays
            import numpy as np
            original_array = np.array(original_image)
            processed_array = np.array(processed_image)
            
            # Вычисляем метрики качества
            self.quality_metrics = self.quality_assessor.compute_quality_metrics(
                original_array, processed_array
            )
            
            # Вычисляем карту разности
            self.difference_map = self.quality_assessor.compute_absolute_difference_map(
                original_array, processed_array
            )
            
            # Отображаем карту разности
            self.display_difference_map()
            
            # Обновляем информацию
            quality_report = self.quality_assessor.format_quality_report(self.quality_metrics)
            update_info_callback(f"Анализ качества завершен\n{quality_report}")
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось проанализировать качество: {e}")
    
    def display_difference_map(self):
        """Отображает карту разности."""
        if self.difference_map is None:
            return
        
        try:
            # Создаем визуализацию карты разности
            visualization = self.quality_assessor.create_visualization_map(self.difference_map, 'hot')
            
            # Конвертируем в PIL Image
            if len(visualization.shape) == 3:
                diff_image = Image.fromarray(visualization)
            else:
                diff_image = Image.fromarray(visualization, mode='L')
            
            # Изменяем размер для отображения
            from constants import DISPLAY_IMAGE_SIZE
            display_image = diff_image.copy()
            display_image.thumbnail(DISPLAY_IMAGE_SIZE, Image.Resampling.LANCZOS)
            
            # Конвертируем в PhotoImage
            photo = ImageTk.PhotoImage(display_image)
            
            # Очищаем canvas и отображаем карту
            self.diff_canvas.delete("all")
            self.diff_canvas.create_image(200, 100, image=photo)
            self.diff_canvas.image = photo  # Сохраняем ссылку
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось отобразить карту разности: {e}")
    
    def show_difference_map(self):
        """Показывает карту разности в отдельном окне."""
        if self.difference_map is None:
            self.window_manager.show_warning("Предупреждение", "Сначала выполните анализ качества")
            return
        
        try:
            # Создаем новое окно
            diff_window = self.window_manager.create_diff_window()
            
            # Создаем canvas для отображения
            canvas = self.window_manager.create_canvas_for_window(diff_window)
            
            # Создаем визуализацию
            visualization = self.quality_assessor.create_visualization_map(self.difference_map, 'hot')
            
            # Конвертируем в PIL Image
            if len(visualization.shape) == 3:
                diff_image = Image.fromarray(visualization)
            else:
                diff_image = Image.fromarray(visualization, mode='L')
            
            # Отображаем карту
            self.window_manager.display_image_in_canvas(canvas, diff_image)
            
            # Добавляем информацию
            info_text = f"Средняя разность: {self.quality_metrics['mean_difference']:.2f}\n"
            info_text += f"Максимальная разность: {self.quality_metrics['max_difference']}\n"
            info_text += f"Оценка качества: {self.quality_metrics['quality_rating']}"
            
            info_label = tk.Label(
                diff_window, 
                text=info_text, 
                bg="#2b2b2b", 
                fg="#ffffff", 
                font=("Segoe UI", 10)
            )
            info_label.pack(pady=5)
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось показать карту разности: {e}")
    
    def compare_filters(self, original_image, update_info_callback):
        """Сравнивает качество различных фильтров."""
        if not original_image:
            self.window_manager.show_warning("Предупреждение", "Сначала загрузите изображение")
            return
        
        try:
            # Создаем окно сравнения
            compare_window = self.window_manager.create_comparison_window()
            
            # Создаем интерфейс выбора фильтров
            selection_frame = self.ui_factory.create_label_frame(
                compare_window, "Выберите фильтры для сравнения", padding="10"
            )
            selection_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Чекбоксы для выбора фильтров
            self.selected_filters = self.ui_factory.create_filter_checkboxes(
                selection_frame, AVAILABLE_FILTERS
            )
            
            # Кнопка запуска сравнения
            compare_btn = self.ui_factory.create_button(
                selection_frame, 
                "🔄 Сравнить выбранные фильтры", 
                lambda: self.run_filter_comparison(compare_window, original_image, update_info_callback)
            )
            compare_btn.grid(row=len(AVAILABLE_FILTERS)//2 + 1, column=0, columnspan=2, pady=10)
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось создать окно сравнения: {e}")
    
    def run_filter_comparison(self, window, original_image, update_info_callback):
        """Запускает сравнение выбранных фильтров."""
        try:
            # Получаем выбранные фильтры
            selected = [name for name, var in self.selected_filters.items() if var.get()]
            
            if not selected:
                self.window_manager.show_warning("Предупреждение", "Выберите хотя бы один фильтр")
                return
            
            # Инициализируем оценщик качества
            from image_processing.quality_assessment import FilterQualityComparator
            comparator = FilterQualityComparator()
            
            # Применяем выбранные фильтры
            import numpy as np
            from image_processing.factories.transform_factory import TransformFactory
            
            original_array = np.array(original_image)
            filter_results = {}
            
            for filter_name in selected:
                try:
                    transform = TransformFactory.create_transform(filter_name)
                    processed_array = transform.apply(original_array)
                    filter_results[filter_name] = processed_array
                except Exception as e:
                    self.window_manager.show_error("Ошибка", f"Не удалось применить фильтр {filter_name}: {e}")
                    return
            
            # Сравниваем фильтры
            comparison_results = comparator.compare_filters(original_array, filter_results)
            
            # Отображаем результаты
            self.display_comparison_results(window, comparison_results, comparator)
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось выполнить сравнение: {e}")
    
    def display_comparison_results(self, window, results, comparator):
        """Отображает результаты сравнения фильтров."""
        try:
            # Очищаем окно
            for widget in window.winfo_children():
                if isinstance(widget, ttk.LabelFrame):
                    widget.destroy()
            
            # Создаем область для результатов
            results_frame = self.ui_factory.create_label_frame(
                window, "Результаты сравнения", padding="10"
            )
            results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Отчет о сравнении
            report_text = comparator.format_comparison_report()
            
            # Создаем текстовое поле для отчета
            text_widget = tk.Text(
                results_frame.frame, 
                wrap=tk.WORD, 
                bg="#3c3c3c", 
                fg="#ffffff", 
                font=("Segoe UI", 9)
            )
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(1.0, report_text)
            text_widget.configure(state=tk.DISABLED)
            
            # Кнопка закрытия
            close_btn = self.ui_factory.create_button(
                results_frame.frame, "Закрыть", window.destroy
            )
            close_btn.pack(pady=10)
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось отобразить результаты: {e}")
    
    def compare_sharpness_filters(self, original_image, update_info_callback):
        """Сравнивает различные фильтры резкости."""
        if not original_image:
            self.window_manager.show_warning("Предупреждение", "Сначала загрузите изображение")
            return
        
        try:
            # Создаем окно сравнения фильтров резкости
            sharpness_window = self.window_manager.create_sharpness_window()
            
            # Создаем интерфейс выбора параметров
            selection_frame = self.ui_factory.create_label_frame(
                sharpness_window, "Параметры сравнения", padding="10"
            )
            selection_frame.pack(fill=tk.X, padx=10, pady=10)
            
            # Выбор размеров ядер
            ttk.Label(selection_frame.frame, text="Размеры ядер (k):", style='Modern.TLabel').pack(anchor=tk.W)
            kernel_frame = ttk.Frame(selection_frame.frame, style='Modern.TFrame')
            kernel_frame.pack(fill=tk.X, pady=(5, 10))
            
            self.kernel_vars = self.ui_factory.create_kernel_checkboxes(kernel_frame)
            
            # Выбор значений λ
            ttk.Label(selection_frame.frame, text="Значения λ:", style='Modern.TLabel').pack(anchor=tk.W)
            lambda_frame = ttk.Frame(selection_frame.frame, style='Modern.TFrame')
            lambda_frame.pack(fill=tk.X, pady=(5, 10))
            
            self.lambda_vars = self.ui_factory.create_lambda_checkboxes(lambda_frame)
            
            # Кнопка запуска сравнения
            compare_btn = self.ui_factory.create_button(
                selection_frame, 
                "🔍 Сравнить фильтры резкости", 
                lambda: self.run_sharpness_comparison(sharpness_window, original_image, update_info_callback)
            )
            compare_btn.pack(pady=10)
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось создать окно сравнения: {e}")
    
    def run_sharpness_comparison(self, window, original_image, update_info_callback):
        """Запускает сравнение фильтров резкости."""
        try:
            # Получаем выбранные параметры
            selected_kernels = [k for k, var in self.kernel_vars.items() if var.get()]
            selected_lambdas = [lambda_val for lambda_val, var in self.lambda_vars.items() if var.get()]
            
            if not selected_kernels or not selected_lambdas:
                self.window_manager.show_warning(
                    "Предупреждение", 
                    "Выберите хотя бы один размер ядра и одно значение λ"
                )
                return
            
            # Инициализируем компаратор
            from image_processing.sharpness_comparator import SharpnessComparator
            comparator = SharpnessComparator()
            
            # Конвертируем изображение в numpy array
            import numpy as np
            original_array = np.array(original_image)
            
            # Выполняем сравнение
            results = comparator.compare_sharpness_filters(
                original_array, 
                kernel_sizes=selected_kernels, 
                lambda_values=selected_lambdas
            )
            
            # Отображаем результаты
            self.display_sharpness_comparison_results(window, results, comparator)
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось выполнить сравнение: {e}")
    
    def display_sharpness_comparison_results(self, window, results, comparator):
        """Отображает результаты сравнения фильтров резкости."""
        try:
            # Очищаем окно
            for widget in window.winfo_children():
                if isinstance(widget, ttk.LabelFrame):
                    widget.destroy()
            
            # Создаем область для результатов
            results_frame = self.ui_factory.create_label_frame(
                window, "Результаты сравнения фильтров резкости", padding="10"
            )
            results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Отчет о сравнении
            report_text = comparator.format_comparison_report()
            
            # Добавляем рекомендации
            recommendations = comparator.get_filter_recommendations()
            report_text += "\n\n" + "\n".join(recommendations)
            
            # Создаем текстовое поле для отчета
            text_widget = tk.Text(
                results_frame.frame, 
                wrap=tk.WORD, 
                bg="#3c3c3c", 
                fg="#ffffff", 
                font=("Segoe UI", 9)
            )
            text_widget.pack(fill=tk.BOTH, expand=True)
            text_widget.insert(1.0, report_text)
            text_widget.configure(state=tk.DISABLED)
            
            # Кнопка закрытия
            close_btn = self.ui_factory.create_button(
                results_frame.frame, "Закрыть", window.destroy
            )
            close_btn.pack(pady=10)
            
        except Exception as e:
            self.window_manager.show_error("Ошибка", f"Не удалось отобразить результаты: {e}")
