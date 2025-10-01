"""
Рефакторированная версия Photo Editor Pro.
Использует модульную архитектуру и устраняет дублирование кода.
"""

import tkinter as tk
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем рефакторированное главное окно
from gui.refactored_main_window import RefactoredMainWindow


class ModernPhotoEditor:
    """Современный фоторедактор с рефакторированной архитектурой."""
    
    def __init__(self, root):
        """Инициализация редактора."""
        self.root = root
        self.app = RefactoredMainWindow(root)


def main():
    """Главная функция запуска приложения."""
    try:
        print("🚀 Запуск Photo Editor Pro (рефакторированная версия)...")
        print("✨ Модульная архитектура:")
        print("   📁 Константы вынесены в отдельный файл")
        print("   🎨 Базовые классы для UI компонентов")
        print("   🏭 Фабрики для создания компонентов")
        print("   🎛️ Менеджеры для различных аспектов приложения")
        print("   🔧 Устранено дублирование кода")
        print()
        
        # Создание главного окна
        root = tk.Tk()
        
        # Создание приложения с рефакторированной архитектурой
        app = ModernPhotoEditor(root)
        
        print("✅ Photo Editor Pro (рефакторированная версия) запущен успешно!")
        print("📝 Инструкции:")
        print("   1. Нажмите '📁 Загрузить' для выбора изображения")
        print("   2. Выберите тип преобразования в правой панели")
        print("   3. Настройте параметры и нажмите кнопку применения")
        print("   4. Сохраните результат с помощью '💾 Сохранить'")
        print("   5. Используйте '🔄 Сброс' для возврата к исходному")
        print("   6. Используйте панель качества для анализа результатов")
        print()
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
