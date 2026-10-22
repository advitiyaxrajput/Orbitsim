
import math

import numpy as np

from orbitsim.simulation import run_simulation
from orbitsim.physics import energy


def make_config(method, orbits=10, steps_per_orbit=1000):
    """Build a canonical circular-orbit configuration."""
    return {
        "body": {
            "mu": 1.0,
            "R": 0.1,
        },
        "initial": {
            "scenario": "circular",
            "r0": [1.0, 0.0],
        },
        "run": {
            "method": method,
            "steps_per_orbit": steps_per_orbit,
            "orbits": orbits,
            "save_every": 1,
        },
    }


def specific_energy(r, v, mu=1.0):
    """Calculate specific orbital energy at each saved state."""
    r = np.asarray(r)
    v = np.asarray(v)
    return 0.5 * np.sum(v**2, axis=1) - mu / np.linalg.norm(r, axis=1)


def angular_momentum_z(r, v):
    """Calculate specific angular momentum about the z-axis."""
    return r[:, 0] * v[:, 1] - r[:, 1] * v[:, 0]


def relative_drift(values):
    """Return the absolute relative drift from the initial value."""
    initial = values[0]
    if initial == 0:
        raise ValueError("Initial value is zero; relative drift is undefined")
    return np.abs((values - initial) / initial)


def test_ac1_verlet_circular_orbit_radius_error():
    result = run_simulation(make_config("verlet"))

    radii = np.linalg.norm(result["r"], axis=1)
    max_relative_radius_error = np.max(np.abs(radii - radii[0])) / radii[0]

    assert max_relative_radius_error < 1e-3


def test_ac2_rk4_energy_and_angular_momentum_drift():
    result = run_simulation(make_config("rk4"))

    energies = specific_energy(result["r"], result["v"])
    angular_momenta = angular_momentum_z(result["r"], result["v"])

    max_energy_drift = np.max(relative_drift(energies))
    max_angular_momentum_drift = np.max(relative_drift(angular_momenta))

    assert max_energy_drift < 1e-6
    assert max_angular_momentum_drift < 1e-6


def test_ac3_symplectic_methods_conserve_angular_momentum():
    for method in ("symplectic_euler", "verlet"):
        result = run_simulation(make_config(method))

        angular_momenta = angular_momentum_z(
            result["r"], result["v"]
        )
        max_drift = np.max(relative_drift(angular_momenta))

        assert max_drift < 1e-12, (
            f"{method}: maximum relative angular-momentum drift "
            f"was {max_drift:.3e}"
        )


def test_ac4_symplectic_energy_error_is_bounded():
    errors = {}

    for method in ("symplectic_euler", "verlet"):
        result_10 = run_simulation(make_config(method, orbits=10))
        result_100 = run_simulation(make_config(method, orbits=100))

        energy_10 = specific_energy(result_10["r"], result_10["v"])
        energy_100 = specific_energy(result_100["r"], result_100["v"])

        errors[method] = (
            np.max(relative_drift(energy_100))
            / np.max(relative_drift(energy_10))
        )

    for method, ratio in errors.items():
        assert ratio < 2.0, (
            f"{method}: 100-orbit / 10-orbit maximum energy-error "
            f"ratio was {ratio:.3f}"
        )


def test_ac5_euler_energy_rises_and_radius_increases():
    result = run_simulation(make_config("euler"))

    energies = specific_energy(result["r"], result["v"])
    radii = np.linalg.norm(result["r"], axis=1)

    assert np.all(np.diff(energies) > 0), (
        "Euler's specific orbital energy should rise at every step"
    )
    assert radii[-1] > radii[0]
