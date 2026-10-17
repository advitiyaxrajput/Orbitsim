import numpy as np
from .physics import energy, ang_mom

def results_energy(results, mu):
  e = np.array([
    energy(r, v, mu)
    for r, v in zip(results["r"], results["v"])
  ])
  return e

def energy_initial(results, mu):
  return float(results_energy(results, mu)[0])

def energy_drift(E):
  E0 = E[0]
  if E0 == 0:
    raise ValueError("Cannot caluclate relative energy drift when inital energy is 0")
  return np.abs(E-E0) / abs(E0)

def results_hz(results):
  hz = np.array([
    ang_mom(r, v)
    for r, v in zip(results["r"], results["v"])
  ])
  return hz

def hz_initial(results):
  return float(results_hz(results)[0])

def hz_drift(hz):
  h0 = hz[0]
  if h0 == 0:
    raise ValueError("Cannot caluclate relative angular momentum drift when inital angular momentum is 0")
  return np.abs(hz-h0) / abs(h0)
