#!/bin/bash
# Скрипт для проверки синтаксиса всех Python файлов

echo "Checking Python syntax..."

# Находим все .py файлы и проверяем их
for file in $(find app tests -name "*.py" 2>/dev/null); do
    python3 -m py_compile "$file"
    if [ $? -eq 0 ]; then
        echo "✓ $file"
    else
        echo "✗ $file - SYNTAX ERROR"
        exit 1
    fi
done

echo ""
echo "All Python files have valid syntax!"
