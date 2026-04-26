import numpy as np
from sklearn.ensemble import RandomForestRegressor

class DemandPredictor:
    def __init__(self, lookback=10, horizon=5):
        self.lookback = lookback
        self.horizon = horizon
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.trained = False

    def _make_features(self, demand_series):
        X, y = [], []
        for i in range(self.lookback, len(demand_series) - self.horizon):
            X.append(demand_series[i - self.lookback:i])
            y.append(demand_series[i + self.horizon])
        return np.array(X), np.array(y)

    def train(self, demand_series):
        X, y = self._make_features(demand_series)
        self.model.fit(X, y)
        self.trained = True

    def predict(self, recent_demand):
        if not self.trained:
            raise RuntimeError("Train the model before predicting.")
        x = np.array(recent_demand[-self.lookback:]).reshape(1, -1)
        return float(self.model.predict(x)[0])