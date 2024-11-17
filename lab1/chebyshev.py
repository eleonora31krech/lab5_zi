from multiprocessing import Pool, cpu_count
import math
from lab1.gcd import GCDUtils

class ChebyshevTest:
    @staticmethod
    def chebyshev_test_parallel(sequence):
        total_pairs = len(sequence) * (len(sequence) - 1) // 2
        num_cores = cpu_count()

        with Pool(processes=num_cores) as pool:
            chunk_args = [(sequence, i) for i in range(len(sequence))]
            results = pool.map(GCDUtils.calculate_gcd_chunk, chunk_args)

        coprime_count = sum(results)
        if total_pairs == 0 or coprime_count == 0:
            return float('inf')

        pi_estimate = math.sqrt(6 / (coprime_count / total_pairs))
        return pi_estimate


