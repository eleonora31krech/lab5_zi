from lab2.hash_validator import HashValidator


def test_validate_hash():
    test_cases = [
        # Known input and expected hashes
        ("", "D41D8CD98F00B204E9800998ECF8427E", True),
        ("a", "0CC175B9C0F1B6A831C399E269772661", True),
        ("abc", "900150983CD24FB0D6963F7D28E17F72", True),
        ("wrong input", "900150983CD24FB0D6963F7D28E17F72", False),
        ("message digest", "F96B697D7CB7938D525A2F31AAF161D0", True),
        ("different message", "F96B697D7CB7938D525A2F31AAF161D0", False),
    ]

    for input_text, expected_hash, expected_result in test_cases:
        result = HashValidator.validate_hash(input_text, expected_hash)
        assert result == expected_result, f"Failed for input: {input_text}"
        print(f"Test passed for input: {input_text}")


test_validate_hash()
import unittest
from lab2.hash_validator import HashValidator

class TestHashValidator(unittest.TestCase):
    def setUp(self):
        self.hash_validator = HashValidator()
        self.input_text = b"Test message"
        self.empty_text = b""

    def test_validate_hash(self):
        """Test hash validation for a non-empty string."""
        file_hash = self.hash_validator.compute_hash(self.input_text)
        result = self.hash_validator.check_hash(self.input_text, file_hash)
        self.assertTrue(result)

    def test_empty_hash(self):
        """Test hash validation for an empty string."""
        file_hash = self.hash_validator.compute_hash(self.empty_text)
        result = self.hash_validator.check_hash(self.empty_text, file_hash)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
