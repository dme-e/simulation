"""Controller: orchestrates the experiment between the model and the views."""
from __future__ import annotations

from src.modelo import ExperimentoMonteCarlo, ResultadoExperimento
from src.vista import ExportadorCsv, GraficoErrores, VistaConsola

# Tamaños de muestra que pide la guía.
TAMANOS_DEFECTO = (1_000, 10_000, 100_000, 1_000_000)


class ExperimentoControlador:
    """Runs the experiment for each sample size and hands results to the views."""

    def __init__(
        self,
        modelo: ExperimentoMonteCarlo,
        vista: VistaConsola | None = None,
        tamanos: tuple[int, ...] = TAMANOS_DEFECTO,
    ) -> None:
        self.modelo = modelo
        self.vista = vista if vista is not None else VistaConsola()
        self.tamanos = tuple(tamanos)

    def ejecutar(self) -> list[ResultadoExperimento]:
        resultados: list[ResultadoExperimento] = []
        for n in self.tamanos:
            resultado = self.modelo.ejecutar(n)
            resultados.append(resultado)
            self.vista.mostrar_fila(resultado)
        self.vista.mostrar_tabla(resultados)
        return resultados

    def exportar(
        self,
        resultados: list[ResultadoExperimento],
        ruta_csv: str,
        ruta_grafico: str | None = None,
    ) -> None:
        ruta = ExportadorCsv.guardar(resultados, ruta_csv)
        print(f"Resultados guardados en {ruta}")
        if ruta_grafico:
            GraficoErrores.guardar(resultados, ruta_grafico)
