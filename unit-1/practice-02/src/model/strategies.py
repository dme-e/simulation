"""Strategy pattern for population growth models.

Each model implements the PopulationModel interface, allowing them to be
used interchangeably by the controller (Open/Closed Principle).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
import math
from typing import Protocol

import numpy as np

from src.model.config import SimulationConfig


class PopulationModel(Protocol):
    """Protocol for population growth models.

    All models must implement a run method that takes a SimulationConfig
    and returns a list of time-population dictionaries.
    """

    def run(self, config: SimulationConfig) -> list[dict[str, float]]:
        """Run the simulation and return time-population pairs.

        Args:
            config: Simulation configuration.

        Returns:
            List of dicts with keys "tiempo" (float/int) and "poblacion" (float).
        """
        ...


@dataclass(frozen=True, slots=True)
class DeterministicModel:
    """Deterministic exponential growth model: P(t) = P0 * exp(r * t).

    No randomness; continuous exponential growth.
    """

    def run(self, config: SimulationConfig) -> list[dict[str, float]]:
        results = []
        for t in range(config.tiempo + 1):
            poblacion = config.P0 * math.exp(config.r * t)
            results.append({"tiempo": float(t), "poblacion": poblacion})
        return results


@dataclass(frozen=True, slots=True)
class DiscreteModel:
    """Discrete growth model: P_{n+1} = P_n + r * P_n.

    Population changes at discrete time intervals (per period).
    """

    def run(self, config: SimulationConfig) -> list[dict[str, float]]:
        results = []
        poblacion = config.P0
        results.append({"tiempo": 0.0, "poblacion": poblacion})

        for t in range(1, config.tiempo + 1):
            incremento = config.r * poblacion
            poblacion = poblacion + incremento
            results.append({"tiempo": float(t), "poblacion": poblacion})
        return results


@dataclass(frozen=True, slots=True)
class StochasticModel:
    """Stochastic growth model: P_{n+1} = P_n + r * P_n + noise.

    Noise is drawn from Normal(0, sigma), clamped to keep population >= 0.
    Uses a seeded RandomState for reproducibility.
    """

    seed: int = 42

    def run(self, config: SimulationConfig) -> list[dict[str, float]]:
        rng = np.random.RandomState(self.seed)
        results = []
        poblacion = config.P0
        results.append({"tiempo": 0.0, "poblacion": poblacion})

        for t in range(1, config.tiempo + 1):
            ruido = rng.normal(0.0, config.sigma)
            incremento = config.r * poblacion
            nueva_poblacion = poblacion + incremento + ruido
            if nueva_poblacion < 0:
                nueva_poblacion = 0.0
            poblacion = nueva_poblacion
            results.append({"tiempo": float(t), "poblacion": poblacion})
        return results


@dataclass(frozen=True, slots=True)
class EulerContinuousModel:
    """Continuous growth model via Euler's method: P_{t+dt} = P_t + dt * r * P_t.

    Approximates the differential equation dP/dt = r * P using step size dt.
    """

    def run(self, config: SimulationConfig) -> list[dict[str, float]]:
        results = []
        poblacion = config.P0
        t = 0.0
        results.append({"tiempo": t, "poblacion": poblacion})

        # Step through time with dt increments
        while t < config.tiempo - 1e-10:  # Avoid floating point issues
            cambio = config.r * poblacion
            poblacion = poblacion + config.dt * cambio
            t += config.dt
            # Round time to avoid floating point accumulation errors
            t = round(t, 10)
            results.append({"tiempo": t, "poblacion": poblacion})

        return results