"""Merges the Python and Java CSVs into the practice guide's comparison table.

It also verifies the guide's requirement that both implementations produce the
same sequence with the same parameters: for each N, the number of hits (Nc)
and the pi estimate must be identical.

Run command: python scripts/comparar_resultados.py
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
PYTHON_CSV_DEFECTO = BASE / "resultados" / "resultados_python.csv"
JAVA_CSV_DEFECTO = BASE / "resultados" / "resultados_java.csv"
SALIDA_DEFECTO = BASE / "resultados" / "tabla_comparativa.md"


def leer_resultados(ruta: Path) -> list[dict[str, str]]:
    with ruta.open(newline="", encoding="utf-8") as archivo:
        return list(csv.DictReader(archivo))


def formatear_n(n: str) -> str:
    return f"{int(n):,}".replace(",", " ")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Genera la tabla comparativa Python vs Java (guía práctica 07)."
    )
    parser.add_argument("--python-csv", type=Path, default=PYTHON_CSV_DEFECTO)
    parser.add_argument("--java-csv", type=Path, default=JAVA_CSV_DEFECTO)
    parser.add_argument("--salida", type=Path, default=SALIDA_DEFECTO)
    args = parser.parse_args()

    filas_python = leer_resultados(args.python_csv)
    filas_java = leer_resultados(args.java_csv)
    if len(filas_python) != len(filas_java):
        print("Error: los archivos tienen distinta cantidad de filas.", file=sys.stderr)
        sys.exit(1)

    lineas = [
        "| N | pi estimado | Error | Tiempo Python | Tiempo Java |",
        "|---|---|---|---|---|",
    ]
    for fp, fj in zip(filas_python, filas_java):
        if fp["n"] != fj["n"]:
            print(f"Error: N no coincide ({fp['n']} vs {fj['n']}).", file=sys.stderr)
            sys.exit(1)
        if fp["aciertos"] != fj["aciertos"]:
            print(
                f"Error: la secuencia difiere en N={fp['n']} "
                f"(aciertos {fp['aciertos']} vs {fj['aciertos']}).",
                file=sys.stderr,
            )
            sys.exit(1)
        lineas.append(
            f"| {formatear_n(fp['n'])} "
            f"| {float(fp['pi_estimado']):.6f} "
            f"| {float(fp['error_absoluto']):.6f} "
            f"| {float(fp['tiempo_segundos']):.4f} s "
            f"| {float(fj['tiempo_segundos']):.4f} s |"
        )

    tabla = "\n".join(lineas)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(
        "# Tabla comparativa Python vs Java\n\n"
        "Ambas implementaciones usan la misma semilla y el mismo generador\n"
        "(LCG de java.util.Random), por lo que producen la misma secuencia.\n\n"
        f"{tabla}\n",
        encoding="utf-8",
    )
    print(tabla)
    print()
    print("Secuencias verificadas: Python y Java generan los mismos resultados.")
    print(f"Tabla guardada en {args.salida}")


if __name__ == "__main__":
    main()
