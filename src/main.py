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

from metrics import compute_metrics, save_metrics_table


def build_controllers(mode, params):
    predictor = None

    if mode == "open":
        controllers = None

    elif mode == "linear":
        controllers = {
            cell: LinearController(
                K=20,
                rho_target=110,
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
                "AI predictor not found. Run the training script first."
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
        raise ValueError(f"Invalid mode: {mode}")

    return controllers, predictor


def run_mode(mode, params, scenario, save_plots=True):
    controllers, predictor = build_controllers(mode, params)

    results = run_simulation(
        params,
        scenario,
        controllers=controllers,
        predictor=predictor,
    )

    if save_plots:
        plot_density_heatmap(
            results["rho"],
            output_path=f"results/density_{mode}.png",
        )

        plot_density_surface(
            results["rho"],
            output_path=f"results/density_surface_{mode}.png",
        )

        plot_all_queues(
            results["queue"],
            params["ramp_cells"],
            output_path=f"results/queues_{mode}.png",
        )

        plot_ramp_flows(
            results["ramp_flow"],
            params["ramp_cells"],
            output_path=f"results/flows_{mode}.png",
        )

    return results


def main():
    parser = argparse.ArgumentParser(description="Freeway simulation")
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        default="open",
        choices=["open", "linear", "pi", "ai", "all"],
        help="Simulation mode",
    )
    args = parser.parse_args()

    os.makedirs("results", exist_ok=True)
    os.makedirs("results/metrics", exist_ok=True)

    params = build_parameters()
    scenario = build_scenario()

    if args.mode == "all":
        modes = ["open", "linear", "pi", "ai"]
        metrics_by_mode = {}

        for mode in modes:
            results = run_mode(mode, params, scenario, save_plots=True)
            metrics_by_mode[mode] = compute_metrics(results, params)

        df = save_metrics_table(
            metrics_by_mode,
            "results/metrics/comparison.csv",
        )

        print(df)

    else:
        results = run_mode(args.mode, params, scenario, save_plots=True)
        metrics = compute_metrics(results, params)

        print(f"\nMetrics for mode: {args.mode}")
        for key, value in metrics.items():
            print(f"{key}: {value:.3f}")


if __name__ == "__main__":
    main()