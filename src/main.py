import argparse
import os
import pickle

from scenario import build_parameters, build_scenario
from simulator import run_simulation

from controllers.linear_controller import LinearController
from controllers.pi_controller import PIController

from plotting import (
    plot_density_heatmap,
    plot_density_surface,
    plot_all_queues,
    plot_ramp_flows,
)


def main():
    parser = argparse.ArgumentParser(description="Freeway simulation")
    parser.add_argument(
        "-m", "--mode",
        type=str,
        default="open",
        choices=["open", "linear", "pi", "ai"],
        help="Simulation mode",
    )
    args = parser.parse_args()
    mode = args.mode

    os.makedirs("results", exist_ok=True)

    params = build_parameters()
    scenario = build_scenario()

    predictor = None

    if mode == "open":
        controllers = None

    elif mode == "linear":
        controllers = {
            cell: LinearController(
                K=20,
                rho_target=70,
                r_max=params["r_max"],
                r_base=400.0,
            )
            for cell in params["ramp_cells"]
        }

    elif mode == "pi":
        controllers = {
            cell: PIController(
                Kp=12,
                Ki=0.6,
                rho_target=70,
                r_max=params["r_max"],
                r_base=400.0,
                ai_enabled=False,
            )
            for cell in params["ramp_cells"]
        }

    elif mode == "ai":
        predictor_path = "results/metrics/predictor.pkl"

        if not os.path.exists(predictor_path):
            raise RuntimeError(
                "AI predictor not found. Run the training script first to generate "
                "results/metrics/predictor.pkl"
            )

        with open(predictor_path, "rb") as f:
            predictor = pickle.load(f)

        controllers = {
            cell: PIController(
                Kp=12,
                Ki=0.6,
                rho_target=70,
                r_max=params["r_max"],
                r_base=400.0,
                ai_enabled=True,
                demand_threshold=650.0,
                ai_gain=0.25,
            )
            for cell in params["ramp_cells"]
        }

    else:
        raise ValueError("Invalid mode selected")

    results = run_simulation(
        params,
        scenario,
        controllers=controllers,
        predictor=predictor,
    )

    suffix = mode

    plot_density_heatmap(
        results["rho"],
        output_path=f"results/density_{suffix}.png",
    )

    plot_density_surface(
        results["rho"],
        output_path=f"results/density_surface_{suffix}.png",
    )

    plot_all_queues(
        results["queue"],
        params["ramp_cells"],
        output_path=f"results/queues_{suffix}.png",
    )

    plot_ramp_flows(
        results["ramp_flow"],
        params["ramp_cells"],
        output_path=f"results/flows_{suffix}.png",
    )


if __name__ == "__main__":
    main()