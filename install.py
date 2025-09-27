#!/usr/bin/env python3
"""
Скрипт для установки зависимостей приложения.
"""

import subprocess
import sys
import os

def install_requirements():
    """Устанавливает зависимости из requirements.txt."""
    try:
        print("Установка зависимостей...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Зависимости успешно установлены!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при установке зависимостей: {e}")
        return False

def create_directories():
    """Создает необходимые директории."""
    directories = ["logs", "test_images"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Создана директория: {directory}")

if __name__ == "__main__":
    print("Настройка приложения обработки изображений...")
    
    # Создаем директории
    create_directories()
    
    # Устанавливаем зависимости
    if install_requirements():
        print("\n🎉 Приложение готово к использованию!")
        print("Для запуска выполните: python main.py")
    else:
        print("\n❌ Ошибка при настройке приложения")
        sys.exit(1)
