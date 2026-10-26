"""Model package for population growth simulation."""

from src.model.config import SimulationConfig
from src.model.data import DATOS, TIEMPOS
from src.model.strategies import (
    PopulationModel,
    DeterministicModel,
    DiscreteModel,
    StochasticModel,
    EulerContinuousModel,
)

__all__ = [
    "SimulationConfig",
    "DATOS",
    "TIEMPOS",
    "PopulationModel",
    "DeterministicModel",
    "DiscreteModel",
    "StochasticModel",
    "EulerContinuousModel",
]