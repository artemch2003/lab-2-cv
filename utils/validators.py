"""
Модуль для валидации параметров.
"""

from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ParameterValidator:
    """Класс для валидации параметров преобразований."""
    
    @staticmethod
    def validate_float(value: Any, min_val: Optional[float] = None, max_val: Optional[float] = None, 
                      name: str = "параметр") -> float:
        """
        Валидирует и конвертирует значение в float.
        
        Args:
            value: Значение для валидации
            min_val: Минимальное допустимое значение
            max_val: Максимальное допустимое значение
            name: Название параметра для сообщений об ошибках
            
        Returns:
            float: Валидное значение
            
        Raises:
            ValueError: Если значение невалидно
        """
        try:
            float_value = float(value)
            
            if min_val is not None and float_value < min_val:
                raise ValueError(f"{name} должен быть не менее {min_val}")
            if max_val is not None and float_value > max_val:
                raise ValueError(f"{name} должен быть не более {max_val}")
                
            return float_value
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Неверное значение {name}: {e}")
    
    @staticmethod
    def validate_positive_float(value: Any, name: str = "параметр") -> float:
        """
        Валидирует положительное float значение.
        
        Args:
            value: Значение для валидации
            name: Название параметра для сообщений об ошибках
            
        Returns:
            float: Валидное положительное значение
            
        Raises:
            ValueError: Если значение невалидно
        """
        return ParameterValidator.validate_float(value, min_val=0, name=name)
    
    @staticmethod
    def validate_threshold(value: Any) -> float:
        """
        Валидирует пороговое значение (0-255).
        
        Args:
            value: Значение для валидации
            
        Returns:
            float: Валидное пороговое значение
            
        Raises:
            ValueError: Если значение невалидно
        """
        return ParameterValidator.validate_float(value, min_val=0, max_val=255, name="порог")
    
    @staticmethod
    def validate_brightness_range(min_brightness: Any, max_brightness: Any) -> tuple[float, float]:
        """
        Валидирует диапазон яркости.
        
        Args:
            min_brightness: Минимальная яркость
            max_brightness: Максимальная яркость
            
        Returns:
            tuple[float, float]: Валидные значения минимальной и максимальной яркости
            
        Raises:
            ValueError: Если значения невалидны
        """
        min_val = ParameterValidator.validate_float(min_brightness, min_val=0, max_val=255, name="минимальная яркость")
        max_val = ParameterValidator.validate_float(max_brightness, min_val=0, max_val=255, name="максимальная яркость")
        
        if min_val >= max_val:
            raise ValueError("Минимальная яркость должна быть меньше максимальной")
            
        return min_val, max_val
    
    @staticmethod
    def validate_mode(mode: Any, valid_modes: list[str], name: str = "режим") -> str:
        """
        Валидирует режим из списка допустимых значений.
        
        Args:
            mode: Режим для валидации
            valid_modes: Список допустимых режимов
            name: Название параметра для сообщений об ошибках
            
        Returns:
            str: Валидный режим
            
        Raises:
            ValueError: Если режим невалиден
        """
        if mode not in valid_modes:
            raise ValueError(f"Неверный {name}. Допустимые значения: {', '.join(valid_modes)}")
        return mode
