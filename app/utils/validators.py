from typing import Optional


def require_text(value: Optional[str], name: str) -> str:
    if not value or not value.strip():
        raise ValueError(f'El campo {name} es obligatorio.')
    return value.strip()


def require_positive_number(value: float, name: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f'El campo {name} debe ser numérico.')

    if number < 0:
        raise ValueError(f'El campo {name} debe ser mayor o igual a cero.')
    return number
