import numpy as np
import time
from .config import check_config
from .physics import accel, circular_start, elliptical_start
from .integrators import euler, symplectic_euler, verlet, rk4

METHODS = {"euler": euler, "symplectic_euler": symplectic_euler, "verlet": verlet, "rk4":rk4}

def pick_method(name):
  if name not in METHODS:
    raise ValueError(f"got method {name} which isn't in the available methods")
  return METHODS[name];

def run_simulation(config):
  config = check_config(config) #check the config if values entered are correct

  #retrieve values
  mu = config["body"]["mu"]
  run = config["run"]

  h = run["h"]
  T = run["T"]
  name = run["method"]
  method = pick_method(name)

  #obtain number of rounds and correct step size
  N = round(T / h)
  if N < 1:
      raise ValueError("Simulation must have at least one step")
  h = T / N

  #initiallise the initial state
  initial = config["initial"]
  scenario = initial["scenario"]

  if scenario == "circular":
    r_init = np.linalg.norm(initial["r0"])
    r, v = circular_start(mu, r_init)
  elif scenario == "elliptical":
    rp = initial["rp"]
    e = initial["e"]
    r, v = elliptical_start(mu, rp, e)

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
    r, v = method(r, v, h, acceleration)
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
    "wall_time": wall_time,
    "T": T,
    "h": h,
    "N": N
  }
  
  