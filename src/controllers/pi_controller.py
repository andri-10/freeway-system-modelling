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

        proactive_r_max = self.r_max
        if predicted_demand is not None and predicted_demand > 550.0:
            scale = max(0.85, 1.0 - (predicted_demand - 550.0) / 4000.0)
            proactive_r_max = self.r_max * scale

        r = (
            self.r_prev
            + self.Kp * (error - self.prev_error)
            + self.Ki * error
        )
        r_sat = max(0.0, min(proactive_r_max, r))
        self.prev_error = error
        self.r_prev = r_sat
        return r_sat