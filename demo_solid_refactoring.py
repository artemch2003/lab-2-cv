"""
Демонстрация рефакторинга по принципам SOLID.
Показывает, как легко добавить новое преобразование.
"""

import sys
import os
import tkinter as tk

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_processing.transforms.negative_transform import NegativeTransform
from image_processing.factories.transform_factory import TransformFactory
from di.config import create_container
from gui.main_window_refactored import MainWindow


def demonstrate_solid_principles():
    """Демонстрирует принципы SOLID."""
    print("🚀 Демонстрация рефакторинга по принципам SOLID")
    print("=" * 60)
    
    # 1. Single Responsibility Principle (SRP)
    print("\n1. Single Responsibility Principle (SRP):")
    print("   ✅ Каждый класс имеет одну ответственность:")
    print("   - ImageManager: управление изображениями")
    print("   - TransformManager: управление преобразованиями")
    print("   - TransformSettings: настройки UI")
    print("   - ImageDisplay: отображение изображений")
    print("   - InfoPanel: информационная панель")
    
    # 2. Open/Closed Principle (OCP)
    print("\n2. Open/Closed Principle (OCP):")
    print("   ✅ Система открыта для расширения, закрыта для модификации:")
    
    # Регистрируем новое преобразование
    TransformFactory.register_transform("Негативное", NegativeTransform)
    print("   ✅ Добавлено новое преобразование 'Негативное' без изменения существующего кода")
    
    # 3. Liskov Substitution Principle (LSP)
    print("\n3. Liskov Substitution Principle (LSP):")
    print("   ✅ Все преобразования взаимозаменяемы:")
    available_transforms = TransformFactory.get_available_transforms()
    print(f"   ✅ Доступные преобразования: {', '.join(available_transforms)}")
    
    # 4. Interface Segregation Principle (ISP)
    print("\n4. Interface Segregation Principle (ISP):")
    print("   ✅ Интерфейсы разделены по функциональности:")
    print("   - ImageLoaderInterface: загрузка изображений")
    print("   - ImageSaverInterface: сохранение изображений")
    print("   - ImageDisplayInterface: отображение изображений")
    print("   - TransformApplierInterface: применение преобразований")
    
    # 5. Dependency Inversion Principle (DIP)
    print("\n5. Dependency Inversion Principle (DIP):")
    print("   ✅ Зависимости инвертированы через контейнер DI:")
    container = create_container()
    print("   ✅ Контейнер зависимостей настроен")
    print("   ✅ Контроллер получает зависимости через инжекцию")
    
    print("\n🎉 Все принципы SOLID успешно реализованы!")
    print("=" * 60)


def run_application():
    """Запускает приложение с демонстрацией SOLID принципов."""
    print("Запуск приложения с рефакторингом по SOLID...")
    
    # Создаем контейнер зависимостей
    container = create_container()
    
    # Создаем главное окно
    root = tk.Tk()
    app = MainWindow(root, container)
    
    # Запускаем приложение
    root.mainloop()


if __name__ == "__main__":
    demonstrate_solid_principles()
    
    print("\n" + "=" * 60)
    print("Запуск приложения...")
    print("=" * 60)
    
    run_application()
