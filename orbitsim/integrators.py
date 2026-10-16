import numpy as np

def euler(r, v, h, accel):
  r0 = np.asarray(r, dtype = np.float64)
  v0 = np.asarray(v, dtype = np.float64)
  absr = np.linalg.norm(r0)
  speed = np.linalg.norm(v0)
  a0 = accel(r0)
  r_next = r0 + h*v0
  v_next = v0 + h*a0
  return r_next, v_next

def verlet():
  pass

def rk4():
  pass
  