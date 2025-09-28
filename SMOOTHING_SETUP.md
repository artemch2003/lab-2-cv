# Настройка и запуск фильтров сглаживания

## Быстрый старт

### 1. Простой тест фильтров
```bash
python3 simple_test.py
```

### 2. Простое приложение с интерфейсом
```bash
python3 run_simple_smoothing.py
```

### 3. Полное приложение с вкладками
```bash
python3 run_smoothing_app.py
```

## Что реализовано

### ✅ Фильтры сглаживания
- **Прямоугольный фильтр 3x3** - усреднение по окну 3x3
- **Прямоугольный фильтр 5x5** - усреднение по окну 5x5  
- **Медианный фильтр 3x3** - медиана по окну 3x3
- **Медианный фильтр 5x5** - медиана по окну 5x5

### ✅ Особенности
- Алгоритмы разработаны самостоятельно (без OpenCV/scipy)
- Поддержка цветных и оттенков серого изображений
- Корректная обработка границ с padding
- Интеграция с существующей архитектурой
- Отдельная вкладка в UI

### ✅ Файлы
- `image_processing/transforms/smoothing_filters.py` - реализация фильтров
- `gui/components/modern_smoothing_settings.py` - UI компонент
- `gui/modern_main_window_with_tabs.py` - главное окно с вкладками
- `run_smoothing_app.py` - полное приложение
- `run_simple_smoothing.py` - простое приложение
- `simple_test.py` - тесты фильтров

## Использование

### Программное использование
```python
from image_processing.transforms.smoothing_filters import RectangularFilter3x3

# Создание фильтра
filter_3x3 = RectangularFilter3x3()

# Применение к изображению
result = filter_3x3.apply(image_array)
```

### Графический интерфейс
1. Запустите `run_simple_smoothing.py` для простого интерфейса
2. Выберите тип фильтра из выпадающего списка
3. Нажмите "Тестировать фильтр" для проверки работы
4. Для полного функционала используйте `run_smoothing_app.py`

## Тестирование

```bash
# Простой тест
python3 simple_test.py

# Тест с созданием изображений
python3 test_smoothing_filters.py
```

## Структура проекта

```
image_processing/transforms/
├── smoothing_filters.py          # Реализация фильтров
└── base_transform.py            # Базовый класс

gui/
├── components/
│   └── modern_smoothing_settings.py  # UI компонент
├── modern_main_window_with_tabs.py    # Главное окно
└── controllers/
    └── main_controller.py            # Контроллер

# Запускаемые файлы
├── run_smoothing_app.py         # Полное приложение
├── run_simple_smoothing.py      # Простое приложение  
└── simple_test.py               # Тесты
```

## Решение проблем

### Ошибка импорта
Если возникают ошибки импорта, убедитесь что:
1. Вы находитесь в корневой директории проекта
2. Все файлы на месте
3. Python может найти модули

### Ошибка запуска GUI
Если GUI не запускается:
1. Проверьте, что tkinter установлен
2. Используйте `run_simple_smoothing.py` для диагностики
3. Проверьте логи в консоли

### Тестирование фильтров
```bash
# Проверка импортов
python3 -c "from image_processing.transforms.smoothing_filters import RectangularFilter3x3; print('OK')"

# Полный тест
python3 simple_test.py
```

## Готово! 🎉

Все фильтры сглаживания реализованы и готовы к использованию:
- ✅ Прямоугольные фильтры 3x3 и 5x5
- ✅ Медианные фильтры 3x3 и 5x5  
- ✅ Алгоритмы разработаны самостоятельно
- ✅ Отдельная вкладка в UI
- ✅ Полная интеграция с системой
