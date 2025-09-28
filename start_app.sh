#!/bin/bash

# Активируем виртуальное окружение и запускаем приложение
cd "$(dirname "$0")"
source venv/bin/activate
python run_smoothing_app.py
