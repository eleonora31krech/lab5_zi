import numpy as np
import random

class LCGGenerator:
    def __init__(self, m, a, c, X0):
        self.m = m
        self.a = a
        self.c = c
        self.X0 = X0

    def lcg_generator_numpy(self, num_values):
        indices = np.arange(num_values)
        X = (self.a**indices * self.X0 + self.c * (self.a**indices - 1) // (self.a - 1)) % self.m
        return X.astype(np.uint64)

    @staticmethod
    def system_random_generator(num_values):
        return np.array([random.randint(0, 2**31 - 1) for _ in range(num_values)], dtype=np.uint64)
