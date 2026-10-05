"""Reine, nachvollziehbare Regeln für die Demo-Bewertung."""

import math

from acoustic_report.domain.formatting import round_half_up
from acoustic_report.domain.models import (
    AcousticDataset,
    AssessmentResult,
    InputValidationError,
)


def energetic_sum(levels_db: list[float] | tuple[float, ...]) -> float:
    """Addiert Schalldruckpegel energetisch statt arithmetisch."""
    if not levels_db:
        raise InputValidationError("Für die Pegelsumme ist mindestens ein Wert erforderlich.")
    return 10.0 * math.log10(sum(10.0 ** (level / 10.0) for level in levels_db))


def assess_receivers(dataset: AcousticDataset) -> tuple[AssessmentResult, ...]:
    """Bewertet jeden Immissionsort gegen seinen synthetischen Tagesrichtwert."""
    dataset.validate()
    results = []
    for receiver in dataset.receivers:
        levels = [
            item.level_db
            for item in dataset.contributions
            if item.receiver_id == receiver.receiver_id
        ]
        if not levels:
            raise InputValidationError(
                f"Für Immissionsort {receiver.receiver_id} fehlen Pegelbeiträge."
            )
        calculated = energetic_sum(levels)
        rating = round_half_up(calculated)
        margin = round_half_up(receiver.limit_db) - rating
        results.append(
            AssessmentResult(
                receiver=receiver,
                calculated_level_db=calculated,
                rating_level_db=rating,
                margin_db=margin,
                compliant=rating <= receiver.limit_db,
            )
        )
    return tuple(results)
