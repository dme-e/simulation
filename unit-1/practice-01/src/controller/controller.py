from model.data import DATA
from model.rain_model import RainModel


class SimulationController:
    def __init__(self, model):
        self.model = model

    def run(self):
        results = []

        for data in DATA:
            result = self.model.calculate(
                data["humidity"],
                data["cloudiness"],
                data["temperature"]
            )

            result["time"] = data["time"]
            results.append(result)

        return results