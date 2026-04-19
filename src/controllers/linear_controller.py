class LinearController:
    def __init__(self, K, rho_target, r_max):
        self.K = K
        self.rho_target = rho_target
        self.r_max = r_max

    def compute(self, rho):
        error = self.rho_target - rho
        r = self.K * error
        return max(0.0, min(self.r_max, r))