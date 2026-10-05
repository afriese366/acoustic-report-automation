"""Deterministische deutsche Zahlenformatierung."""

from decimal import Decimal, ROUND_HALF_UP


def round_half_up(value: float) -> int:
    """Rundet .5 kaufmännisch auf die nächste ganze Zahl."""
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def format_decimal(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}f}".replace(".", ",")


def format_db(value: float, digits: int = 1) -> str:
    return f"{format_decimal(value, digits)} dB(A)"
