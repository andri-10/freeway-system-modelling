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

def plot_queue(queue, ramp_cell, output_path=None):
    plt.figure(figsize=(8, 4.5))
    plt.plot(queue[:, ramp_cell])
    plt.xlabel("Time step")
    plt.ylabel("Queue [veh]")
    plt.title(f"Queue evolution at ramp cell {ramp_cell + 1}")
    if output_path:
        plt.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.show()