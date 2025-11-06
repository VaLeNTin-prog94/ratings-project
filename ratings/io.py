from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, Dict, List


REQUIRED_COLUMNS = ("name", "brand", "price", "rating")


def read_csv_files(paths: Iterable[str | Path]) -> List[Dict[str, str]]:
    """
    Читает несколько CSV, валидирует обязательные колонки и возвращает список строк (dict).
    Допускает:
      - лишние колонки
      - разные регистры в заголовках (нормализуем к нижнему)
    """
    rows: List[Dict[str, str]] = []
    for p in paths:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {path}")

        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            field_map = {name: name.lower() for name in reader.fieldnames or []}
            missing = [c for c in REQUIRED_COLUMNS if c not in (n.lower() for n in (reader.fieldnames or []))]
            if missing:
                raise ValueError(f"В файле {path} отсутствуют колонки: {', '.join(missing)}")
            for raw in reader:
                row = {field_map[k]: v for k, v in raw.items() if k is not None}
                rows.append(row)
    return rows
