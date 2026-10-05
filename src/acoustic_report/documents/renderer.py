"""Rendert den fachlichen Kontext in eine neutrale Word-Vorlage."""

from pathlib import Path

import jinja2
from docxtpl import DocxTemplate


def render_template(template_path: Path, context: dict, output_path: Path) -> None:
    if not template_path.is_file():
        raise FileNotFoundError(f"Word-Vorlage nicht gefunden: {template_path}")
    document = DocxTemplate(template_path)
    environment = jinja2.Environment(trim_blocks=True, lstrip_blocks=True, autoescape=True)
    document.render(context, jinja_env=environment)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(output_path)
