"""Kommandozeileneinstieg für die Demo-Anwendung."""

import argparse
from pathlib import Path

from acoustic_report.application.generate_report import generate_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Erzeugt einen synthetischen schalltechnischen Demo-Bericht.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("examples/synthetic_project/project.json"),
        help="Pfad zur JSON-Projektkonfiguration",
    )
    args = parser.parse_args(argv)
    try:
        output = generate_report(args.config)
    except (FileNotFoundError, ValueError) as exc:
        parser.exit(2, f"Fehler: {exc}\n")
    print(f"Demo-Bericht erstellt: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
