
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives import hashes
import binascii

class Signer:
    @staticmethod
    def sign_message(message, private_key_file):
        """
        Signs a plain text message using the specified private key file.
        """
        with open(private_key_file, 'rb') as key_file:
            private_key = load_pem_private_key(key_file.read(), password=None)

        signature = private_key.sign(
            message.encode(),
            hashes.SHA256()
        )
        return binascii.hexlify(signature).decode()

    @staticmethod
    def sign_message_file(file_path, private_key_file):
        """
        Signs the contents of a file (any format) using the specified private key.
        """
        with open(private_key_file, 'rb') as key_file:
            private_key = load_pem_private_key(key_file.read(), password=None)

        with open(file_path, 'rb') as f:
            file_data = f.read()

        signature = private_key.sign(
            file_data,
            hashes.SHA256()
        )
        return binascii.hexlify(signature).decode()