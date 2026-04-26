import numpy as np

from actm import compute_flow, update_density, update_queue


def run_simulation(params, scenario, controllers=None, predictor=None):
    N = params["N"]
    ramp_cells = params["ramp_cells"]
    T = params["T"]
    L = params["L"]
    v = params["v"]
    w = params["w"]
    rho_max = params["rho_max"]
    r_max = params["r_max"]

    K = scenario["num_steps"]
    upstream_demand = scenario["upstream_demand"]
    ramp_demands = scenario["ramp_demands"]
    capacity_factor = scenario["capacity_factor"]

    rho = np.zeros((K + 1, N))
    queue = np.zeros((K + 1, N))
    ramp_flow = np.zeros((K, N))
    phi = np.zeros((K, N + 1))

    for k in range(K):

        # Compute ramp flows for all ramp cells
        for ramp_cell in ramp_cells:
            available_ramp = ramp_demands[k, ramp_cell] + queue[k, ramp_cell] / T

            if controllers is None:
                r = min(r_max, available_ramp)

            else:
                rho_current = rho[k, ramp_cell]

                if predictor is not None and k >= predictor.lookback:
                    history = ramp_demands[
                        k - predictor.lookback:k,
                        ramp_cell
                    ]
                    predicted_demand = predictor.predict(history)
                else:
                    predicted_demand = None

                r_control = controllers[ramp_cell].compute(
                    rho_current,
                    predicted_demand
                )

                r = min(r_control, available_ramp)

            ramp_flow[k, ramp_cell] = max(0.0, min(r_max, r))

        # Upstream boundary flow
        effective_rho_max_0 = rho_max * capacity_factor[k, 0]
        phi[k, 0] = min(
            upstream_demand[k],
            w * (effective_rho_max_0 - rho[k, 0])
        )
        phi[k, 0] = max(0.0, phi[k, 0])

        # Internal flows
        for i in range(1, N):
            effective_rho_max = rho_max * capacity_factor[k, i]

            phi[k, i] = compute_flow(
                rho_up=rho[k, i - 1],
                rho_down=rho[k, i],
                v=v,
                w=w,
                rho_max=effective_rho_max,
                ramp_flow=ramp_flow[k, i],
            )

        # Downstream boundary outflow
        phi[k, N] = v * rho[k, N - 1]

        # Update states
        for i in range(N):
            rho[k + 1, i] = update_density(
                rho_i=rho[k, i],
                phi_in=phi[k, i],
                phi_out=phi[k, i + 1],
                ramp_flow=ramp_flow[k, i],
                T=T,
                L=L,
            )

            queue[k + 1, i] = update_queue(
                queue_i=queue[k, i],
                demand_i=ramp_demands[k, i],
                ramp_flow=ramp_flow[k, i],
                T=T,
            )

            rho[k + 1, i] = max(0.0, min(rho[k + 1, i], rho_max))
            queue[k + 1, i] = max(0.0, queue[k + 1, i])

    print("Max density:", rho.max())
    print("Max queue:", queue.max())
    print("Ramp flow sums:", ramp_flow[:, params["ramp_cells"]].sum(axis=0))

    return {
        "rho": rho,
        "queue": queue,
        "ramp_flow": ramp_flow,
        "phi": phi,
        "time": scenario["time"],
    }