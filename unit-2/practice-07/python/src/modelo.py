"""Model: Monte Carlo experiment and the pseudo-random generator.

The generator is a bit-for-bit replica of java.util.Random (48-bit linear
congruential generator) so that the Python and Java implementations produce
the exact same sequence of points for the same seed and sample size.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass

# Constants of the java.util.Random LCG.
_MULTIPLIER = 0x5DEECE66D  # 25214903917
_ADDEND = 0xB
_MASK = (1 << 48) - 1
_TWO_POW_53 = float(1 << 53)


class GeneradorJava:
    """Replica of java.util.Random: 48-bit LCG with the JDK sampling formulas.

    Seeding and sampling follow the JDK implementation exactly:
    seed' = (seed ^ 0x5DEECE66D) & (2^48 - 1)
    nextDouble() = ((next(26) << 27) + next(27)) / 2^53
    """

    def __init__(self, semilla: int = 0) -> None:
        self._semilla = (semilla ^ _MULTIPLIER) & _MASK

    def _next(self, bits: int) -> int:
        self._semilla = (self._semilla * _MULTIPLIER + _ADDEND) & _MASK
        return self._semilla >> (48 - bits)

    def next_double(self) -> float:
        return ((self._next(26) << 27) + self._next(27)) / _TWO_POW_53


@dataclass(frozen=True)
class ResultadoExperimento:
    """Variables registradas por la guía para un tamaño de muestra N."""

    n: int
    aciertos: int  # Nc: puntos dentro del círculo
    pi_estimado: float  # 4 * Nc / N
    error_absoluto: float  # |pi estimado - pi real|
    tiempo_segundos: float  # tiempo de ejecución


class ExperimentoMonteCarlo:
    """Estimates pi by sampling points uniformly in the square [-1, 1] x [-1, 1]
    and counting how many fall inside the inscribed circle (x^2 + y^2 <= 1).

    pi ~= 4 * (Nc / N)
    """

    def __init__(self, semilla: int = 2026) -> None:
        self.semilla = semilla

    def ejecutar(self, n: int) -> ResultadoExperimento:
        if n <= 0:
            raise ValueError("n must be positive")
        rng = GeneradorJava(self.semilla)
        next_double = rng.next_double
        aciertos = 0
        inicio = time.perf_counter()
        for _ in range(n):
            x = next_double() * 2.0 - 1.0
            y = next_double() * 2.0 - 1.0
            if x * x + y * y <= 1.0:
                aciertos += 1
        tiempo = time.perf_counter() - inicio
        pi_estimado = 4.0 * aciertos / n
        return ResultadoExperimento(
            n=n,
            aciertos=aciertos,
            pi_estimado=pi_estimado,
            error_absoluto=abs(pi_estimado - math.pi),
            tiempo_segundos=tiempo,
        )
