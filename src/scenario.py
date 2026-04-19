import numpy as np

def build_scenario(num_steps=180):
    time = np.arange(num_steps)

    upstream_demand = np.full(num_steps, 1800.0)
    upstream_demand[60:120] = 2600.0

    ramp_demand = np.zeros(num_steps)
    ramp_demand[40:140] = 600.0

    return {
        "num_steps": num_steps,
        "time": time,
        "upstream_demand": upstream_demand,
        "ramp_demand": ramp_demand,
    }

def build_parameters():
    return {
        "N": 6,
        "ramp_cell": 2,      # zero-based index
        "T": 10.0 / 3600.0,  # 10 seconds in hours
        "L": 0.5,            # km
        "v": 100.0,          # km/h
        "w": 20.0,           # km/h
        "rho_max": 180.0,    # veh/km
        "r_max": 900.0,      # veh/h
    }