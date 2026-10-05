from model.temperature import get_temperature_factor
from model.strategies import RainModelStrategy


class RainModel:
    def __init__(self, strategy: RainModelStrategy):
        self.strategy = strategy

    def calculate(self, humidity, cloudiness, temperature):
        h = humidity / 100
        n = cloudiness / 100
        tf = get_temperature_factor(temperature)

        index = self.strategy.calculate_index(h, n, tf)
        state = self._get_state(index)

        return {
            "humidity": h,
            "cloudiness": n,
            "temperature": temperature,
            "temperature_factor": tf,
            "index": index,
            "state": state
        }

    def _get_state(self, index):
        if index < 0.40:
            return "Sin lluvia"
        elif index < 0.60:
            return "Baja posibilidad"
        elif index < 0.75:
            return "Lluvia probable"
        else:
            return "Lluvia"