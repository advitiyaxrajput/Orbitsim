import argparse
import sys
from orbitsim.config import load_config, check_config
from .simulation import run_simulation
from .plotting import save_sim

def main(argv=None):
  parser = argparse.ArgumentParser(prog = "orbitsim")
  sub = parser.add_subparsers(dest="command", required = True)

  run_parser = sub.add_parser("run", help="run one simulation")
  run_parser.add_argument("config")

  sweep_parser = sub.add_parser("sweep", help="run a parameter sweep")
  sweep_parser.add_argument("config")

  args = parser.parse_args(argv)

  try:
    config = load_config(args.config)
    config = check_config(config)
  except (ValueError, KeyError) as error:
    print(f"error: {error}", file=sys.stderr)
    return 1

  if args.command == "run":
    run = run_simulation(config)
    save = save_sim(config, run, args.config)
    return 0
  if args.command == "sweep":
    print("Sweep support will be added later in M9")
    return 0

if __name__ == "__main__":
  sys.exit(main())

