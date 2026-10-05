"""Orchestriert die vollständige, deterministische Report-Pipeline."""

from pathlib import Path

from acoustic_report.adapters.citations import load_citations
from acoustic_report.adapters.configuration import load_config
from acoustic_report.adapters.spreadsheet_reader import read_workbook
from acoustic_report.documents.context_builder import build_context
from acoustic_report.documents.postprocess import insert_results_table
from acoustic_report.documents.renderer import render_template
from acoustic_report.domain.acoustic_rules import assess_receivers


def generate_report(config_path: str | Path) -> Path:
    config = load_config(config_path)
    dataset = read_workbook(config.workbook_path)
    results = assess_receivers(dataset)
    citations = load_citations(config.citations_path, ("DEMO_METHOD", "DEMO_QUALITY"))
    context = build_context(config.project, dataset, results, citations)
    render_template(config.template_path, context, config.output_path)
    insert_results_table(config.output_path, context["results"])
    return config.output_path
