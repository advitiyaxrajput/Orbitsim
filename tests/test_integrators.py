
import math

import numpy as np
import pytest

from orbitsim.physics import circular_start
from orbitsim.simulation import run_simulation


def circular_config(
    *,
    mu=1.0,
    r0=1.0,
    steps_per_orbit=100,
    orbits=1,
    save_every=1,
    method="rk4",
):
    """Build a valid circular-orbit simulation configuration."""
    return {
        "body": {
            "mu": mu,
            "R": 0.1,
        },
        "initial": {
            "scenario": "circular",
            "r0": [r0, 0.0],
        },
        "run": {
            "method": method,
            "steps_per_orbit": steps_per_orbit,
            "orbits": orbits,
            "save_every": save_every,
        },
    }


def test_circular_start_position_and_velocity():
    mu = 4.0
    radius = 2.0

    r, v = circular_start(mu, radius)

    assert np.allclose(r, [radius, 0.0])
    assert np.allclose(v, [0.0, math.sqrt(mu / radius)])


def test_circular_start_has_correct_radius_and_speed():
    mu = 4.0
    radius = 2.0

    r, v = circular_start(mu, radius)

    assert math.isclose(np.linalg.norm(r), radius)
    assert math.isclose(np.linalg.norm(v), math.sqrt(mu / radius))


def test_simulation_step_count_and_final_time():
    result = run_simulation(circular_config(steps_per_orbit=100))

    assert result["N"] == 100
    assert len(result["t"]) == 101
    assert math.isclose(result["t"][0], 0.0)
    assert math.isclose(result["t"][-1], result["T"])

def test_simulation_handles_non_whole_T_over_h():
    config = circular_config(steps_per_orbit=100)

    config["run"].pop("steps_per_orbit")
    config["run"].pop("orbits")

    config["run"]["h"] = 0.07
    config["run"]["T"] = 1.0

    result = run_simulation(config)

    assert result["N"] == 14
    assert len(result["t"]) == 15
    assert result["h"] == pytest.approx(1.0 / 14)
    assert result["t"][-1] == pytest.approx(1.0)

def test_save_every_controls_saved_rows():
    result = run_simulation(
        circular_config(steps_per_orbit=100, save_every=10)
    )

    # Indices 0, 10, 20, ..., 100 are saved.
    assert len(result["t"]) == 11
    assert result["r"].shape[0] == 11
    assert result["v"].shape[0] == 11


def test_final_state_is_near_initial_state_after_one_orbit():
    result = run_simulation(
        circular_config(
            mu=4.0,
            r0=1.0,
            steps_per_orbit=1000,
            orbits=1,
            method="rk4",
        )
    )

    assert np.allclose(result["r"][0], result["r"][-1], atol=1e-6)
    assert np.allclose(result["v"][0], result["v"][-1], atol=1e-6)


@pytest.mark.parametrize(
    "method",
    ["euler", "symplectic_euler", "verlet", "rk4"],
)
def test_each_integrator_runs(method):
    result = run_simulation(
        circular_config(steps_per_orbit=20, method=method)
    )

    assert result["r"].shape == (21, 2)
    assert result["v"].shape == (21, 2)
    assert np.all(np.isfinite(result["r"]))
    assert np.all(np.isfinite(result["v"]))
