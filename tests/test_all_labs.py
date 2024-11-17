
import unittest
import numpy as np
from lab1.gcd import GCDUtils
from lab1.chebyshev import ChebyshevTest
from lab1.constants import LCG_MODULUS, LCG_MULTIPLIER, LCG_INCREMENT, LCG_SEED
from lab1.lcg import LCGGenerator

class TestGCDUtils(unittest.TestCase):
    def test_calculate_gcd_chunk(self):
        sequence = np.array([12, 15, 25, 35, 50])
        args = (sequence, 0)
        result = GCDUtils.calculate_gcd_chunk(args)
        self.assertEqual(result, 2)  # gcd(12, 15) == 3, gcd(12, 25) == 1, gcd(12, 35) == 1

class TestChebyshevTest(unittest.TestCase):
    def test_chebyshev_test_parallel(self):
        sequence = np.array([12, 15, 25, 35, 50])
        result = ChebyshevTest.chebyshev_test_parallel(sequence)
        self.assertTrue(result > 0)  # Valid pi estimate should be greater than 0.

class TestConstants(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(LCG_MODULUS, 2**18 - 1)
        self.assertEqual(LCG_MULTIPLIER, 53)
        self.assertEqual(LCG_INCREMENT, 34)
        self.assertEqual(LCG_SEED, 512)

class TestLCGGenerator(unittest.TestCase):
    def test_lcg_generator_numpy(self):
        generator = LCGGenerator(LCG_MODULUS, LCG_MULTIPLIER, LCG_INCREMENT, LCG_SEED)
        result = generator.lcg_generator_numpy(5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(result < LCG_MODULUS))

    def test_system_random_generator(self):
        result = LCGGenerator.system_random_generator(5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(result >= 0))

if __name__ == '__main__':
    unittest.main()