"""
Финальная рефакторированная версия Photo Editor Pro.
Полностью модульная архитектура с устранением дублирования.
"""

import tkinter as tk
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импортируем финальную рефакторированную версию
from gui.final_main_window import FinalMainWindow


class ModernPhotoEditor:
    """Современный фоторедактор с полностью рефакторированной архитектурой."""
    
    def __init__(self, root):
        """Инициализация редактора."""
        self.root = root
        self.app = FinalMainWindow(root)


def main():
    """Главная функция запуска приложения."""
    try:
        print("🚀 Запуск Photo Editor Pro (финальная рефакторированная версия)...")
        print("✨ Полностью модульная архитектура:")
        print("   📁 constants.py - все константы и магические числа")
        print("   🎨 base_components.py - базовые классы UI компонентов")
        print("   🏭 ui_factory.py - фабрика для создания компонентов")
        print("   🎛️ style_manager.py - менеджер стилей")
        print("   🖼️ image_manager.py - менеджер изображений")
        print("   🎯 parameter_manager.py - менеджер параметров")
        print("   📊 quality_manager.py - менеджер качества")
        print("   🎪 event_manager.py - менеджер событий")
        print("   🪟 window_manager.py - менеджер окон")
        print("   🔧 Полностью устранено дублирование кода")
        print()
        
        # Создание главного окна
        root = tk.Tk()
        
        # Создание приложения с полностью рефакторированной архитектурой
        app = ModernPhotoEditor(root)
        
        print("✅ Photo Editor Pro (финальная версия) запущен успешно!")
        print("📝 Инструкции:")
        print("   1. Нажмите '📁 Загрузить' для выбора изображения")
        print("   2. Выберите тип преобразования в правой панели")
        print("   3. Настройте параметры и нажмите кнопку применения")
        print("   4. Сохраните результат с помощью '💾 Сохранить'")
        print("   5. Используйте '🔄 Сброс' для возврата к исходному")
        print("   6. Используйте панель качества для анализа результатов")
        print()
        print("🏗️ Архитектурные улучшения:")
        print("   ✅ Все магические числа вынесены в константы")
        print("   ✅ Код разбит на модули по ответственности")
        print("   ✅ Созданы базовые классы для UI компонентов")
        print("   ✅ Устранено дублирование через фабрики")
        print("   ✅ Общие компоненты переиспользуются")
        print("   ✅ Менеджеры инкапсулируют логику")
        print("   ✅ События обрабатываются централизованно")
        print()
        
        # Запуск главного цикла
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
