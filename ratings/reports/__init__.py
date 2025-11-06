from __future__ import annotations

import pkgutil
import importlib
from typing import Dict, Type

from .base import BaseReport

# Регистрация всех отчётов в пакете (автоскан модулей)
def _discover_reports() -> Dict[str, Type[BaseReport]]:
    registry: Dict[str, Type[BaseReport]] = {}

    package = __name__  # ratings.reports
    for mod in pkgutil.iter_modules(__path__):  # type: ignore[name-defined]
        if mod.name in {"base", "__init__"}:
            continue
        importlib.import_module(f"{package}.{mod.name}")

    # Собираем всех наследников BaseReport
    for cls in BaseReport.__subclasses__():
        if not getattr(cls, "name", None):
            continue
        registry[cls.name] = cls

    return registry


REPORTS_REGISTRY: Dict[str, Type[BaseReport]] = _discover_reports()
