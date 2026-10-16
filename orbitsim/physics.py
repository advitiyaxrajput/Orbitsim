import numpy as np

def accel(r, mu):
  r = np.asarray(r, dtype = np.float64)
  absr = np.linalg.norm(r)
  accel = -(mu*r)/(absr**3)
  return accel

def energy(r, v, mu):
  r = np.asarray(r, dtype = np.float64)
  absr = np.linalg.norm(r)
  
  v = np.asarray(v, dtype = np.float64)
  absv = np.linalg.norm(v)
  Ke = (absv**2)/2
  Pe = -mu/absr
  return Ke+Pe

def ang_mom(r, v):
  r = np.asarray(r, dtype = np.float64)
  v = np.asarray(v, dtype = np.float64)
  ang_mom = float(r[0]*v[1] - r[1]*v[0])
  return ang_mom

def circular_start(mu, r0):
  r = np.asarray([r0, 0], dtype=np.float64)
  speed = np.sqrt(mu/r0)
  v = np.array([0.0, speed], dtype=np.float64)
  return r, v

  
  