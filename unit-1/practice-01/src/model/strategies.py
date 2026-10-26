"""Strategy pattern for rain-index calculation.

Each strategy implements a different weighted combination of the normalized
input variables.  The model receives the strategy as a dependency, so new
formulas can be added without changing the model itself (Open/Closed Principle).
"""

from abc import ABC, abstractmethod


class RainModelStrategy(ABC):
    """Abstract strategy for calculating the rain index."""

    @abstractmethod
    def calculate_index(
        self,
        humidity: float,
        cloudiness: float,
        temperature_factor: float,
    ) -> float:
        """Calculate and return the rain index.

        All arguments are already normalized: humidity and cloudiness are in
        the range [0, 1], and temperature_factor comes from the lookup table.
        """


class BaseModelStrategy(RainModelStrategy):
    """Original weights from the guide: 50% humidity, 30% cloudiness, 20% temperature."""

    def calculate_index(
        self,
        humidity: float,
        cloudiness: float,
        temperature_factor: float,
    ) -> float:
        return 0.5 * humidity + 0.3 * cloudiness + 0.2 * temperature_factor


class AdjustedModelStrategy(RainModelStrategy):
    """Adjusted weights that give cloudiness the same importance as humidity."""

    def calculate_index(
        self,
        humidity: float,
        cloudiness: float,
        temperature_factor: float,
    ) -> float:
        return 0.4 * humidity + 0.4 * cloudiness + 0.2 * temperature_factor
