"""Controller that wires the model with the static dataset."""

from src.model.data import DATA
from src.model.rain_model import RainModel


class SimulationController:
    """Run the simulation over the fixed dataset and collect results."""

    def __init__(self, model: RainModel):
        self.model = model

    def run(self) -> list[dict]:
        """Run the model for every entry in DATA and return the results."""
        results = []

        for data in DATA:
            result = self.model.calculate(
                data["humidity"],
                data["cloudiness"],
                data["temperature"],
            )
            result["time"] = data["time"]
            results.append(result)

        return results
