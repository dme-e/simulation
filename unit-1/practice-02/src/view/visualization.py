"""Visualization for population growth model comparison."""

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from src.model.config import SimulationConfig


class Visualization:
    """Render comparison of population growth models.

    The renderer can draw on an externally supplied Axes (useful for tests),
    return a new Figure, or save the chart to a file. It never blocks
    the process by default.
    """

    _MODEL_STYLES = {
        "Determinista": {"color": "blue", "linestyle": "-", "marker": "o"},
        "Discreto": {"color": "green", "linestyle": "--", "marker": "s"},
        "Estocástico": {"color": "red", "linestyle": ":", "marker": "^"},
        "Continuo (Euler)": {"color": "orange", "linestyle": "-.", "marker": "D"},
    }

    def show_comparison(
        self,
        results: dict[str, list[dict[str, float]]],
        config: SimulationConfig,
        ax: Axes | None = None,
        save_path: Path | str | None = None,
    ) -> plt.Figure:
        """Plot all four model series plus real data points.

        Args:
            results: Dictionary mapping model names to their result lists.
            config: Simulation configuration (provides real DATOS).
            ax: Optional Axes to draw on. If omitted, a new figure is created.
            save_path: Optional path where the figure should be saved.

        Returns:
            The matplotlib Figure that was drawn.
        """
        own_figure = ax is None
        if own_figure:
            fig, ax = plt.subplots(figsize=(10, 6))
        else:
            fig = ax.figure

        # Plot each model's results
        for model_name, model_results in results.items():
            style = self._MODEL_STYLES.get(model_name, {})
            tiempos = [r["tiempo"] for r in model_results]
            poblaciones = [r["poblacion"] for r in model_results]
            ax.plot(tiempos, poblaciones, label=model_name, **style)

        # Plot real data points
        tiempos_reales = list(range(len(config.DATOS)))
        ax.scatter(
            tiempos_reales,
            config.DATOS,
            color="black",
            zorder=5,
            label="Datos reales",
            marker="x",
            s=100,
        )

        ax.set_title("Comparación de Modelos de Crecimiento Poblacional")
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Población")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()

        if save_path is not None:
            fig.savefig(save_path, dpi=150)

        return fig