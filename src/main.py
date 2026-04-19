from scenario import build_parameters, build_scenario
from simulator import run_open_loop
from plotting import plot_density_heatmap, plot_queue

def main():
    params = build_parameters()
    scenario = build_scenario()
    results = run_open_loop(params, scenario)

    plot_density_heatmap(results["rho"], output_path="results/density_heatmap.png")
    plot_queue(results["queue"], params["ramp_cell"], output_path="results/queue_plot.png")

if __name__ == "__main__":
    main()