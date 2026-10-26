"""Visualization helpers for the rain simulation results."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.axes import Axes


class Visualization:
    """Render the rain index results as a line chart.

    The renderer can either draw on an externally supplied Axes (useful for
    tests), return a new Figure, or save the chart to a file.  It never blocks
    the process by default.
    """

    _THRESHOLDS = (
        (0.40, "Baja posibilidad"),
        (0.60, "Lluvia probable"),
        (0.75, "Lluvia"),
    )

    def show_results(
        self,
        results: list[dict],
        title: str,
        ax: Axes | None = None,
        save_path: Path | str | None = None,
    ) -> plt.Figure:
        """Plot the rain index over time.

        Args:
            results: List of result dictionaries produced by the model.
            title: Chart title.
            ax: Optional Axes to draw on. If omitted, a new figure is created.
            save_path: Optional path where the figure should be saved.

        Returns:
            The matplotlib Figure that was drawn.
        """
        own_figure = ax is None
        if own_figure:
            fig, ax = plt.subplots(figsize=(10, 5))
        else:
            fig = ax.figure

        times = [result["time"] for result in results]
        indexes = [result["index"] for result in results]

        ax.plot(times, indexes, marker="o")
        for threshold, label in self._THRESHOLDS:
            ax.axhline(threshold, linestyle="--", label=label)

        ax.set_title(title)
        ax.set_xlabel("Hora")
        ax.set_ylabel("Índice de lluvia")
        ax.set_ylim(0, 1)
        ax.grid(True)
        ax.legend()
        fig.tight_layout()

        if save_path is not None:
            fig.savefig(save_path)

        return fig
