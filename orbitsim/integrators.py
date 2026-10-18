import numpy as np

def euler(r, v, h, accel):
  r0 = np.asarray(r, dtype = np.float64)
  v0 = np.asarray(v, dtype = np.float64)
  a0 = accel(r0)
  r_next = r0 + h*v0
  v_next = v0 + h*a0
  return r_next, v_next

def symplectic_euler(r, v, h, accel):
  r0 = np.asarray(r, dtype = np.float64)
  v0 = np.asarray(v, dtype = np.float64)
  a0 = accel(r0)
  v_next = v0 + h*a0
  r_next = r0 + h*v_next
  return r_next, v_next

def verlet(r, v, h, accel):
  r0 = np.asarray(r, dtype = np.float64)
  v0 = np.asarray(v, dtype = np.float64)
  a0 = accel(r0)
  r_next = r0 + h*v0 + 0.5*(h**2)*a0
  a_next = accel(r_next)
  v_next = v0 + 0.5*h*(a0+a_next)
  return r_next, v_next

def rk4(r, v, h, accel):
  r0 = np.asarray(r, dtype = np.float64)
  v0 = np.asarray(v, dtype = np.float64)
  
  k1_r, k1_v = v0, accel(r0)
  k2_r, k2_v = v0 + 0.5 * h * k1_v, accel(r0 + 0.5 * h * k1_r)
  k3_r, k3_v = v0 + 0.5 * h * k2_v, accel(r0 + 0.5 * h * k2_r)
  k4_r, k4_v = v0 + h * k3_v, accel(r0 + h * k3_r)

  r_next = r0 + (h/6)*(k1_r + 2*k2_r + 2*k3_r + k4_r)
  v_next = v0 + (h/6)*(k1_v + 2*k2_v + 2*k3_v +k4_v)

  return r_next, v_next
  
  