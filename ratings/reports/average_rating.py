from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Dict, List

from .base import BaseReport


class AverageRatingReport(BaseReport):
    """
    Отчёт: средний рейтинг по брендам (сортировка по убыванию рейтинга, затем по бренду).
    """
    name = "average-rating"

    def headers(self) -> List[str]:
        return ["brand", "rating"]

    def run(self, rows: Iterable[Dict[str, str]]) -> List[Dict[str, object]]:
        sums = defaultdict(float)
        counts = defaultdict(int)

        for r in rows:
            brand = (r.get("brand") or "").strip()
            if not brand:
                continue
            rating_raw = (r.get("rating") or "").strip()
            if rating_raw == "":
                continue

            try:
                rating = float(rating_raw.replace(",", "."))
            except ValueError:
                continue

            sums[brand] += rating
            counts[brand] += 1

        result: List[Dict[str, object]] = []
        for brand, total in sums.items():
            avg = total / counts[brand] if counts[brand] else 0.0
            result.append({"brand": brand, "rating": round(avg, 2)})

        result.sort(key=lambda x: (-x["rating"], x["brand"]))
        return result
