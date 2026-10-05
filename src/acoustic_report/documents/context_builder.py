"""Übersetzt Domänenobjekte in einen stabilen Template-Kontext."""

from acoustic_report.domain.formatting import format_db, format_decimal
from acoustic_report.domain.models import AcousticDataset, AssessmentResult, Project


def build_context(
    project: Project,
    dataset: AcousticDataset,
    results: tuple[AssessmentResult, ...],
    citations: list[dict[str, str]],
) -> dict:
    compliant_count = sum(result.compliant for result in results)
    return {
        "project": {
            "id": project.project_id,
            "title": project.title,
            "report_date": project.report_date.strftime("%d.%m.%Y"),
            "author": project.author,
        },
        "sources": [
            {
                "id": source.source_id,
                "description": source.description,
                "sound_power": format_db(source.sound_power_db),
                "correction": format_decimal(source.correction_db),
                "corrected": format_db(source.corrected_sound_power_db),
            }
            for source in dataset.sources
        ],
        "results": [
            {
                "receiver_id": result.receiver.receiver_id,
                "description": result.receiver.description,
                "area_type": result.receiver.area_type,
                "calculated_level": format_db(result.calculated_level_db),
                "rating_level": f"{result.rating_level_db} dB(A)",
                "limit": f"{int(result.receiver.limit_db)} dB(A)",
                "margin": f"{result.margin_db} dB",
                "status": "compliant" if result.compliant else "exceeded",
            }
            for result in results
        ],
        "citations": citations,
        "summary": {
            "receiver_count": len(results),
            "compliant_count": compliant_count,
            "all_compliant": compliant_count == len(results),
        },
    }
