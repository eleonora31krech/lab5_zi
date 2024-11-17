from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption

class KeyManager:
    @staticmethod
    def generate_keys(private_key_file='private_key.pem', public_key_file='public_key.pem'):
        private_key = dsa.generate_private_key(key_size=2048)
        public_key = private_key.public_key()

        with open(private_key_file, 'wb') as priv_file:
            priv_file.write(private_key.private_bytes(
                Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
            ))

        with open(public_key_file, 'wb') as pub_file:
            pub_file.write(public_key.public_bytes(
                Encoding.PEM, PublicFormat.SubjectPublicKeyInfo
            ))
        print(f"Keys saved to {private_key_file} and {public_key_file}.")
