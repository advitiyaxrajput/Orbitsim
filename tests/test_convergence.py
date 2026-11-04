import math
import numpy as np
import pytest

from orbitsim.physics import accel, elliptical_start
from orbitsim.integrators import *

MU = 1.0
RP = 1.0
ECCENTRICITY = 0.5

A = RP / (1-ECCENTRICITY)
PERIOD = 2*math.pi*math.sqrt(A**3/MU)

END_TIME = 0.37*PERIOD
REFERENCE_STEPS = 200_000

METHODS = [
  (euler, [1000, 2000, 4000], 2),
  (symplectic_euler, [1000, 2000, 4000], 2),
  (verlet, [1000, 2000, 4000], 4),
  (rk4, [250, 500, 1000], 16)
]
def integrate(method, N):
  """Integrate the elliptical orbit for N steps."""

  r, v = elliptical_start(MU, RP, ECCENTRICITY)
  h = END_TIME/N

  def acceleration(pos):
    return accel(pos, MU)
  for _ in range(N):
    r, v = method(r, v, h, acceleration)
  return r

@pytest.fixture(scope="module")
def reference_position():
  """Calculate the high-accuracy RK4 reference position once"""
  return integrate(rk4, REFERENCE_STEPS)

def errors(method, counts, reference):
  """Calculate final position erros for each step count."""
  result = []
  for N in counts:
    final_position = integrate(method, N)
    error = np.linalg.norm(final_position - reference)
    result.append(error)
  return result
  
def ratios(errs):
  """Calculate the successive coarse-to-find error ratios"""
  return [
    errs[i]/errs[i+1]
    for i in range(len(errs)-1)
  ]

@pytest.mark.parametrize(
  "method, counts, target",
  METHODS,
  ids=["euler", "symplectic_euler", "verlet","rk4"]
)
def test_convergence(method, counts, target, reference_position):
  errs = errors(method, counts, reference_position)
  measured_ratios = ratios(errs)
  lower = target*0.85
  upper = target*1.15

  for ratio in measured_ratios:
    assert lower <= ratio <= upper, (
      f"Expected ratio near {target}, "
      f"but got {ratio:.4f}"
      f"Errors: {errs}"
    )