"""Unit tests for the rain simulation model and its collaborators."""

import pytest
import matplotlib.pyplot as plt

from src.model.temperature import get_temperature_factor
from src.model.strategies import BaseModelStrategy, AdjustedModelStrategy
from src.model.state_classifier import StateClassifier
from src.model.rain_model import RainModel
from src.controller.controller import SimulationController
from src.view.visualization import Visualization


class TestTemperatureFactor:
    def test_extreme_low_temperature(self):
        assert get_temperature_factor(-5) == 1.00

    def test_exact_lookup_values(self):
        assert get_temperature_factor(10) == 1.00
        assert get_temperature_factor(12) == 0.90
        assert get_temperature_factor(18) == 0.60
        assert get_temperature_factor(28) == 0.10

    def test_between_reference_values(self):
        # 11 °C falls in the [10, 12) bucket -> 1.00
        assert get_temperature_factor(11) == 1.00
        # 19 °C falls in the [18, 20) bucket -> 0.60
        assert get_temperature_factor(19) == 0.60

    def test_high_temperature(self):
        assert get_temperature_factor(35) == 0.10


class TestStrategies:
    def test_base_model_strategy(self):
        strategy = BaseModelStrategy()
        # h=0.9, n=0.8, tf=0.6 -> 0.5*0.9 + 0.3*0.8 + 0.2*0.6 = 0.81
        assert strategy.calculate_index(0.9, 0.8, 0.6) == pytest.approx(0.81)

    def test_adjusted_model_strategy(self):
        strategy = AdjustedModelStrategy()
        # h=0.9, n=0.8, tf=0.6 -> 0.4*0.9 + 0.4*0.8 + 0.2*0.6 = 0.80
        assert strategy.calculate_index(0.9, 0.8, 0.6) == pytest.approx(0.80)


class TestStateClassifier:
    def test_rain_states(self):
        classifier = StateClassifier()
        assert classifier.classify(0.39) == "Sin lluvia"
        assert classifier.classify(0.40) == "Baja posibilidad"
        assert classifier.classify(0.59) == "Baja posibilidad"
        assert classifier.classify(0.60) == "Lluvia probable"
        assert classifier.classify(0.74) == "Lluvia probable"
        assert classifier.classify(0.75) == "Lluvia"
        assert classifier.classify(0.90) == "Lluvia"


class TestRainModel:
    def test_calculate_guide_example(self):
        # Example from the guide: H=90%, N=80%, T=18 °C -> I=0.81
        model = RainModel(BaseModelStrategy())
        result = model.calculate(90, 80, 18)

        assert result["humidity"] == pytest.approx(0.90)
        assert result["cloudiness"] == pytest.approx(0.80)
        assert result["temperature_factor"] == pytest.approx(0.60)
        assert result["index"] == pytest.approx(0.81)
        assert result["state"] == "Lluvia"

    def test_calculate_with_adjusted_strategy(self):
        model = RainModel(AdjustedModelStrategy())
        result = model.calculate(90, 80, 18)
        assert result["index"] == pytest.approx(0.80)
        assert result["state"] == "Lluvia"

    @pytest.mark.parametrize(
        "humidity,cloudiness,temperature,expected_exception",
        [
            (-1, 50, 20, ValueError),
            (101, 50, 20, ValueError),
            (50, -5, 20, ValueError),
            (50, 105, 20, ValueError),
            (50, 50, "hot", TypeError),
            ("high", 50, 20, TypeError),
        ],
    )
    def test_invalid_inputs(
        self, humidity, cloudiness, temperature, expected_exception
    ):
        model = RainModel(BaseModelStrategy())
        with pytest.raises(expected_exception):
            model.calculate(humidity, cloudiness, temperature)


class TestSimulationController:
    def test_run_returns_ordered_results(self):
        model = RainModel(BaseModelStrategy())
        controller = SimulationController(model)
        results = controller.run()

        assert len(results) == 9
        assert results[0]["time"] == "06:00"
        assert results[-1]["time"] == "22:00"
        assert all("index" in r and "state" in r for r in results)


class TestVisualization:
    def test_show_results_draws_on_supplied_axes(self):
        fig, ax = plt.subplots()
        visualization = Visualization()
        returned_fig = visualization.show_results(
            [
                {"time": "06:00", "index": 0.3},
                {"time": "08:00", "index": 0.7},
            ],
            "Test chart",
            ax=ax,
        )

        assert returned_fig is fig
        # One data line plus one threshold line for each of the 3 thresholds.
        assert len(ax.lines) == 4

    def test_show_results_saves_to_file(self, tmp_path):
        fig, ax = plt.subplots()
        visualization = Visualization()
        output = tmp_path / "chart.png"
        visualization.show_results(
            [{"time": "06:00", "index": 0.5}],
            "Saved chart",
            ax=ax,
            save_path=output,
        )

        assert output.exists()
