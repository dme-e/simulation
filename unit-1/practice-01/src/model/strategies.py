from abc import ABC, abstractmethod


class RainModelStrategy(ABC):

    @abstractmethod
    def calculate_index(self, humidity, cloudiness, temperature_factor):
        pass


class BaseModelStrategy(RainModelStrategy):

    def calculate_index(self, humidity, cloudiness, temperature_factor):
        return (
            0.5 * humidity
            + 0.3 * cloudiness
            + 0.2 * temperature_factor
        )


class AdjustedModelStrategy(RainModelStrategy):

    def calculate_index(self, humidity, cloudiness, temperature_factor):
        return (
            0.4 * humidity
            + 0.4 * cloudiness
            + 0.2 * temperature_factor
        )