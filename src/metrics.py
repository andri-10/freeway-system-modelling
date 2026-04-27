import pandas as pd


def compute_metrics(results, params):
    rho = results["rho"]
    queue = results["queue"]
    ramp_flow = results["ramp_flow"]

    T = params["T"]
    L = params["L"]
    ramp_cells = params["ramp_cells"]

    mainline_tts = T * L * rho[:-1, :].sum()
    queue_tts = T * queue[:-1, :].sum()
    total_tts = mainline_tts + queue_tts

    metrics = {
        "TTS [veh*h]": total_tts,
        "Mainline TTS [veh*h]": mainline_tts,
        "Queue TTS [veh*h]": queue_tts,
        "Max density [veh/km]": rho.max(),
        "Avg density [veh/km]": rho.mean(),
        "Max queue [veh]": queue[:, ramp_cells].max(),
        "Total queue [veh*h]": T * queue[:, ramp_cells].sum(),
        "Avg ramp flow [veh/h]": ramp_flow[:, ramp_cells].mean(),
    }

    return metrics


def save_metrics_table(metrics_by_mode, output_path):
    df = pd.DataFrame(metrics_by_mode).T
    df.to_csv(output_path)
    return df