"""Temperature-factor lookup used by the rain model."""


# Sorted from highest temperature threshold to lowest.  The first matching row
# is the factor that applies.
_TEMPERATURE_TABLE = (
    (28, 0.10),
    (26, 0.20),
    (24, 0.30),
    (22, 0.40),
    (20, 0.50),
    (18, 0.60),
    (16, 0.70),
    (14, 0.80),
    (12, 0.90),
    (10, 1.00),
)


def get_temperature_factor(temperature: float) -> float:
    """Return the temperature factor for a given Celsius value.

    The guide provides discrete values; this function assigns the factor of the
    nearest lower-or-equal reference temperature.  Temperatures above 28 °C get
    the lowest factor (0.10) and temperatures below 10 °C get the highest (1.00).
    """
    for threshold, factor in _TEMPERATURE_TABLE:
        if temperature >= threshold:
            return factor
    return 1.00
