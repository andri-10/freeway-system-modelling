class PIController:
    def __init__(self, Kp, Ki, rho_target, r_max, r_base=300.0):
        self.Kp = Kp
        self.Ki = Ki
        self.rho_target = rho_target
        self.r_max = r_max

        self.prev_error = 0.0
        self.r_prev = r_base

    def compute(self, rho, predicted_demand=None):
        error = self.rho_target - rho

        # if prediction available and demand is rising, tighten control
        if predicted_demand is not None:
            anticipation = max(0.0, predicted_demand - 500.0)
            error = error - min(0.005 * anticipation, 20.0)

        r = (
            self.r_prev
            + self.Kp * (error - self.prev_error)
            + self.Ki * error
        )
        r_sat = max(0.0, min(self.r_max, r))
        self.prev_error = error
        self.r_prev = r_sat
        return r_sat