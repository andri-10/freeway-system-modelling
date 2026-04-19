import numpy as np

def compute_flow(rho_up, rho_down, v, w, rho_max, ramp_flow):
    demand = max(0.0, v * rho_up)
    supply = max(0.0, w * (rho_max - rho_down) - ramp_flow)
    return min(demand, supply)

def update_density(rho_i, phi_in, phi_out, ramp_flow, T, L):
    rho_next = rho_i + (T / L) * (phi_in + ramp_flow - phi_out)
    return max(0.0, rho_next)

def update_queue(queue_i, demand_i, ramp_flow, T):
    queue_next = queue_i + T * (demand_i - ramp_flow)
    return max(0.0, queue_next)