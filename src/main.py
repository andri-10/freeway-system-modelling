from scenario import build_parameters, build_scenario
from simulator import run_simulation
from controllers.linear_controller import LinearController
from controllers.pi_controller import PIController
from plotting import plot_density_heatmap, plot_queue
import os
os.makedirs("results", exist_ok=True)

def main():
    params = build_parameters()
    scenario = build_scenario()

    mode = "pi"   # options: "open", "linear", "pi"

    if mode == "open":
        controller = None

    elif mode == "linear":
        controller = LinearController(
            K=50,
            rho_target=30,
            r_max=params["r_max"]
        )

    elif mode == "pi":
        controller = PIController(
            Kp=50,
            Ki=5,
            rho_target=30,
            r_max=params["r_max"]
        )

    else:
        raise ValueError("Invalid mode selected")

    results = run_simulation(params, scenario, controller=controller)
    suffix = mode

    plot_density_heatmap(
        results["rho"],
        output_path=f"results/density_{suffix}.png"
    )

    plot_queue(
        results["queue"],
        params["ramp_cell"],
        output_path=f"results/queue_{suffix}.png"
    )


if __name__ == "__main__":
    main()