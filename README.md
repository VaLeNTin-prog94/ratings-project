# ratings-project

Скрипт читает один или несколько CSV с товарами и строит отчёт (**average-rating**) — средний рейтинг по брендам (сортировка по убыванию).

## Требования
- Python 3.9+
- Библиотеки: только стандартная, для вывода таблицы — `tabulate` (разрешено по условиям)

## Установка окружения
```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
