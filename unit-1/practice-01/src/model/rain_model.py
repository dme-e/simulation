"""Core rain prediction model."""

from src.model.temperature import get_temperature_factor
from src.model.strategies import RainModelStrategy
from src.model.state_classifier import StateClassifier
from src.model.validators import validate_reading


class RainModel:
    """Rain model composed of a calculation strategy and a state classifier.

    The model is deliberately small: it validates inputs, normalises the
    percentage variables, delegates the index calculation to a strategy, and
    classifies the result.  Each collaborator can be replaced or extended
    independently.
    """

    def __init__(
        self,
        strategy: RainModelStrategy,
        classifier: StateClassifier | None = None,
    ):
        self.strategy = strategy
        self.classifier = classifier or StateClassifier()

    def calculate(
        self,
        humidity: float,
        cloudiness: float,
        temperature: float,
    ) -> dict:
        """Calculate the rain index and state for a single reading."""
        validate_reading(humidity, cloudiness, temperature)

        h = humidity / 100.0
        n = cloudiness / 100.0
        tf = get_temperature_factor(temperature)

        index = self.strategy.calculate_index(h, n, tf)
        state = self.classifier.classify(index)

        return {
            "humidity": h,
            "cloudiness": n,
            "temperature": temperature,
            "temperature_factor": tf,
            "index": index,
            "state": state,
        }
