class PIController:
    def __init__(
        self,
        Kp,
        Ki,
        rho_target,
        r_max,
        r_base=300.0,
        ai_enabled=False,
        demand_threshold=650.0,
        ai_gain=0.15,
    ):
        self.Kp = Kp
        self.Ki = Ki
        self.rho_target = rho_target
        self.r_max = r_max
        self.ai_enabled = ai_enabled
        self.demand_threshold = demand_threshold
        self.ai_gain = ai_gain

        self.prev_error = 0.0
        self.r_prev = r_base

    def compute(self, rho, predicted_demand=None):
        error = self.rho_target - rho

        r = (
            self.r_prev
            + self.Kp * (error - self.prev_error)
            + self.Ki * error
        )

        # AI anticipation: if future demand is predicted high,
        # restrict ramp flow earlier.
        if self.ai_enabled and predicted_demand is not None:
            anticipation = max(0.0, predicted_demand - self.demand_threshold)
            r = r - self.ai_gain * anticipation

        r_sat = max(0.0, min(self.r_max, r))

        self.prev_error = error
        self.r_prev = r_sat

        return r_sat