"""
Контейнер зависимостей для инверсии управления.
"""

from typing import Dict, Any, Type, TypeVar, Callable, Optional
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class DIContainer:
    """Контейнер зависимостей."""
    
    def __init__(self):
        """Инициализация контейнера."""
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register_singleton(self, interface: Type[T], implementation: Type[T]) -> None:
        """
        Регистрирует синглтон.
        
        Args:
            interface: Интерфейс
            implementation: Реализация
        """
        interface_name = interface.__name__
        self._services[interface_name] = implementation
        logger.info(f"Зарегистрирован синглтон: {interface_name}")
    
    def register_factory(self, interface: Type[T], factory: Callable[[], T]) -> None:
        """
        Регистрирует фабрику.
        
        Args:
            interface: Интерфейс
            factory: Фабрика для создания экземпляра
        """
        interface_name = interface.__name__
        self._factories[interface_name] = factory
        logger.info(f"Зарегистрирована фабрика: {interface_name}")
    
    def register_instance(self, interface: Type[T], instance: T) -> None:
        """
        Регистрирует экземпляр.
        
        Args:
            interface: Интерфейс
            instance: Экземпляр
        """
        interface_name = interface.__name__
        self._singletons[interface_name] = instance
        logger.info(f"Зарегистрирован экземпляр: {interface_name}")
    
    def get(self, interface: Type[T]) -> T:
        """
        Получает экземпляр по интерфейсу.
        
        Args:
            interface: Интерфейс
            
        Returns:
            T: Экземпляр реализации
            
        Raises:
            ValueError: Если сервис не зарегистрирован
        """
        interface_name = interface.__name__
        
        # Проверяем синглтоны
        if interface_name in self._singletons:
            return self._singletons[interface_name]
        
        # Проверяем фабрики
        if interface_name in self._factories:
            instance = self._factories[interface_name]()
            self._singletons[interface_name] = instance  # Кэшируем как синглтон
            return instance
        
        # Проверяем сервисы
        if interface_name in self._services:
            implementation = self._services[interface_name]
            instance = implementation()
            self._singletons[interface_name] = instance  # Кэшируем как синглтон
            return instance
        
        raise ValueError(f"Сервис {interface_name} не зарегистрирован")
    
    def is_registered(self, interface: Type[T]) -> bool:
        """
        Проверяет, зарегистрирован ли сервис.
        
        Args:
            interface: Интерфейс
            
        Returns:
            bool: True если сервис зарегистрирован
        """
        interface_name = interface.__name__
        return (interface_name in self._services or 
                interface_name in self._factories or 
                interface_name in self._singletons)
