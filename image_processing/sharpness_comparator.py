"""
Модуль для сравнения фильтров резкости с различными параметрами.
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from .transforms.sharpness_filters import UnsharpMasking
from .quality_assessment import QualityAssessment
import logging

logger = logging.getLogger(__name__)


class SharpnessComparator:
    """Класс для сравнения различных фильтров резкости."""
    
    def __init__(self):
        """Инициализация компаратора."""
        self.quality_assessor = QualityAssessment()
        self.comparison_results = {}
    
    def compare_sharpness_filters(self, original_image: np.ndarray, 
                                 kernel_sizes: List[int] = [3, 5, 7], 
                                 lambda_values: List[float] = [0.5, 1.0, 1.5, 2.0]) -> Dict[str, Any]:
        """
        Сравнивает фильтры резкости с различными параметрами.
        
        Args:
            original_image: Исходное изображение
            kernel_sizes: Список размеров ядер для сравнения
            lambda_values: Список значений λ для сравнения
            
        Returns:
            Dict[str, Any]: Результаты сравнения
        """
        logger.info(f"Начинаем сравнение фильтров резкости для {len(kernel_sizes)} размеров ядра и {len(lambda_values)} значений λ")
        
        results = {
            'original_image': original_image,
            'filter_results': {},
            'quality_metrics': {},
            'best_filters': {},
            'comparison_summary': {}
        }
        
        # Применяем все комбинации фильтров
        for k in kernel_sizes:
            for lambda_coeff in lambda_values:
                filter_name = f"k={k}, λ={lambda_coeff:.1f}"
                
                try:
                    # Создаем фильтр
                    filter_instance = UnsharpMasking(kernel_size=k, lambda_coeff=lambda_coeff)
                    
                    # Применяем фильтр
                    sharpened_image = filter_instance.apply(original_image)
                    
                    # Вычисляем метрики качества
                    quality_metrics = self.quality_assessor.compute_quality_metrics(
                        original_image, sharpened_image
                    )
                    
                    # Сохраняем результаты
                    results['filter_results'][filter_name] = sharpened_image
                    results['quality_metrics'][filter_name] = quality_metrics
                    
                    logger.info(f"Обработан фильтр {filter_name}: качество = {quality_metrics['quality_rating']}")
                    
                except Exception as e:
                    logger.error(f"Ошибка при применении фильтра {filter_name}: {e}")
                    continue
        
        # Находим лучшие фильтры по различным критериям
        results['best_filters'] = self._find_best_filters(results['quality_metrics'])
        
        # Создаем сводку сравнения
        results['comparison_summary'] = self._create_comparison_summary(results)
        
        self.comparison_results = results
        return results
    
    def _find_best_filters(self, quality_metrics: Dict[str, Dict[str, Any]]) -> Dict[str, str]:
        """
        Находит лучшие фильтры по различным критериям.
        
        Args:
            quality_metrics: Метрики качества для всех фильтров
            
        Returns:
            Dict[str, str]: Лучшие фильтры по критериям
        """
        best_filters = {}
        
        if not quality_metrics:
            return best_filters
        
        # Лучший по общему качеству
        best_quality = max(quality_metrics.items(), 
                          key=lambda x: x[1]['quality_rating'])
        best_filters['best_overall'] = best_quality[0]
        
        # Лучший по минимальной разности
        best_difference = min(quality_metrics.items(), 
                             key=lambda x: x[1]['mean_difference'])
        best_filters['best_difference'] = best_difference[0]
        
        # Лучший по максимальному PSNR
        best_psnr = max(quality_metrics.items(), 
                       key=lambda x: x[1].get('psnr', 0))
        best_filters['best_psnr'] = best_psnr[0]
        
        return best_filters
    
    def _create_comparison_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создает сводку сравнения.
        
        Args:
            results: Результаты сравнения
            
        Returns:
            Dict[str, Any]: Сводка сравнения
        """
        summary = {
            'total_filters_tested': len(results['quality_metrics']),
            'kernel_sizes_tested': list(set([k.split(',')[0].split('=')[1] for k in results['quality_metrics'].keys()])),
            'lambda_values_tested': list(set([k.split('λ=')[1] for k in results['quality_metrics'].keys()])),
            'average_quality': np.mean([m['quality_rating'] for m in results['quality_metrics'].values()]),
            'quality_range': {
                'min': min([m['quality_rating'] for m in results['quality_metrics'].values()]),
                'max': max([m['quality_rating'] for m in results['quality_metrics'].values()])
            }
        }
        
        return summary
    
    def format_comparison_report(self) -> str:
        """
        Форматирует отчет о сравнении фильтров резкости.
        
        Returns:
            str: Отформатированный отчет
        """
        if not self.comparison_results:
            return "Сравнение не выполнено"
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("ОТЧЕТ О СРАВНЕНИИ ФИЛЬТРОВ РЕЗКОСТИ")
        report_lines.append("=" * 60)
        report_lines.append("")
        
        # Сводка
        summary = self.comparison_results['comparison_summary']
        report_lines.append("СВОДКА СРАВНЕНИЯ:")
        report_lines.append(f"  • Всего протестировано фильтров: {summary['total_filters_tested']}")
        report_lines.append(f"  • Размеры ядер: {', '.join(summary['kernel_sizes_tested'])}")
        report_lines.append(f"  • Значения λ: {', '.join(summary['lambda_values_tested'])}")
        report_lines.append(f"  • Среднее качество: {summary['average_quality']:.2f}")
        report_lines.append(f"  • Диапазон качества: {summary['quality_range']['min']:.2f} - {summary['quality_range']['max']:.2f}")
        report_lines.append("")
        
        # Лучшие фильтры
        best_filters = self.comparison_results['best_filters']
        report_lines.append("ЛУЧШИЕ ФИЛЬТРЫ:")
        report_lines.append(f"  • Лучший общий: {best_filters.get('best_overall', 'Не определен')}")
        report_lines.append(f"  • Лучший по разности: {best_filters.get('best_difference', 'Не определен')}")
        report_lines.append(f"  • Лучший по PSNR: {best_filters.get('best_psnr', 'Не определен')}")
        report_lines.append("")
        
        # Детальные результаты
        report_lines.append("ДЕТАЛЬНЫЕ РЕЗУЛЬТАТЫ:")
        report_lines.append("-" * 60)
        
        quality_metrics = self.comparison_results['quality_metrics']
        for filter_name, metrics in sorted(quality_metrics.items(), 
                                         key=lambda x: x[1]['quality_rating'], 
                                         reverse=True):
            report_lines.append(f"Фильтр: {filter_name}")
            report_lines.append(f"  • Качество: {metrics['quality_rating']:.2f}")
            report_lines.append(f"  • Средняя разность: {metrics['mean_difference']:.2f}")
            report_lines.append(f"  • Максимальная разность: {metrics['max_difference']}")
            if 'psnr' in metrics:
                report_lines.append(f"  • PSNR: {metrics['psnr']:.2f} дБ")
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def get_filter_recommendations(self) -> List[str]:
        """
        Возвращает рекомендации по выбору фильтров.
        
        Returns:
            List[str]: Список рекомендаций
        """
        if not self.comparison_results:
            return ["Сравнение не выполнено"]
        
        recommendations = []
        summary = self.comparison_results['comparison_summary']
        best_filters = self.comparison_results['best_filters']
        
        recommendations.append("РЕКОМЕНДАЦИИ ПО ВЫБОРУ ФИЛЬТРОВ РЕЗКОСТИ:")
        recommendations.append("")
        
        # Рекомендации по размеру ядра
        recommendations.append("1. РАЗМЕР ЯДРА (k):")
        recommendations.append("   • k=3: Для тонких деталей и мягкого повышения резкости")
        recommendations.append("   • k=5: Для среднего уровня детализации")
        recommendations.append("   • k=7: Для сильного повышения резкости крупных объектов")
        recommendations.append("")
        
        # Рекомендации по коэффициенту λ
        recommendations.append("2. КОЭФФИЦИЕНТ λ:")
        recommendations.append("   • λ=0.5: Мягкое повышение резкости, подходит для портретов")
        recommendations.append("   • λ=1.0: Стандартное повышение резкости")
        recommendations.append("   • λ=1.5: Сильное повышение резкости для пейзажей")
        recommendations.append("   • λ=2.0: Очень сильное повышение резкости, может создать артефакты")
        recommendations.append("")
        
        # Лучшие комбинации
        if best_filters:
            recommendations.append("3. ЛУЧШИЕ КОМБИНАЦИИ ПО РЕЗУЛЬТАТАМ ТЕСТИРОВАНИЯ:")
            for criterion, filter_name in best_filters.items():
                criterion_name = {
                    'best_overall': 'Общее качество',
                    'best_difference': 'Минимальная разность',
                    'best_psnr': 'Максимальный PSNR'
                }.get(criterion, criterion)
                recommendations.append(f"   • {criterion_name}: {filter_name}")
        
        return recommendations
