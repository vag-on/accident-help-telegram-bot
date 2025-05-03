#!/bin/bash

echo "Удаление старой установки..."
pip uninstall -y accident_help_bot

echo "Очистка кэша pip..."
pip cache purge

echo "Установка пакета в режиме разработки..."
pip install -e .

echo "Установка завершена!"
