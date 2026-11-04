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

def bound_status(r, v, mu):
  e = energy(r, v, mu)
  if e < 0:
    return "bound"
  return "unbound"

def period(t, x, y):
  t = np.asarray(t, dtype=np.float64)
  x = np.asarray(x, dtype=np.float64)
  y = np.asarray(y, dtype=np.float64)
  if len(t) != len(x) or len(t) != len(y):
    raise ValueError("t, x and y must have equal length")
  if len(t) < 2:
    return None
  crossing_times = []
  for i in range(len(t)-1):
    if y[i] <0 and y[i+1] >=0:
      fraction = -y[i] / (y[i+1]-y[i])
      crossing_time = t[i] + fraction * (t[i+1]-t[i])
      crossing_x = x[i] + fraction * (x[i+1]-x[i])
      if crossing_x >0:
        crossing_times.append(crossing_time)
  if len(crossing_times) <2:
    return None
  intervals = np.diff(crossing_times)
  return float(np.mean(intervals))
  