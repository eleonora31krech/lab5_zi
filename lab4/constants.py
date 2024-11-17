from cryptography.hazmat.primitives import  hashes

RSA_KEY_SIZE = 2048  # Розмір ключа RSA
RSA_PUBLIC_EXPONENT = 65537  # Експонента
RSA_PADDING_ALGORITHM = hashes.SHA256()  # Алгоритм хешування для OAEP
FERNET_KEY_SIZE = 256  # Розмір ключа AES (Fernet)

# Константи для тестів
TEST_TEXT_DATA = b"Test message for encryption"
TEST_NUMERIC_DATA = b"12345678901234567890"
TEST_BINARY_DATA = b"\x00\x01\x02\x03\xFF\xFE\xFD\xFC"
LARGE_DATA_SIZE = 10**6  # 1 MB
VERY_LARGE_DATA_SIZE = 100 * 1024 * 1024  # 100 MB
PRIVATE_KEY_FILE = "private_test.pem"
PUBLIC_KEY_FILE = "public_test.pem"
TEST_INPUT_FILE_LARGE = "test_input_large.txt"
TEST_ENCRYPTED_FILE_LARGE = "test_encrypted_large.enc"
TEST_DECRYPTED_FILE_LARGE = "test_decrypted_large.txt"
TEST_INPUT_FILE_VERY_LARGE = "test_input_very_large.txt"
TEST_ENCRYPTED_FILE_VERY_LARGE = "test_encrypted_very_large.enc"
TEST_DECRYPTED_FILE_VERY_LARGE = "test_decrypted_very_large.txt"