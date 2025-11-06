from __future__ import annotations
from typing import Iterable, Dict, List


class BaseReport:
    """
    Базовый класс для отчёта. Любой новый отчёт должен унаследоваться и реализовать:
      - name (str): машинное имя отчёта
      - headers() -> list[str]: список заголовков таблицы
      - run(rows) -> list[dict]: данные отчёта
    """
    name: str = "base"

    def headers(self) -> List[str]:
        raise NotImplementedError

    def run(self, rows: Iterable[Dict[str, str]]) -> List[Dict[str, object]]:
        raise NotImplementedError
