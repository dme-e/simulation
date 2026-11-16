"""Tests for the Monte Carlo model and the Java-compatible generator.

Plain asserts so the file runs under pytest or directly with:
    python tests/test_modelo.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.modelo import ExperimentoMonteCarlo, GeneradorJava


def test_generador_replica_java_random_seed_zero() -> None:
    # First java.util.Random(0).nextDouble() value (documented JDK behaviour).
    assert abs(GeneradorJava(0).next_double() - 0.730967787376657) < 1e-15


def test_generador_es_determinista() -> None:
    g1 = GeneradorJava(2026)
    g2 = GeneradorJava(2026)
    assert [g1.next_double() for _ in range(5)] == [g2.next_double() for _ in range(5)]


def test_misma_semilla_mismo_resultado() -> None:
    r1 = ExperimentoMonteCarlo(semilla=2026).ejecutar(1_000)
    r2 = ExperimentoMonteCarlo(semilla=2026).ejecutar(1_000)
    assert r1.aciertos == r2.aciertos
    assert r1.pi_estimado == r2.pi_estimado


def test_estimacion_converge_a_pi() -> None:
    resultado = ExperimentoMonteCarlo(semilla=2026).ejecutar(100_000)
    assert resultado.error_absoluto < 0.02
    assert resultado.pi_estimado == 4.0 * resultado.aciertos / resultado.n
    assert abs(resultado.pi_estimado - math.pi) == resultado.error_absoluto


def test_n_invalido_lanza_error() -> None:
    try:
        ExperimentoMonteCarlo().ejecutar(0)
    except ValueError:
        return
    raise AssertionError("se esperaba ValueError para n <= 0")


def main() -> None:
    pruebas = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for prueba in pruebas:
        prueba()
        print(f"OK  {prueba.__name__}")
    print(f"{len(pruebas)} pruebas ejecutadas.")


if __name__ == "__main__":
    main()
