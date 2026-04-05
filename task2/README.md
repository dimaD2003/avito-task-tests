# Автоматические тесты для API

## 1. Клонирование репо



Клонируем репозиторий:
```bash
git clone https://github.com/dimaD2003/avito-task-tests.git
cd avito-task-tests/task2
```
## 2. Установка зависимостей

Для работы тестов требуется Python 3.10+.

1. Создать окружение с Python 3.10:
```bash
conda create -n avito-tests python=3.10 -y
```
2. Активировать окружение
```bash
conda activate avito-tests
```

3. Установить зависимости:
```bash
pip install -r requirements.txt
```

## 3. Запуск автотестов
1. Запуск всех автотестов
```bash
pytest  -v test/
```
2. Запуск конкретного файла
```bash
pytest -v test/test_get_item.py
pytest -v test/test_get_seller.py
pytest -v test/test_get_statistic.py
pytest -v test/test_post_item.py
```
* В ходе выплнения тестов должно не пройти 3 тетса , н акаждый есть баг-репорт в в файле  **BUGS.md** *

## 3. Линтеры
### Конфигурация линтеров и форматтеров

Для обеспечения единообразного стиля кода и проверки качества используются следующие инструменты:

### 1. Flake8
**Цель:** Проверка PEP8, предупреждения о потенциальных ошибках и проблемах со стилем.

**Конфигурация:** `.flake8` 
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
```


### Запуск
```bash
flake8 test
```
### 2. Black
Цель: Автоматическое форматирование кода в соответствии с PEP8.

**Конфигурация:**
```ini
[tool.black]
line-length = 88
target-version = ['py310']
```
### Запуск
```bash
black test
```

### 3. isort :
Цель: Автоматическая сортировка импортов по стандартам PEP8

**Конфигурация:**
```ini
[settings]
profile = black
line_length = 88
```
### Запуск
```bash
isort test
```
