import argparse
import sys
import datetime as dt
import copy
from pathlib import Path
from orbitsim.config import load_config, check_config
from .simulation import run_simulation
from .diagnostics import results_energy, energy_drift
from .plotting import save_sim, drift_plot, orbit_plot, sweep_orbit_plot, sweep_drift_plot

def run_one(config, config_path):
  results = run_simulation(config)
  folder = save_sim(config, results, config_path)
  orbit_plot(results, folder / "orbit.png")
  drift_plot(config, results, folder / "drift.png")
  return results, folder

def run(config, config_path):
  run_one(config, config_path)

def sweep(config, config_path, n):
  base_h = config["run"]["h"]
  mu = config["body"]["mu"]
  step_sizes = [base_h / (2**i) for i in range(n)]
  sweep_results = []

  for h in step_sizes:
    run_config = copy.deepcopy(config)
    run_config["run"]["h"] = h
    results, folder = run_one(run_config, config_path)
    energy = results_energy(results, mu)
    final_drift = float(energy_drift(energy)[-1])
    sweep_results.append({
      "h": results["h"],
      "results": results,
      "final_energy_drift": final_drift,
    })
  timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
  sweep_folder = Path("runs") / f"sweep_{timestamp}"
  sweep_folder.mkdir(parents=True, exist_ok = False)
  sweep_orbit_plot(sweep_results, sweep_folder/"sweep_orbits.png")
  sweep_drift_plot(sweep_results, sweep_folder/"sweep_drift.png")

def main(argv=None):
  parser = argparse.ArgumentParser(prog = "orbitsim")
  sub = parser.add_subparsers(dest="command", required = True)

  run_parser = sub.add_parser("run", help="run one simulation")
  run_parser.add_argument("config")

  sweep_parser = sub.add_parser("sweep", help="run a parameter sweep")
  sweep_parser.add_argument("config")

  args = parser.parse_args(argv)

  try:
    config = check_config(load_config(args.config))
  except (ValueError, KeyError) as error:
    print(f"error: {error}", file=sys.stderr)
    return 1
  if args.command == "run":
    run(config, args.config)
  elif args.command == "sweep":
      sweep(config, args.config, 4)
  return 0

if __name__ == "__main__":
  sys.exit(main())

