"""
Модуль для оценки качества обработки изображений.
"""

import numpy as np
from typing import Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class QualityAssessment:
    """Класс для оценки качества обработки изображений."""
    
    def __init__(self):
        """Инициализация оценщика качества."""
        pass
    
    def compute_absolute_difference_map(self, original: np.ndarray, processed: np.ndarray) -> np.ndarray:
        """
        Вычисляет карту абсолютной разности между исходным и обработанным изображениями.
        
        Args:
            original: Исходное изображение
            processed: Обработанное изображение
            
        Returns:
            np.ndarray: Карта абсолютной разности
        """
        try:
            # Проверяем, что изображения имеют одинаковые размеры
            if original.shape != processed.shape:
                raise ValueError("Изображения должны иметь одинаковые размеры")
            
            # Вычисляем абсолютную разность
            if len(original.shape) == 3:
                # Цветное изображение - вычисляем разность для каждого канала
                diff_map = np.zeros_like(original, dtype=np.float64)
                for channel in range(original.shape[2]):
                    diff_map[:, :, channel] = np.abs(original[:, :, channel].astype(np.float64) - 
                                                    processed[:, :, channel].astype(np.float64))
            else:
                # Оттенки серого
                diff_map = np.abs(original.astype(np.float64) - processed.astype(np.float64))
            
            return diff_map.astype(np.uint8)
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении карты разности: {e}")
            raise
    
    def compute_quality_metrics(self, original: np.ndarray, processed: np.ndarray) -> Dict[str, Any]:
        """
        Вычисляет метрики качества обработки.
        
        Args:
            original: Исходное изображение
            processed: Обработанное изображение
            
        Returns:
            Dict[str, Any]: Словарь с метриками качества
        """
        try:
            # Вычисляем карту разности
            diff_map = self.compute_absolute_difference_map(original, processed)
            
            # Базовые метрики
            metrics = {
                'mean_difference': float(np.mean(diff_map)),
                'max_difference': int(np.max(diff_map)),
                'std_difference': float(np.std(diff_map)),
                'total_pixels': int(diff_map.size),
                'high_difference_pixels': int(np.sum(diff_map > 50)),  # Пиксели с большой разностью
                'medium_difference_pixels': int(np.sum((diff_map > 20) & (diff_map <= 50))),
                'low_difference_pixels': int(np.sum(diff_map <= 20))
            }
            
            # Процентные метрики
            total_pixels = metrics['total_pixels']
            metrics['high_difference_percent'] = (metrics['high_difference_pixels'] / total_pixels) * 100
            metrics['medium_difference_percent'] = (metrics['medium_difference_pixels'] / total_pixels) * 100
            metrics['low_difference_percent'] = (metrics['low_difference_pixels'] / total_pixels) * 100
            
            # Оценка качества (чем меньше разность, тем лучше)
            # Числовая оценка для математических операций (0-100)
            if metrics['mean_difference'] < 10:
                metrics['quality_rating'] = 90.0  # Отличное
                metrics['quality_label'] = "Отличное"
            elif metrics['mean_difference'] < 25:
                metrics['quality_rating'] = 75.0  # Хорошее
                metrics['quality_label'] = "Хорошее"
            elif metrics['mean_difference'] < 50:
                metrics['quality_rating'] = 60.0  # Удовлетворительное
                metrics['quality_label'] = "Удовлетворительное"
            else:
                metrics['quality_rating'] = 30.0  # Плохое
                metrics['quality_label'] = "Плохое"
            
            return metrics
            
        except Exception as e:
            logger.error(f"Ошибка при вычислении метрик качества: {e}")
            raise
    
    def create_visualization_map(self, diff_map: np.ndarray, colormap: str = 'hot') -> np.ndarray:
        """
        Создает визуализацию карты разности с цветовой схемой.
        
        Args:
            diff_map: Карта абсолютной разности
            colormap: Цветовая схема ('hot', 'cool', 'gray')
            
        Returns:
            np.ndarray: Визуализированная карта
        """
        try:
            # Нормализуем карту к диапазону 0-255
            if np.max(diff_map) > 0:
                normalized_map = (diff_map.astype(np.float64) / np.max(diff_map) * 255).astype(np.uint8)
            else:
                normalized_map = diff_map.copy()
            
            if colormap == 'hot':
                # Горячая цветовая схема (черный -> красный -> желтый -> белый)
                return self._apply_hot_colormap(normalized_map)
            elif colormap == 'cool':
                # Холодная цветовая схема (черный -> синий -> голубой -> белый)
                return self._apply_cool_colormap(normalized_map)
            else:
                # Серая схема
                return np.stack([normalized_map] * 3, axis=-1) if len(normalized_map.shape) == 2 else normalized_map
                
        except Exception as e:
            logger.error(f"Ошибка при создании визуализации: {e}")
            raise
    
    def _apply_hot_colormap(self, normalized_map: np.ndarray) -> np.ndarray:
        """Применяет горячую цветовую схему."""
        if len(normalized_map.shape) == 2:
            # Оттенки серого -> RGB
            result = np.zeros((*normalized_map.shape, 3), dtype=np.uint8)
            
            # Красный канал
            result[:, :, 0] = np.clip(normalized_map * 3, 0, 255)
            # Зеленый канал  
            result[:, :, 1] = np.clip((normalized_map - 85) * 3, 0, 255)
            # Синий канал
            result[:, :, 2] = np.clip((normalized_map - 170) * 3, 0, 255)
            
            return result
        else:
            return normalized_map
    
    def _apply_cool_colormap(self, normalized_map: np.ndarray) -> np.ndarray:
        """Применяет холодную цветовую схему."""
        if len(normalized_map.shape) == 2:
            # Оттенки серого -> RGB
            result = np.zeros((*normalized_map.shape, 3), dtype=np.uint8)
            
            # Синий канал
            result[:, :, 2] = np.clip(normalized_map * 3, 0, 255)
            # Зеленый канал
            result[:, :, 1] = np.clip((normalized_map - 85) * 3, 0, 255)
            # Красный канал
            result[:, :, 0] = np.clip((normalized_map - 170) * 3, 0, 255)
            
            return result
        else:
            return normalized_map
    
    def format_quality_report(self, metrics: Dict[str, Any]) -> str:
        """
        Форматирует отчет о качестве обработки.
        
        Args:
            metrics: Метрики качества
            
        Returns:
            str: Отформатированный отчет
        """
        report = []
        report.append("=== ОЦЕНКА КАЧЕСТВА ОБРАБОТКИ ===")
        report.append(f"Общая оценка: {metrics.get('quality_label', metrics['quality_rating'])}")
        report.append("")
        report.append("Статистика разности:")
        report.append(f"  Средняя разность: {metrics['mean_difference']:.2f}")
        report.append(f"  Максимальная разность: {metrics['max_difference']}")
        report.append(f"  Стандартное отклонение: {metrics['std_difference']:.2f}")
        report.append("")
        report.append("Распределение разности:")
        report.append(f"  Низкая разность (≤20): {metrics['low_difference_percent']:.1f}%")
        report.append(f"  Средняя разность (21-50): {metrics['medium_difference_percent']:.1f}%")
        report.append(f"  Высокая разность (>50): {metrics['high_difference_percent']:.1f}%")
        
        return "\n".join(report)


