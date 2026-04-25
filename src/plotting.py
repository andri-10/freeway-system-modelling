import matplotlib.pyplot as plt
import numpy as np

def plot_density_heatmap(rho, output_path=None):
    plt.figure(figsize=(8, 4.5))
    plt.imshow(rho.T, aspect="auto", origin="lower")
    plt.colorbar(label="Density [veh/km]")
    plt.xlabel("Time step")
    plt.ylabel("Cell")
    plt.title("Density evolution")
    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.show()

def plot_all_queues(queue, ramp_cells, output_path=None):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(9, 5))

    for ramp_cell in ramp_cells:
        plt.plot(queue[:, ramp_cell], label=f"Ramp cell {ramp_cell + 1}")

    plt.xlabel("Time step")
    plt.ylabel("Queue [veh]")
    plt.title("Queue evolution at on-ramps")
    plt.legend()

    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")

    plt.show()

def plot_density_surface(rho, output_path=None):
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D  # needed for 3D plotting

    time_steps = np.arange(rho.shape[0])
    cells = np.arange(rho.shape[1])

    T_grid, C_grid = np.meshgrid(time_steps, cells)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(T_grid, C_grid, rho.T, cmap="viridis")

    ax.set_title("3D Density Evolution")
    ax.set_xlabel("Time step")
    ax.set_ylabel("Cell")
    ax.set_zlabel("Density [veh/km]")

    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")

    plt.show()

def plot_ramp_flows(ramp_flow, ramp_cells, output_path=None):
    plt.figure(figsize=(9, 5))
    for ramp_cell in ramp_cells:
        plt.plot(ramp_flow[:, ramp_cell], label=f"Ramp cell {ramp_cell + 1}")

    plt.xlabel("Time step")
    plt.ylabel("Ramp flow [veh/h]")
    plt.title("Ramp metering flows")
    plt.legend()

    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")

    plt.show()