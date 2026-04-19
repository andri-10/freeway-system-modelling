import numpy as np
from actm import compute_flow, update_density, update_queue

def run_open_loop(params, scenario):
    N = params["N"]
    ramp_cell = params["ramp_cell"]
    T = params["T"]
    L = params["L"]
    v = params["v"]
    w = params["w"]
    rho_max = params["rho_max"]
    r_max = params["r_max"]

    K = scenario["num_steps"]
    upstream_demand = scenario["upstream_demand"]
    ramp_demand = scenario["ramp_demand"]

    rho = np.zeros((K + 1, N))
    queue = np.zeros((K + 1, N))
    ramp_flow = np.zeros((K, N))
    phi = np.zeros((K, N + 1))

    for k in range(K):
        # Ramp flow: unconstrained except by queue availability and max metering rate
        available_ramp = ramp_demand[k] + queue[k, ramp_cell] / T
        ramp_flow[k, ramp_cell] = min(r_max, max(0.0, available_ramp))

        # Boundary inflow from upstream
        phi[k, 0] = min(upstream_demand[k], w * (rho_max - rho[k, 0]))

        # Internal flows
        for i in range(1, N):
            r_i = ramp_flow[k, i]
            phi[k, i] = compute_flow(
                rho_up=rho[k, i - 1],
                rho_down=rho[k, i],
                v=v,
                w=w,
                rho_max=rho_max,
                ramp_flow=r_i,
            )

        # Outflow from last cell
        phi[k, N] = v * rho[k, N - 1]

        # Update states
        for i in range(N):
            r_i = ramp_flow[k, i]
            rho[k + 1, i] = update_density(
                rho_i=rho[k, i],
                phi_in=phi[k, i],
                phi_out=phi[k, i + 1],
                ramp_flow=r_i,
                T=T,
                L=L,
            )

            d_i = ramp_demand[k] if i == ramp_cell else 0.0
            queue[k + 1, i] = update_queue(
                queue_i=queue[k, i],
                demand_i=d_i,
                ramp_flow=r_i,
                T=T,
            )

            rho[k + 1, i] = min(rho[k + 1, i], rho_max)

    return {
        "rho": rho,
        "queue": queue,
        "ramp_flow": ramp_flow,
        "phi": phi,
        "time": scenario["time"],
    }