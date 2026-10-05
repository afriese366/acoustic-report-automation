"""Typisierte Datenstrukturen der synthetischen Schallprognose."""

from dataclasses import dataclass
from datetime import date


class InputValidationError(ValueError):
    """Meldet fachlich verständliche Fehler in Eingabedaten."""


@dataclass(frozen=True)
class Project:
    project_id: str
    title: str
    report_date: date
    author: str

    def validate(self) -> None:
        missing = [
            name
            for name, value in (
                ("project_id", self.project_id),
                ("title", self.title),
                ("author", self.author),
            )
            if not value.strip()
        ]
        if missing:
            raise InputValidationError(
                "Fehlende Projektfelder: " + ", ".join(missing)
            )


@dataclass(frozen=True)
class NoiseSource:
    source_id: str
    description: str
    sound_power_db: float
    correction_db: float = 0.0

    @property
    def corrected_sound_power_db(self) -> float:
        return self.sound_power_db + self.correction_db


@dataclass(frozen=True)
class Receiver:
    receiver_id: str
    description: str
    area_type: str
    limit_db: float


@dataclass(frozen=True)
class Contribution:
    receiver_id: str
    source_id: str
    level_db: float


@dataclass(frozen=True)
class AcousticDataset:
    sources: tuple[NoiseSource, ...]
    receivers: tuple[Receiver, ...]
    contributions: tuple[Contribution, ...]

    def validate(self) -> None:
        if not self.sources:
            raise InputValidationError("Mindestens eine Schallquelle ist erforderlich.")
        if not self.receivers:
            raise InputValidationError("Mindestens ein Immissionsort ist erforderlich.")

        source_ids = [source.source_id for source in self.sources]
        receiver_ids = [receiver.receiver_id for receiver in self.receivers]
        if len(source_ids) != len(set(source_ids)):
            raise InputValidationError("Quellenkennungen müssen eindeutig sein.")
        if len(receiver_ids) != len(set(receiver_ids)):
            raise InputValidationError("Immissionsortkennungen müssen eindeutig sein.")

        unknown_sources = {
            item.source_id for item in self.contributions if item.source_id not in source_ids
        }
        unknown_receivers = {
            item.receiver_id
            for item in self.contributions
            if item.receiver_id not in receiver_ids
        }
        if unknown_sources:
            raise InputValidationError(
                "Unbekannte Quellen in Contributions: " + ", ".join(sorted(unknown_sources))
            )
        if unknown_receivers:
            raise InputValidationError(
                "Unbekannte Immissionsorte in Contributions: "
                + ", ".join(sorted(unknown_receivers))
            )


@dataclass(frozen=True)
class AssessmentResult:
    receiver: Receiver
    calculated_level_db: float
    rating_level_db: int
    margin_db: int
    compliant: bool
