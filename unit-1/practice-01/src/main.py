"""Entry point for the rain simulation practice."""

from pathlib import Path

from src.model.strategies import BaseModelStrategy, AdjustedModelStrategy
from src.model.rain_model import RainModel
from src.controller.controller import SimulationController
from src.view.visualization import Visualization


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Modelo base
    base_strategy = BaseModelStrategy()
    base_model = RainModel(base_strategy)
    base_controller = SimulationController(base_model)
    base_results = base_controller.run()

    print("MODELO BASE")
    print_results(base_results)

    # Modelo ajustado
    adjusted_strategy = AdjustedModelStrategy()
    adjusted_model = RainModel(adjusted_strategy)
    adjusted_controller = SimulationController(adjusted_model)
    adjusted_results = adjusted_controller.run()

    print("\nMODELO AJUSTADO")
    print_results(adjusted_results)

    # Gráficas
    visualization = Visualization()

    visualization.show_results(
        base_results,
        "Índice de lluvia - Modelo Base",
        save_path=OUTPUT_DIR / "rain_index_base.png",
    )
    print(f"\nGráfica base guardada en: {OUTPUT_DIR / 'rain_index_base.png'}")

    visualization.show_results(
        adjusted_results,
        "Índice de lluvia - Modelo Ajustado",
        save_path=OUTPUT_DIR / "rain_index_adjusted.png",
    )
    print(f"Gráfica ajustada guardada en: {OUTPUT_DIR / 'rain_index_adjusted.png'}")


def print_results(results: list[dict]) -> None:
    header = "Hora  |   H   |   N   |  Tf  |   I   | Estado"
    separator = "-" * len(header)
    print(header)
    print(separator)
    for result in results:
        print(
            f"{result['time']} | "
            f"{result['humidity']:.2f} | "
            f"{result['cloudiness']:.2f} | "
            f"{result['temperature_factor']:.2f} | "
            f"{result['index']:.3f} | "
            f"{result['state']}"
        )


if __name__ == "__main__":
    main()
