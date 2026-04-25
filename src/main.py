import argparse
import os

from scenario import build_parameters, build_scenario
from simulator import run_simulation

from controllers.linear_controller import LinearController
from controllers.pi_controller import PIController

from plotting import (
    plot_density_heatmap,
    plot_density_surface,
    plot_all_queues,
    plot_ramp_flows
)


def main():
    # ---- CLI arguments ----
    parser = argparse.ArgumentParser(description="Freeway simulation")
    parser.add_argument(
        "-m", "--mode",
        type=str,
        default="open",
        choices=["open", "linear", "pi"],
        help="Simulation mode"
    )
    args = parser.parse_args()
    mode = args.mode

    os.makedirs("results", exist_ok=True)

    params = build_parameters()
    scenario = build_scenario()

    
    if mode == "open":
        controllers = None

    elif mode == "linear":
        controllers = {
            cell: LinearController(
                K=20,
                rho_target=70,
                r_max=params["r_max"],
                r_base=400.0
            )
            for cell in params["ramp_cells"]
        }

    elif mode == "pi":
        controllers = {
            cell: PIController(
                Kp=20,
                Ki=1,
                rho_target=70,
                r_max=params["r_max"],
                r_base=400.0
            )
            for cell in params["ramp_cells"]
        }

    else:
        raise ValueError("Invalid mode selected")

    # ---- Run simulation ----
    results = run_simulation(params, scenario, controllers=controllers)

    suffix = mode

    # ---- Plot results ----
    plot_density_heatmap(
        results["rho"],
        output_path=f"results/density_{suffix}.png"
    )

    plot_density_surface(
        results["rho"],
        output_path=f"results/density_surface_{suffix}.png"
    )

    plot_all_queues(
        results["queue"],
        params["ramp_cells"],
        output_path=f"results/queues_{suffix}.png"
    )

    plot_ramp_flows(
        results["ramp_flow"],
        params["ramp_cells"],
        output_path=f"results/flows_{suffix}.png"
    )


if __name__ == "__main__":
    main()