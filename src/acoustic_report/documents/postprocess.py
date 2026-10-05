"""Fügt die variable Ergebnistabelle ein und bereinigt Dokumentmetadaten."""

from pathlib import Path
import re
from zipfile import ZIP_DEFLATED, ZipFile

from docx import Document

from acoustic_report.documents.docx_helpers import (
    find_marker,
    format_cell,
    remove_paragraph,
    repeat_table_header,
    shade_cell,
)


RESULTS_MARKER = "[[RESULTS_TABLE]]"


def _scrub_metadata(output_path: Path) -> None:
    """Entfernt persönliche Eigenschaften und Word-Sitzungskennungen."""
    temporary_path = output_path.with_suffix(".scrubbed.tmp")
    with ZipFile(output_path, "r") as source, ZipFile(
        temporary_path, "w", ZIP_DEFLATED
    ) as target:
        for item in source.infolist():
            payload = source.read(item.filename)
            if item.filename == "docProps/core.xml":
                for tag in (b"dc:creator", b"cp:lastModifiedBy", b"dcterms:created", b"dcterms:modified"):
                    payload = re.sub(
                        rb"<" + tag + rb"\b[^>]*(?:/>|>.*?</" + tag + rb">)",
                        b"",
                        payload,
                        flags=re.DOTALL,
                    )
            elif item.filename.startswith("word/") and item.filename.endswith(".xml"):
                payload = re.sub(rb'\s+w:rsid[A-Za-z0-9]*="[^"]*"', b"", payload)
            target.writestr(item, payload)
    temporary_path.replace(output_path)


def insert_results_table(output_path: str | Path, rows: list[dict]) -> None:
    document = Document(output_path)
    marker = find_marker(document, RESULTS_MARKER)
    if marker is None:
        raise ValueError(f"Marker {RESULTS_MARKER} fehlt in der Vorlage.")

    columns = (
        ("receiver_id", "Receiver"),
        ("description", "Description"),
        ("area_type", "Area"),
        ("calculated_level", "Calculated"),
        ("rating_level", "Rating"),
        ("limit", "Limit"),
        ("margin", "Margin"),
        ("status", "Status"),
    )
    table = document.add_table(rows=1, cols=len(columns))
    table.style = "Table Grid"
    table.autofit = True
    repeat_table_header(table.rows[0])
    for index, (_, label) in enumerate(columns):
        cell = table.rows[0].cells[index]
        cell.text = label
        shade_cell(cell, "1F4E78")
        format_cell(cell, bold=True, centered=True, color="FFFFFF")

    for row_index, row in enumerate(rows):
        cells = table.add_row().cells
        for column_index, (key, _) in enumerate(columns):
            cells[column_index].text = str(row[key])
            if row_index % 2:
                shade_cell(cells[column_index], "EAF2F8")
            format_cell(cells[column_index], centered=key not in {"description", "area_type"})

    marker._p.addnext(table._tbl)
    remove_paragraph(marker)
    properties = document.core_properties
    properties.author = ""
    properties.last_modified_by = ""
    properties.title = "Synthetic Acoustic Assessment"
    properties.subject = "Portfolio demonstration"
    properties.keywords = ""
    properties.comments = ""
    document.save(output_path)
    _scrub_metadata(Path(output_path))
