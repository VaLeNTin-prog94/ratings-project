from __future__ import annotations

import argparse
from typing import List, Dict
from tabulate import tabulate

from .io import read_csv_files
from .reports import REPORTS_REGISTRY, BaseReport


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ratings",
        description="Генератор отчётов по CSV с товарами."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV файлам (один или несколько).",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=sorted(REPORTS_REGISTRY.keys()),
        help="Название отчёта. Например: average-rating",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    rows = read_csv_files(args.files)
    report_cls = REPORTS_REGISTRY[args.report]
    report: BaseReport = report_cls()

    data: List[Dict[str, object]] = report.run(rows)

    headers = report.headers()
    table = [[row.get(h) for h in headers] for row in data]
    print(
        tabulate(
            table,
            headers=headers,
            tablefmt="grid",
            floatfmt=".2f",
            showindex=range(1, len(table) + 1),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
