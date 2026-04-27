import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pickle
from ai.demand_predictor import DemandPredictor

def generate_training_data(n_profiles=50, num_steps=360):
    profiles = []
    rng = np.random.default_rng(42)
    for _ in range(n_profiles):
        base = rng.uniform(400, 700, num_steps)
        peak_start = int(rng.integers(60, 180))
        peak_len = int(rng.integers(60, 120))
        peak_height = rng.uniform(200, 500)
        base[peak_start:peak_start + peak_len] += peak_height
        profiles.append(base)
    return np.concatenate(profiles)

if __name__ == "__main__":
    os.makedirs("results/metrics", exist_ok=True)
    print("Generating training data...")
    demand_series = generate_training_data()
    print(f"Training on {len(demand_series)} samples...")
    predictor = DemandPredictor(lookback=10, horizon=15)
    predictor.train(demand_series)
    save_path = "results/metrics/predictor.pkl"
    with open(save_path, "wb") as f:
        pickle.dump(predictor, f)
    print(f"Model trained and saved to {save_path}")