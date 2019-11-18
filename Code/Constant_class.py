class Constants:
    def __init__(self, description, l, mu, n):
        self.description = description
        self.l = l
        self.rho = l / (n * mu)
        self.mu = mu
        self.n = n