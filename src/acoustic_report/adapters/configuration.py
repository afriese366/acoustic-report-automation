"""Lädt die portable JSON-Konfiguration des Demo-Projekts."""

from dataclasses import dataclass
from datetime import date
import json
from pathlib import Path

from acoustic_report.domain.models import InputValidationError, Project


@dataclass(frozen=True)
class AppConfig:
    project: Project
    workbook_path: Path
    template_path: Path
    citations_path: Path
    output_path: Path


def _resolve(base: Path, value: str, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise InputValidationError(f"Konfigurationsfeld {field} fehlt.")
    return (base / value).resolve()


def load_config(path: str | Path) -> AppConfig:
    config_path = Path(path).resolve()
    if not config_path.is_file():
        raise FileNotFoundError(f"Konfiguration nicht gefunden: {config_path}")
    raw = json.loads(config_path.read_text(encoding="utf-8"))
    project_raw = raw.get("project", {})
    try:
        project = Project(
            project_id=str(project_raw["project_id"]),
            title=str(project_raw["title"]),
            report_date=date.fromisoformat(project_raw["report_date"]),
            author=str(project_raw["author"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise InputValidationError("Projektkonfiguration ist unvollständig oder ungültig.") from exc
    project.validate()
    base = config_path.parent
    return AppConfig(
        project=project,
        workbook_path=_resolve(base, raw.get("input_workbook", ""), "input_workbook"),
        template_path=_resolve(base, raw.get("template", ""), "template"),
        citations_path=_resolve(base, raw.get("citations", ""), "citations"),
        output_path=_resolve(base, raw.get("output_file", ""), "output_file"),
    )
