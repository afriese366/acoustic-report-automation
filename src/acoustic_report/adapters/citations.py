"""Deterministische Referenzliste aus einem kleinen JSON-Katalog."""

import json
from pathlib import Path

from acoustic_report.domain.models import InputValidationError


def load_citations(path: str | Path, keys: tuple[str, ...]) -> list[dict[str, str]]:
    citation_path = Path(path)
    if not citation_path.is_file():
        raise FileNotFoundError(f"Referenzdatei nicht gefunden: {citation_path}")
    raw = json.loads(citation_path.read_text(encoding="utf-8"))
    result = []
    for index, key in enumerate(keys, start=1):
        item = raw.get(key)
        if not isinstance(item, dict) or not str(item.get("title", "")).strip():
            raise InputValidationError(f"Referenz {key} fehlt oder ist ungültig.")
        result.append({"reference": f"[{index}]", "title": str(item["title"]).strip()})
    return result
