import csv
import numpy as np
import datetime as dt
import json
import shutil
from pathlib import Path
import matplotlib 
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .diagnostics import *

def save_sim(config, results, config_path):
  when = dt.datetime.now()
  timestamp = when.strftime("%Y%m%d_%H%M%S")

  #retrieve values
  mu = config["body"]["mu"]
  run = config["run"]
  h = results["h"]
  T = results["T"]
  N = results["N"]
  if N < 1:
      raise ValueError("Simulation must have at least one step")
  
  method = run["method"]
  name = f"{timestamp}_{method}_h{h:.6g}"

  folder = Path("runs")/name
  folder.mkdir(parents=True, exist_ok=False)

  t = results["t"]
  r = results["r"]
  v = results["v"]
  rx = results["r"][:, 0]
  ry = results["r"][:, 1]
  vx = results["v"][:, 0]
  vy = results["v"][:, 1]
  measured_period = period(t, rx, ry)
  wall_time = results["wall_time"]
  e = results_energy(results, mu)
  e0 = float(energy_initial(results, mu))
  h_z = results_hz(results)
  h0 = float(hz_initial(results))
  e_drift = energy_drift(e)
  hz_drift_values = hz_drift(h_z)
  s = bound_status(r[0], v[0], mu)
  
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
    "measured_period": measured_period,
    "wall_time": wall_time,
    "status": s
  }
  with open(folder/"summary.json", "w") as fh:
    json.dump(summary, fh, indent=2)
  shutil.copyfile(config_path, folder / "config.toml")

  return folder
  
def orbit_plot(results, path):
  rx = results["r"][:, 0]
  ry = results["r"][:, 1]
  fig, ax = plt.subplots()
  ax.plot(rx, ry, label="position")
  ax.plot(0, 0, "o")
  ax.plot(rx[0], ry[0], "s")
  ax.set_xlabel("position X")
  ax.set_ylabel("position Y")
  ax.set_title("Trajectory")
  ax.set_aspect("equal")
  ax.legend()
  fig.savefig(path)
  plt.close(fig)
  return ax

def drift_plot(config, results, path):
  t = results["t"]
  T = results["T"]
  mu = config["body"]["mu"]
  time = t/T
  
  e = results_energy(results, mu)
  h_z = results_hz(results)
  
  e_drift = energy_drift(e)
  hz_drift_values = hz_drift(h_z)
  
  fig, ax = plt.subplots()
  ax.plot(time, e_drift, label="relative energy drift")
  ax.plot(time, hz_drift_values, label="relative h_z drift")
  ax.set_yscale("log")
  ax.set_ylabel("drift")
  ax.set_xlabel("time")
  ax.legend()
  fig.savefig(path)
  plt.close(fig)
  
  return ax

def sweep_orbit_plot(sweep_results, path):
  fig, ax = plt.subplots()
  for item in sweep_results:
    results = item["results"]
    rx = results["r"][:, 0]
    ry = results["r"][:, 1]
    h = item["h"]
    ax.plot(rx, ry, label=f"h = {h:.4g}")
  ax.plot(0, 0, "ko", label="central body")
  ax.set_xlabel("x")
  ax.set_ylabel("y")
  ax.set_title("Orbit comparison across sizes")
  ax.set_aspect("equal")
  ax.legend()

  fig.savefig(path)
  plt.close(fig)
  
def sweep_drift_plot(sweep_results, path):
  fig, ax = plt.subplots()
  step_sizes = [item["h"] for item in sweep_results]
  final_drifts = [
    item["final_energy_drift"] for item in sweep_results
  ]
  ax.loglog(step_sizes, final_drifts, "o-", label="final energy drift")
  ax.set_xlabel("step Size h")
  ax.set_ylabel("Final Relative Energy Drift")
  ax.set_title("Energy Drift vs Step Size")
  ax.legend()

  fig.savefig(path)
  plt.close(fig)