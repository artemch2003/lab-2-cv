# Исправление trace() для Python 3.13

## Проблема
В Python 3.13 изменился синтаксис для `trace()`:
```
❌ Ошибка: bad option "variable": must be add, info, or remove
```

## Причина
Старый синтаксис `trace('w', callback)` больше не поддерживается в Python 3.13.
Нужно использовать новый синтаксис `trace_add('write', callback)`.

## Решение

### ✅ Исправлены все файлы:

1. **`gui/components/color_transform_settings.py`**
   ```python
   # Было:
   self.transform_type_var.trace('w', self._on_transform_type_change)
   
   # Стало:
   self.transform_type_var.trace_add('write', self._on_transform_type_change)
   ```

2. **`gui/components/smoothing_settings.py`**
   ```python
   # Было:
   self.filter_type_var.trace('w', self._on_filter_type_change)
   
   # Стало:
   self.filter_type_var.trace_add('write', self._on_filter_type_change)
   ```

3. **`gui/components/sharpness_settings.py`**
   ```python
   # Было:
   self.filter_type_var.trace('w', self._on_filter_type_change)
   
   # Стало:
   self.filter_type_var.trace_add('write', self._on_filter_type_change)
   ```

4. **`gui/components/transform_settings.py`**
   ```python
   # Было:
   self.transform_type_var.trace('w', self._on_transform_type_change)
   
   # Стало:
   self.transform_type_var.trace_add('write', self._on_transform_type_change)
   ```

5. **`gui/components/modern_transform_settings.py`**
   ```python
   # Было:
   self.transform_type_var.trace('w', self._on_transform_type_change)
   
   # Стало:
   self.transform_type_var.trace_add('write', self._on_transform_type_change)
   ```

6. **`gui/components/modern_smoothing_settings.py`**
   ```python
   # Было:
   self.filter_type_var.trace('w', self._on_filter_type_change)
   
   # Стало:
   self.filter_type_var.trace_add('write', self._on_filter_type_change)
   ```

## Изменения синтаксиса

### Старый синтаксис (Python < 3.13):
```python
variable.trace('w', callback)  # 'w' = write
variable.trace('r', callback)  # 'r' = read
variable.trace('u', callback)  # 'u' = unset
```

### Новый синтаксис (Python 3.13+):
```python
variable.trace_add('write', callback)   # вместо 'w'
variable.trace_add('read', callback)    # вместо 'r'
variable.trace_add('unset', callback)  # вместо 'u'
```

## Результат

### ✅ Исправлено:
- Ошибка `bad option "variable"` устранена
- Все компоненты работают с Python 3.13
- Группированный UI запускается без ошибок
- Сохранена обратная совместимость

### 🎯 Преимущества:
1. **Совместимость с Python 3.13** - использует новый синтаксис
2. **Читаемость** - `trace_add('write', ...)` более понятно чем `trace('w', ...)`
3. **Надежность** - официально поддерживаемый синтаксис
4. **Будущее** - готовность к новым версиям Python

## Тестирование

Создан тестовый скрипт `test_trace_fix.py` для проверки исправлений:

```bash
python3 test_trace_fix.py
```

## Запуск

Теперь приложение запускается без ошибок:

```bash
python3 run.py
```

## Структура исправлений

```
gui/
├── components/
│   ├── color_transform_settings.py    # ✅ trace_add('write', ...)
│   ├── smoothing_settings.py          # ✅ trace_add('write', ...)
│   ├── sharpness_settings.py         # ✅ trace_add('write', ...)
│   ├── transform_settings.py          # ✅ trace_add('write', ...)
│   ├── modern_transform_settings.py   # ✅ trace_add('write', ...)
│   └── modern_smoothing_settings.py  # ✅ trace_add('write', ...)
└── grouped_main_window.py             # ✅ Работает с исправленными компонентами
```

Все исправления сохраняют функциональность и улучшают совместимость с Python 3.13!
