"""Unit tests for the population growth models and collaborators."""

import math
from unittest.mock import MagicMock

import matplotlib.pyplot as plt
import numpy as np
import pytest

from src.model.config import SimulationConfig, DEFAULT_CONFIG
from src.model.strategies import (
    DeterministicModel,
    DiscreteModel,
    StochasticModel,
    EulerContinuousModel,
)
from src.controller.controller import SimulationController
from src.view.visualization import Visualization


class TestSimulationConfig:
    def test_default_config_values(self):
        assert DEFAULT_CONFIG.P0 == 1000.0
        assert DEFAULT_CONFIG.r == 0.15
        assert DEFAULT_CONFIG.sigma == 20.0
        assert DEFAULT_CONFIG.dt == 0.1
        assert DEFAULT_CONFIG.tiempo == 6
        assert DEFAULT_CONFIG.DATOS == (1000, 1100, 1250, 1400, 1600, 1850, 2100)

    def test_config_validation_positive_P0(self):
        with pytest.raises(ValueError, match="P0 must be positive"):
            SimulationConfig(P0=0, r=0.1, sigma=10, dt=0.1, tiempo=5, DATOS=(100, 110, 120, 130, 140, 150))

    def test_config_validation_non_negative_r(self):
        with pytest.raises(ValueError, match="r must be non-negative"):
            SimulationConfig(P0=1000, r=-0.1, sigma=10, dt=0.1, tiempo=5, DATOS=(100, 110, 120, 130, 140, 150))

    def test_config_validation_non_negative_sigma(self):
        with pytest.raises(ValueError, match="sigma must be non-negative"):
            SimulationConfig(P0=1000, r=0.1, sigma=-10, dt=0.1, tiempo=5, DATOS=(100, 110, 120, 130, 140, 150))

    def test_config_validation_positive_dt(self):
        with pytest.raises(ValueError, match="dt must be positive"):
            SimulationConfig(P0=1000, r=0.1, sigma=10, dt=0, tiempo=5, DATOS=(100, 110, 120, 130, 140, 150))

    def test_config_validation_positive_tiempo(self):
        with pytest.raises(ValueError, match="tiempo must be positive"):
            SimulationConfig(P0=1000, r=0.1, sigma=10, dt=0.1, tiempo=0, DATOS=(100,))

    def test_config_validation_datos_length(self):
        with pytest.raises(ValueError, match="DATOS length"):
            SimulationConfig(P0=1000, r=0.1, sigma=10, dt=0.1, tiempo=5, DATOS=(100, 110))  # length 2 != 6


class TestDeterministicModel:
    def test_exact_values_at_integer_times(self):
        config = SimulationConfig(P0=1000.0, r=0.15, sigma=20.0, dt=0.1, tiempo=6, DATOS=(1000, 1100, 1250, 1400, 1600, 1850, 2100))
        model = DeterministicModel()
        results = model.run(config)

        assert len(results) == 7  # t=0 to t=6
        for i, result in enumerate(results):
            expected = 1000.0 * math.exp(0.15 * i)
            assert result["tiempo"] == float(i)
            assert result["poblacion"] == pytest.approx(expected, rel=1e-10)

    def test_t0_equals_P0(self):
        config = DEFAULT_CONFIG
        model = DeterministicModel()
        results = model.run(config)
        assert results[0]["poblacion"] == pytest.approx(1000.0)


class TestDiscreteModel:
    def test_recursion_formula(self):
        config = SimulationConfig(P0=1000.0, r=0.15, sigma=20.0, dt=0.1, tiempo=6, DATOS=(1000, 1100, 1250, 1400, 1600, 1850, 2100))
        model = DiscreteModel()
        results = model.run(config)

        assert len(results) == 7
        assert results[0]["poblacion"] == pytest.approx(1000.0)
        # P1 = P0 + r*P0 = 1000 + 150 = 1150
        assert results[1]["poblacion"] == pytest.approx(1150.0)
        # P2 = P1 + r*P1 = 1150 + 172.5 = 1322.5
        assert results[2]["poblacion"] == pytest.approx(1322.5)
        # Verify recursive formula holds for all steps
        for i in range(1, len(results)):
            prev = results[i-1]["poblacion"]
            expected = prev + config.r * prev
            assert results[i]["poblacion"] == pytest.approx(expected)


