from model.strategies import (
    BaseModelStrategy,
    AdjustedModelStrategy
)
from model.rain_model import RainModel
from controller.controller import SimulationController
from view.visualization import Visualization


def main():
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
        "Índice de lluvia - Modelo Base"
    )

    visualization.show_results(
        adjusted_results,
        "Índice de lluvia - Modelo Ajustado"
    )


def print_results(results):
    for result in results:
        print(
            f"{result['time']} | "
            f"H={result['humidity']:.2f} | "
            f"N={result['cloudiness']:.2f} | "
            f"Tf={result['temperature_factor']:.2f} | "
            f"I={result['index']:.3f} | "
            f"{result['state']}"
        )


if __name__ == "__main__":
    main()