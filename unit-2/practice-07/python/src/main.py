"""Entry point of the Python Monte Carlo experiment (practice 07).

Run command: python -m src.main
"""
from __future__ import annotations

import argparse

from src.controlador import TAMANOS_DEFECTO, ExperimentoControlador
from src.modelo import ExperimentoMonteCarlo

SEMILLA_DEFECTO = 2026
CSV_DEFECTO = "../resultados/resultados_python.csv"


def crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m src.main",
        description="Estimación de pi mediante el método de Monte Carlo.",
    )
    parser.add_argument(
        "--tamanos",
        type=int,
        nargs="+",
        default=list(TAMANOS_DEFECTO),
        help="Tamaños de muestra N a ejecutar (por defecto: 1000 10000 100000 1000000).",
    )
    parser.add_argument(
        "--semilla",
        type=int,
        default=SEMILLA_DEFECTO,
        help="Semilla del generador pseudoaleatorio (por defecto: 2026).",
    )
    parser.add_argument(
        "--csv",
        default=CSV_DEFECTO,
        help="Ruta del archivo CSV de resultados.",
    )
    parser.add_argument(
        "--grafico",
        default=None,
        help="Ruta del gráfico de error absoluto (requiere matplotlib).",
    )
    return parser


def main() -> None:
    args = crear_parser().parse_args()
    modelo = ExperimentoMonteCarlo(semilla=args.semilla)
    controlador = ExperimentoControlador(modelo, tamanos=tuple(args.tamanos))
    resultados = controlador.ejecutar()
    controlador.exportar(resultados, args.csv, args.grafico)


if __name__ == "__main__":
    main()
