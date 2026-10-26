"""Controller that runs all population growth models and collects results."""

from src.model.config import SimulationConfig
from src.model.strategies import (
    DeterministicModel,
    DiscreteModel,
    StochasticModel,
    EulerContinuousModel,
)


class SimulationController:
    """Run all four population models and return labeled results."""

    def __init__(self, config: SimulationConfig | None = None):
        from src.model.config import DEFAULT_CONFIG

        self.config = config or DEFAULT_CONFIG
        self._models = {
            "Determinista": DeterministicModel(),
            "Discreto": DiscreteModel(),
            "Estocástico": StochasticModel(),
            "Continuo (Euler)": EulerContinuousModel(),
        }

    def run_all(self) -> dict[str, list[dict[str, float]]]:
        """Execute all models and return results keyed by model name.

        Returns:
            Dictionary mapping model names to their result lists.
        """
        results = {}
        for name, model in self._models.items():
            results[name] = model.run(self.config)
        return results

    def get_model_names(self) -> list[str]:
        """Return the list of model names in execution order."""
        return list(self._models.keys())