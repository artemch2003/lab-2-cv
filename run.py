#!/usr/bin/env python3
"""
Скрипт для запуска приложения обработки изображений.
Проверяет зависимости и запускает графическое приложение.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Проверяет наличие необходимых зависимостей."""
    required_packages = ['PIL', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Отсутствуют необходимые пакеты: {', '.join(missing_packages)}")
        print("📦 Установите зависимости: python install.py")
        return False
    
    return True

def main():
    """Главная функция запуска приложения."""
    print("🚀 Запуск приложения обработки изображений")
    print("=" * 50)
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ Все зависимости установлены")
    
    # Запускаем основное приложение
    try:
        print("🖼️  Запуск графического интерфейса...")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Приложение закрыто пользователем")
    except Exception as e:
        print(f"❌ Ошибка при запуске приложения: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
