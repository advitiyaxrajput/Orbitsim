import numpy as np
import time
from .config import check_config
from .physics import accel, circular_start
from .integrators import euler

def run_simulation(config):
  config = check_config(config) #check the config if values entered are correct

  #retrieve values
  mu = config["body"]["mu"]
  r0 = config["initial"]["r0"]
  run = config["run"]

  h = run["h"]
  T = run["T"]
  method = run["method"]

  #obtain number of rounds and correct step size
  N = round(T / h)
  if N < 1:
      raise ValueError("Simulation must have at least one step")
  h = T / N

  #initiallise the initial state
  r_init = np.linalg.norm(r0)
  r, v = circular_start(mu, r_init)

  #create arrays to store the future values recieved through the integrators
  positions = np.zeros((N+1, 2), dtype = np.float64)
  velocities = np.zeros((N+1, 2), dtype = np.float64)

  #set initial r0 and v0s. 
  positions[0] = r
  velocities[0] = v

  start = time.perf_counter()
  #define acceleration function for integrator
  def acceleration(pos):
    return accel(pos, mu)

  #create the time array for assiciating reocrd positions and velocity with corerseponding times
  t = np.linspace(0.0, T, N+1)

  #simulation loop
  for k in range(N):
    if method == "euler":
      r, v = euler(r, v, h, acceleration)
    elif method == "verlet":
      pass
    elif method == "rk4":
      pass
    positions[k+1] = r
    velocities[k+1] = v

  wall_time = time.perf_counter() - start
  save_every = run.get("save_every", 1)
  save_idx = list(range(0, N + 1, save_every))

  if save_idx[-1] != N:
    save_idx.append(N)
  
  return {
    "t": t[save_idx],
    "r": positions[save_idx],
    "v": velocities[save_idx],
    "wall_time": wall_time
  }
  
  