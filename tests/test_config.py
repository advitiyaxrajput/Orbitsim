
import math

import pytest

from orbitsim.config import check_config, load_config


def write_config(tmp_path, text):
    """Write a temporary TOML configuration file."""
    path = tmp_path / "config.toml"
    path.write_text(text, encoding="utf-8")
    return path


def valid_config():
    """Return a fresh, valid configuration dictionary."""
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
            "method": "verlet",
            "steps_per_orbit": 100,
            "orbits": 1,
        },
    }


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        ("body", "mu", 0.0),
        ("body", "mu", -1.0),
        ("run", "h", 0.0),
        ("run", "h", -0.1),
        ("run", "T", 0.0),
        ("run", "T", -1.0),
        ("initial", "r0", [0.0, 0.0]),
        ("run", "method", "invalid_method"),
    ],
)
def test_invalid_config_values_raise_value_error(section, field, value):
    config = valid_config()

    # Supply h/T directly when testing those fields.
    if field == "h":
        config["run"].pop("steps_per_orbit")
    if field == "T":
        config["run"].pop("orbits")

    config[section][field] = value

    with pytest.raises(ValueError, match=field):
        check_config(config)


def test_initial_radius_must_be_outside_body():
    config = valid_config()
    config["body"]["R"] = 1.0
    config["initial"]["r0"] = [1.0, 0.0]

    with pytest.raises(ValueError, match="r0"):
        check_config(config)


def test_invalid_steps_per_orbit_raises_value_error():
    config = valid_config()
    config["run"]["steps_per_orbit"] = 0

    with pytest.raises(ValueError, match="steps_per_orbit"):
        check_config(config)


def test_both_step_size_options_raise_value_error():
    config = valid_config()
    config["run"]["h"] = 0.01

    with pytest.raises(ValueError):
        check_config(config)


def test_both_duration_options_raise_value_error():
    config = valid_config()
    config["run"]["T"] = 10.0

    with pytest.raises(ValueError):
        check_config(config)


def test_steps_per_orbit_converts_to_step_size():
    config = valid_config()
    result = check_config(config)

    expected_period = 2 * math.pi
    expected_h = expected_period / 100

    assert math.isclose(
        result["run"]["h"], expected_h, rel_tol=1e-12
    )
    assert "steps_per_orbit" not in result["run"]


def test_orbits_converts_to_total_time():
    config = valid_config()
    result = check_config(config)

    expected_period = 2 * math.pi

    assert math.isclose(
        result["run"]["T"], expected_period, rel_tol=1e-12
    )
    assert "orbits" not in result["run"]


def test_load_config_reads_toml_file(tmp_path):
    text = """
[body]
mu = 1.0
R = 0.1

[initial]
scenario = "circular"
r0 = [1.0, 0.0]

[run]
method = "verlet"
steps_per_orbit = 100
orbits = 1
"""
    path = write_config(tmp_path, text)

    config = load_config(path)

    assert config["body"]["mu"] == 1.0
    assert config["run"]["method"] == "verlet"
