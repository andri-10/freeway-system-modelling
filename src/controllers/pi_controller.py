class PIController:
    def __init__(self, Kp, Ki, rho_target, r_max):
        self.Kp = Kp
        self.Ki = Ki
        self.rho_target = rho_target
        self.r_max = r_max

        self.prev_error = 0.0
        self.r_prev = 0.0

    def compute(self, rho):
        error = self.rho_target - rho

        r = (
            self.r_prev
            + self.Kp * (error - self.prev_error)
            + self.Ki * error
        )

        self.prev_error = error
        self.r_prev = r

        return max(0.0, min(self.r_max, r))