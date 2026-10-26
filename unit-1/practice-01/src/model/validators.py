"""Input validation helpers for the rain simulation model."""


def validate_reading(humidity: float, cloudiness: float, temperature: float) -> None:
    """Validate a single weather reading.

    Args:
        humidity: Percentage of humidity (0-100).
        cloudiness: Percentage of cloudiness (0-100).
        temperature: Temperature in degrees Celsius.

    Raises:
        ValueError: If any value is out of range or not numeric.
        TypeError: If any value is not a number.
    """
    for name, value, low, high in (
        ("humidity", humidity, 0, 100),
        ("cloudiness", cloudiness, 0, 100),
    ):
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be a number, got {type(value).__name__}")
        if not low <= value <= high:
            raise ValueError(f"{name} must be between {low} and {high}, got {value}")

    if not isinstance(temperature, (int, float)):
        raise TypeError(
            f"temperature must be a number, got {type(temperature).__name__}"
        )
