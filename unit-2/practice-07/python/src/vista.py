"""View: renders experiment results as console table, CSV and chart.

The console and CSV headers follow the comparison table required by the
practice guide.
"""
from __future__ import annotations

import csv
from pathlib import Path

from src.modelo import ResultadoExperimento

ANCHO_N = 12
ANCHO_NUM = 14


class VistaConsola:
    """Renders results to the standard output."""

    def mostrar_fila(self, resultado: ResultadoExperimento) -> None:
        print(self._formatear_fila(resultado))

    def mostrar_tabla(
        self,
        resultados: list[ResultadoExperimento],
        columna_tiempo: str = "Tiempo Python",
    ) -> None:
        print()
        print(self._formatear_encabezado(columna_tiempo))
        print("-" * (ANCHO_N + 3 * ANCHO_NUM))
        for resultado in resultados:
            print(self._formatear_fila(resultado))
        print()

    @staticmethod
    def _formatear_encabezado(columna_tiempo: str) -> str:
        return (
            f"{'N':>{ANCHO_N}} {'pi estimado':>{ANCHO_NUM}} "
            f"{'Error':>{ANCHO_NUM}} {columna_tiempo:>{ANCHO_NUM}}"
        )

    @staticmethod
    def _formatear_fila(resultado: ResultadoExperimento) -> str:
        return (
            f"{resultado.n:>{ANCHO_N}} "
            f"{resultado.pi_estimado:>{ANCHO_NUM}.6f} "
            f"{resultado.error_absoluto:>{ANCHO_NUM}.6f} "
            f"{resultado.tiempo_segundos:>{ANCHO_NUM}.4f}"
        )


class ExportadorCsv:
    """Writes results to a CSV file with the schema shared with the Java run."""

    COLUMNAS = ("n", "aciertos", "pi_estimado", "error_absoluto", "tiempo_segundos")

    @classmethod
    def guardar(
        cls, resultados: list[ResultadoExperimento], ruta: str | Path
    ) -> Path:
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(cls.COLUMNAS)
            for r in resultados:
                escritor.writerow(
                    (
                        r.n,
                        r.aciertos,
                        f"{r.pi_estimado:.12f}",
                        f"{r.error_absoluto:.12f}",
                        f"{r.tiempo_segundos:.6f}",
                    )
                )
        return ruta


class GraficoErrores:
    """Renders the absolute error vs. sample size chart (requires matplotlib)."""

    @staticmethod
    def guardar(
        resultados: list[ResultadoExperimento], ruta: str | Path
    ) -> Path | None:
        try:
            import matplotlib
        except ImportError:
            print("Aviso: matplotlib no está instalado; se omite el gráfico.")
            return None
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ns = [r.n for r in resultados]
        errores = [r.error_absoluto for r in resultados]
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(ns, errores, marker="o", linewidth=1.5)
        ax.set_xscale("log")
        ax.set_xlabel("Tamaño de muestra N")
        ax.set_ylabel("Error absoluto")
        ax.set_title("Error absoluto de la estimación de pi (Monte Carlo)")
        ax.grid(True, which="both", linestyle="--", alpha=0.5)
        fig.tight_layout()
        fig.savefig(ruta, dpi=150)
        plt.close(fig)
        print(f"Gráfico guardado en {ruta}")
        return ruta
