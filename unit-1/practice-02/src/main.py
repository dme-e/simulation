"""Entry point for the population growth simulation practice.

Run with: python -m src.main
"""

from pathlib import Path

from src.model.config import DEFAULT_CONFIG
from src.controller.controller import SimulationController
from src.view.visualization import Visualization


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    controller = SimulationController(DEFAULT_CONFIG)
    results = controller.run_all()

    # Print small results table for each model at t=0 and t=final
    print("=" * 60)
    print("RESULTADOS: Población inicial (t=0) y final (t=6)")
    print("=" * 60)
    for model_name, model_results in results.items():
        inicial = model_results[0]["poblacion"]
        final = model_results[-1]["poblacion"]
        print(f"\n{model_name}:")
        print(f"  t=0   : {inicial:>10.2f}")
        print(f"  t=6   : {final:>10.2f}")

    # Also print real data for reference
    print("\nDatos reales:")
    print(f"  t=0   : {DEFAULT_CONFIG.DATOS[0]:>10.2f}")
    print(f"  t=6   : {DEFAULT_CONFIG.DATOS[-1]:>10.2f}")

    # Generate and save comparison chart
    visualization = Visualization()
    save_path = OUTPUT_DIR / "comparacion_modelos.png"
    visualization.show_comparison(results, DEFAULT_CONFIG, save_path=save_path)
    print(f"\nGráfica comparativa guardada en: {save_path}")


if __name__ == "__main__":
    main()

# Run command: python -m src.main