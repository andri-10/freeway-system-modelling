import numpy as np

def build_scenario(num_steps=360):
    import numpy as np

    time = np.arange(num_steps)

    upstream_demand = np.full(num_steps, 1600.0)
    upstream_demand[80:240] = 2800.0
    upstream_demand[240:] = 1900.0

    ramp_demands = np.zeros((num_steps, 12))

    ramp_demands[60:240, 2] = 500.0
    ramp_demands[90:260, 5] = 700.0
    ramp_demands[120:280, 8] = 600.0

    # capacity / bottleneck factor per cell and time
    capacity_factor = np.ones((num_steps, 12))
    capacity_factor[140:230, 6:9] = 0.65   # incident or roadwork zone

    return {
        "num_steps": num_steps,
        "time": time,
        "upstream_demand": upstream_demand,
        "ramp_demands": ramp_demands,
        "capacity_factor": capacity_factor,
    }

def build_parameters():
    return {
        "N": 12,
        "ramp_cells": [2, 5, 8],   # zero-based: cells 3, 6, 9
        "T": 10.0 / 3600.0,
        "L": 0.5,
        "v": 100.0,
        "w": 20.0,
        "rho_max": 180.0,
        "r_max": 500.0,
    }