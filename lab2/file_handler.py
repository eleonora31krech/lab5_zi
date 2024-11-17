import os

from lab2.hash_validator import HashValidator


class FileHandler:

    @staticmethod
    def read_file(file_path: str, binary: bool = False) -> bytes:
        """Reads content from a file."""
        mode = 'rb' if binary else 'r'
        with open(file_path, mode) as file:
            return file.read()

    @staticmethod
    def save_file(content: str, file_path: str):
        """Saves content to a file."""
        with open(file_path, 'w') as file:
            file.write(content)

    @staticmethod
    def generate_large_file(file_path: str, size_in_mb: int):
        """Generates a file with specified size in MB."""
        with open(file_path, 'wb') as file:
            file.write(os.urandom(size_in_mb * 1024 * 1024))

    @staticmethod
    def md5_file(file_path: str) -> str:
        """Generates MD5 hash for a file."""
        content = FileHandler.read_file(file_path, binary=True)
        return HashValidator.md5(content)
