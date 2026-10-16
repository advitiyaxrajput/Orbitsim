import tomllib
from pathlib import Path

def load_config(path: str | Path) -> dict:
    with open(path, "rb") as file:
        config = tomllib.load(file)
    return config


def check_config(config):
    import math
    s = dict(config)
    s["body"] = dict(s["body"])
    s["initial"] = dict(s["initial"])
    s["run"] = dict(s["run"])
    body = s["body"]
    initial = s["initial"]
    run = s["run"]
    mu = body["mu"]
    R = body["R"]
    r0 = initial["r0"]
    method = run["method"]
    if mu <= 0:
        raise ValueError(f"mu must be > 0, got {mu}")
    if R < 0:
        raise ValueError(f"R must be >= 0, got {R}")
    r0_mag = math.hypot(*r0) if isinstance(r0, list) else abs(r0)
    if r0_mag <= R:
        raise ValueError(f"r0 must have magnitude > R, got {r0_mag}")
    if method not in ("euler", "verlet", "rk4"):
        raise ValueError(f"unknown method: {method}")
    has_h = "h" in run
    has_steps = "steps_per_orbit" in run
    has_T = "T" in run
    has_orbits = "orbits" in run
    if has_h and has_steps:
        raise ValueError("Cannot provide both h and steps_per_orbit")
    if has_T and has_orbits:
        raise ValueError("Cannot provide both T and orbits")
    if has_h and run["h"] <= 0:
        raise ValueError(f"h must be > 0, got {run['h']}")
    if has_T and run["T"] <= 0:
        raise ValueError(f"T must be > 0, got {run['T']}")
    circular_period = 2 * math.pi * math.sqrt(r0_mag**3 / mu)
    if has_steps:
        if run["steps_per_orbit"] <= 0:
            raise ValueError("steps_per_orbit must be > 0")
        run["h"] = circular_period / run["steps_per_orbit"]
        del run["steps_per_orbit"]
    elif not has_h:
        raise ValueError("Missing h or steps_per_orbit")
    if has_orbits:
        if run["orbits"] <= 0:
            raise ValueError("orbits must be > 0")
        run["T"] = circular_period * run["orbits"]
        del run["orbits"]
    elif not has_T:
        raise ValueError("Missing T or orbits")
    return s