class TestStochasticModel:
    def test_non_negative_population(self):
        config = SimulationConfig(P0=1000.0, r=0.15, sigma=1000.0, dt=0.1, tiempo=6, DATOS=(1000, 1100, 1250, 1400, 1600, 1850, 2100))
        model = StochasticModel(seed=123)
        results = model.run(config)

        for result in results:
            assert result["poblacion"] >= 0, f"Population went negative: {result}"

    def test_seed_reproducibility(self):
        config = DEFAULT_CONFIG
        model1 = StochasticModel(seed=42)
        model2 = StochasticModel(seed=42)
        results1 = model1.run(config)
        results2 = model2.run(config)

        assert len(results1) == len(results2)
        for r1, r2 in zip(results1, results2):
            assert r1["poblacion"] == pytest.approx(r2["poblacion"])
            assert r1["tiempo"] == r2["tiempo"]

    def test_different_seeds_produce_different_results(self):
        config = DEFAULT_CONFIG
        model1 = StochasticModel(seed=1)
        model2 = StochasticModel(seed=2)
        results1 = model1.run(config)
        results2 = model2.run(config)

        # At least one population value should differ
        populations_differ = any(
            r1["poblacion"] != r2["poblacion"] for r1, r2 in zip(results1, results2)
        )
        assert populations_differ


class TestEulerContinuousModel:
    def test_step_formula(self):
        config = SimulationConfig(P0=1000.0, r=0.15, sigma=20.0, dt=0.1, tiempo=6, DATOS=(1000, 1100, 1250, 1400, 1600, 1850, 2100))
        model = EulerContinuousModel()
        results = model.run(config)

        # First step: t=0 -> t=0.1
        # P(0.1) = P0 + dt * r * P0 = 1000 + 0.1 * 0.15 * 1000 = 1015
        assert results[0]["poblacion"] == pytest.approx(1000.0)
        assert results[1]["tiempo"] == pytest.approx(0.1)
        assert results[1]["poblacion"] == pytest.approx(1015.0)

        # Second step: t=0.1 -> t=0.2
        # P(0.2) = 1015 + 0.1 * 0.15 * 1015 = 1030.225
        assert results[2]["tiempo"] == pytest.approx(0.2)
        assert results[2]["poblacion"] == pytest.approx(1030.225)

    def test_final_time_equals_tiempo(self):
        config = DEFAULT_CONFIG
        model = EulerContinuousModel()
        results = model.run(config)

        # Last time point should be approximately tiempo (6.0)
        assert results[-1]["tiempo"] == pytest.approx(config.tiempo, abs=1e-9)

    def test_number_of_steps(self):
        config = DEFAULT_CONFIG
        model = EulerContinuousModel()
        results = model.run(config)

        # With dt=0.1 and tiempo=6, we expect 6/0.1 + 1 = 61 points
        expected_steps = int(config.tiempo / config.dt) + 1
        assert len(results) == expected_steps


class TestSimulationController:
    def test_run_all_returns_four_labeled_results(self):
        controller = SimulationController(DEFAULT_CONFIG)
        results = controller.run_all()

        expected_names = ["Determinista", "Discreto", "Estocástico", "Continuo (Euler)"]
        assert list(results.keys()) == expected_names
        assert all(isinstance(v, list) for v in results.values())
        assert all(len(v) > 0 for v in results.values())

    def test_get_model_names(self):
        controller = SimulationController(DEFAULT_CONFIG)
        names = controller.get_model_names()
        assert names == ["Determinista", "Discreto", "Estocástico", "Continuo (Euler)"]


class TestVisualization:
    def test_show_comparison_draws_on_supplied_axes(self):
        fig, ax = plt.subplots()
        visualization = Visualization()

        # Create mock results
        mock_results = {
            "Determinista": [{"tiempo": 0.0, "poblacion": 1000}, {"tiempo": 1.0, "poblacion": 1150}],
            "Discreto": [{"tiempo": 0.0, "poblacion": 1000}, {"tiempo": 1.0, "poblacion": 1150}],
            "Estocástico": [{"tiempo": 0.0, "poblacion": 1000}, {"tiempo": 1.0, "poblacion": 1170}],
            "Continuo (Euler)": [{"tiempo": 0.0, "poblacion": 1000}, {"tiempo": 0.1, "poblacion": 1015}],
        }

        returned_fig = visualization.show_comparison(mock_results, DEFAULT_CONFIG, ax=ax)

        assert returned_fig is fig
        # 4 model lines + 1 scatter plot for real data = 5 artists with data
        # Actually scatter creates a PathCollection, not a Line2D
        lines = [artist for artist in ax.get_children() if hasattr(artist, 'get_ydata')]
        # We have 4 model lines
        line_count = sum(1 for artist in ax.get_children() if isinstance(artist, plt.Line2D))
        assert line_count == 4

    def test_show_comparison_saves_to_file(self, tmp_path):
        fig, ax = plt.subplots()
        visualization = Visualization()

        mock_results = {
            "Determinista": [{"tiempo": 0.0, "poblacion": 1000}],
            "Discreto": [{"tiempo": 0.0, "poblacion": 1000}],
            "Estocástico": [{"tiempo": 0.0, "poblacion": 1000}],
            "Continuo (Euler)": [{"tiempo": 0.0, "poblacion": 1000}],
        }

        output = tmp_path / "chart.png"
        visualization.show_comparison(mock_results, DEFAULT_CONFIG, ax=ax, save_path=output)

        assert output.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])