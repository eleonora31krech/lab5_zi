import numpy as np

class GCDUtils:
    @staticmethod
    def calculate_gcd_chunk(args):
        sequence, i = args
        gcd_values = np.gcd(sequence[i], sequence[i + 1:])
        coprime_count = np.sum(gcd_values == 1)
        return coprime_count
