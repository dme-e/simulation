"""Immutable configuration for the population growth simulation."""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    """Immutable configuration with validation for population growth models.

    Attributes:
        P0: Initial population.
        r: Growth rate.
        sigma: Noise standard deviation for stochastic model.
        dt: Time step for Euler continuous model.
        tiempo: Total simulation time (number of periods).
        DATOS: Real population data points for comparison.
    """

    P0: float
    r: float
    sigma: float
    dt: float
    tiempo: int
    DATOS: tuple[float, ...]

    def __post_init__(self) -> None:
        """Validate all configuration parameters."""
        if self.P0 <= 0:
            raise ValueError(f"P0 must be positive, got {self.P0}")
        if self.r < 0:
            raise ValueError(f"r must be non-negative, got {self.r}")
        if self.sigma < 0:
            raise ValueError(f"sigma must be non-negative, got {self.sigma}")
        if self.dt <= 0:
            raise ValueError(f"dt must be positive, got {self.dt}")
        if self.tiempo <= 0:
            raise ValueError(f"tiempo must be positive, got {self.tiempo}")
        if len(self.DATOS) != self.tiempo + 1:
            raise ValueError(
                f"DATOS length ({len(self.DATOS)}) must be tiempo + 1 ({self.tiempo + 1})"
            )
        if any(d < 0 for d in self.DATOS):
            raise ValueError("DATOS must not contain negative values")


# Default configuration matching the practice guide
DEFAULT_CONFIG: Final[SimulationConfig] = SimulationConfig(
    P0=1000.0,
    r=0.15,
    sigma=20.0,
    dt=0.1,
    tiempo=6,  # len(DATOS) - 1 = 7 - 1 = 6
    DATOS=(1000, 1100, 1250, 1400, 1600, 1850, 2100),
)