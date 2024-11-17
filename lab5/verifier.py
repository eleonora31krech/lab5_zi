from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
import binascii


class Verifier:
    @staticmethod
    def verify_signature(message, signature_hex, public_key_file):
        """
        Verifies the signature for plain text.
        """
        with open(public_key_file, 'rb') as key_file:
            public_key = load_pem_public_key(key_file.read())

        signature = binascii.unhexlify(signature_hex)

        try:
            public_key.verify(
                signature,
                message.encode(),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    @staticmethod
    def verify_signature_file(file_path, signature_hex, public_key_file):
        """
        Verifies the signature of a file (any format) using the specified public key.
        """
        with open(public_key_file, 'rb') as key_file:
            public_key = load_pem_public_key(key_file.read())

        with open(file_path, 'rb') as f:
            file_data = f.read()

        signature = binascii.unhexlify(signature_hex)

        try:
            public_key.verify(
                signature,
                file_data,
                hashes.SHA256()
            )
            return True
        except Exception:
            return False