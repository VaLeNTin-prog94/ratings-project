from __future__ import annotations

import io
import csv
from ratings.reports.average_rating import AverageRatingReport


def _rows_from_csv_text(text: str):
    f = io.StringIO(text)
    reader = csv.DictReader(f)
    field_map = {name: name.lower() for name in reader.fieldnames or []}
    return [{field_map[k]: v for k, v in row.items() if k is not None} for row in reader]


def test_average_rating_basic():
    text = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
"""
    rows = _rows_from_csv_text(text)
    rep = AverageRatingReport()
    data = rep.run(rows)

    assert data[0]["brand"] == "apple"
    assert data[0]["rating"] == 4.9
    assert len(data) == 3


def test_average_rating_aggregates_multiple_rows():
    text = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
iphone 14,apple,799,4.7
galaxy s23 ultra,samsung,1199,4.8
"""
    rows = _rows_from_csv_text(text)
    rep = AverageRatingReport()
    data = rep.run(rows)

    # apple avg = (4.9 + 4.7)/2 = 4.8  → равен samsung 4.8, сортировка по бренду
    assert data[0]["rating"] == 4.8
    assert data[1]["rating"] == 4.8
    assert {data[0]["brand"], data[1]["brand"]} == {"apple", "samsung"}


def test_average_rating_ignores_empty_or_bad_rating():
    text = """name,brand,price,rating
iphone 15 pro,apple,999,
iphone 14,apple,799,not_a_number
galaxy s23 ultra,samsung,1199,4.8
"""
    rows = _rows_from_csv_text(text)
    rep = AverageRatingReport()
    data = rep.run(rows)

    assert len(data) == 1
    assert data[0]["brand"] == "samsung"
    assert data[0]["rating"] == 4.8


def test_average_rating_handles_comma_decimal():
    text = """name,brand,price,rating
galaxy a34,samsung,299,4,3
"""
    rows = _rows_from_csv_text(text)
    rows[0]["rating"] = "4,3"

    rep = AverageRatingReport()
    data = rep.run(rows)

    assert data[0]["rating"] == 4.3