class FilterQualityComparator:
    """Класс для сравнения качества различных фильтров."""
    
    def __init__(self):
        """Инициализация компаратора."""
        self.quality_assessor = QualityAssessment()
        self.comparison_results = {}
    
    def compare_filters(self, original: np.ndarray, filter_results: Dict[str, np.ndarray]) -> Dict[str, Dict[str, Any]]:
        """
        Сравнивает качество различных фильтров.
        
        Args:
            original: Исходное изображение
            filter_results: Словарь {название_фильтра: обработанное_изображение}
            
        Returns:
            Dict[str, Dict[str, Any]]: Результаты сравнения для каждого фильтра
        """
        comparison = {}
        
        for filter_name, processed_image in filter_results.items():
            try:
                metrics = self.quality_assessor.compute_quality_metrics(original, processed_image)
                diff_map = self.quality_assessor.compute_absolute_difference_map(original, processed_image)
                
                comparison[filter_name] = {
                    'metrics': metrics,
                    'difference_map': diff_map,
                    'visualization': self.quality_assessor.create_visualization_map(diff_map)
                }
                
            except Exception as e:
                logger.error(f"Ошибка при сравнении фильтра {filter_name}: {e}")
                comparison[filter_name] = {'error': str(e)}
        
        self.comparison_results = comparison
        return comparison
    
    def get_best_filter(self) -> str:
        """
        Возвращает название лучшего фильтра по средней разности.
        
        Returns:
            str: Название лучшего фильтра
        """
        if not self.comparison_results:
            return "Нет данных для сравнения"
        
        best_filter = None
        best_score = float('inf')
        
        for filter_name, result in self.comparison_results.items():
            if 'metrics' in result:
                mean_diff = result['metrics']['mean_difference']
                if mean_diff < best_score:
                    best_score = mean_diff
                    best_filter = filter_name
        
        return best_filter if best_filter else "Не удалось определить"
    
    def format_comparison_report(self) -> str:
        """
        Форматирует отчет о сравнении фильтров.
        
        Returns:
            str: Отформатированный отчет
        """
        if not self.comparison_results:
            return "Нет данных для сравнения"
        
        report = []
        report.append("=== СРАВНЕНИЕ КАЧЕСТВА ФИЛЬТРОВ ===")
        report.append("")
        
        # Сортируем фильтры по качеству
        sorted_filters = sorted(
            [(name, result) for name, result in self.comparison_results.items() if 'metrics' in result],
            key=lambda x: x[1]['metrics']['mean_difference']
        )
        
        for i, (filter_name, result) in enumerate(sorted_filters, 1):
            metrics = result['metrics']
            report.append(f"{i}. {filter_name}")
            report.append(f"   Оценка: {metrics['quality_rating']}")
            report.append(f"   Средняя разность: {metrics['mean_difference']:.2f}")
            report.append("")
        
        best_filter = self.get_best_filter()
        report.append(f"Лучший фильтр: {best_filter}")
        
        return "\n".join(report)
