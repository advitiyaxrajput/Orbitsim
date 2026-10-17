import csv
import numpy as np
import datetime as dt
import json
import shutil
from pathlib import Path
from .diagnostics import results_energy, energy_initial, energy_drift, results_hz, hz_initial, hz_drift

def save_sim(config, results, config_path):
  when = dt.datetime.now()
  timestamp = when.strftime("%Y%m%d_%H%M%S")

  #retrieve values
  mu = config["body"]["mu"]
  r0 = config["initial"]["r0"]
  run = config["run"]
  h = run["h"]
  T = run["T"]
  
  #obtain number of rounds and correct step size
  N = round(T / h)
  if N < 1:
      raise ValueError("Simulation must have at least one step")
  h = T / N
  
  method = run["method"]
  name = f"{timestamp}_{method}_h{h:.6g}"

  folder = Path("runs")/name
  folder.mkdir(parents=True, exist_ok=False)

  t = results["t"]
  rx = results["r"][:, 0]
  ry = results["r"][:, 1]
  vx = results["v"][:, 0]
  vy = results["v"][:, 1]
  wall_time = results["wall_time"]
  e = results_energy(results, mu)
  e0 = float(energy_initial(results, mu))
  h_z = results_hz(results)
  h0 = float(hz_initial(results))
  e_drift = energy_drift(e)
  hz_drift_values = hz_drift(h_z)
  
  final_energy_drift = float(e_drift[-1])
  max_energy_drift = float(np.max(e_drift))
  
  final_hz_drift = float(hz_drift_values[-1])
  max_hz_drift = float(np.max(hz_drift_values))

  with open(folder/"trajectory.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["t", "x", "y", "vx", "vy", "energy", "h_z"])
    w.writerows(zip(t, rx, ry, vx, vy, e, h_z))
  summary = {
    "method": method,
    "h": h,
    "N": N,
    "e0": e0,
    "h0": h0,
    "final_energy_drift": final_energy_drift,
    "max_energy_drift": max_energy_drift,
    "final_hz_drift": final_hz_drift,
    "max_hz_drift": max_hz_drift,
    "wall_time": wall_time,
  }
  with open(folder/"summary.json", "w") as fh:
    json.dump(summary, fh, indent=2)
  shutil.copyfile(config_path, folder / "config.toml")

  return folder
  
  

  
  

  