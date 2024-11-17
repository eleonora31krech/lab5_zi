from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet

from lab4.constants import RSA_PADDING_ALGORITHM, RSA_PUBLIC_EXPONENT, RSA_KEY_SIZE

RSA_PADDING = rsa_padding.OAEP(
    mgf=rsa_padding.MGF1(algorithm=RSA_PADDING_ALGORITHM),
    algorithm=RSA_PADDING_ALGORITHM,
    label=None
)
PRIVATE_KEY_FORMAT = serialization.PrivateFormat.PKCS8
PUBLIC_KEY_FORMAT = serialization.PublicFormat.SubjectPublicKeyInfo
PEM_ENCODING = serialization.Encoding.PEM

class RSAHandler:
    def __init__(self):
        self.private_key, self.public_key = self.generate_key()

    def generate_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=RSA_PUBLIC_EXPONENT,
            key_size=RSA_KEY_SIZE,
        )
        public_key = private_key.public_key()
        return private_key, public_key

    def save_keys(self, private_file, public_file):
        with open(private_file, 'wb') as priv_file:
            priv_file.write(self.private_key.private_bytes(
                encoding=PEM_ENCODING,
                format=PRIVATE_KEY_FORMAT,
                encryption_algorithm=serialization.NoEncryption()
            ))
        with open(public_file, 'wb') as pub_file:
            pub_file.write(self.public_key.public_bytes(
                encoding=PEM_ENCODING,
                format=PUBLIC_KEY_FORMAT
            ))

    def load_keys(self, private_file, public_file):
        with open(private_file, 'rb') as priv_file:
            self.private_key = serialization.load_pem_private_key(
                priv_file.read(),
                password=None,
            )
        with open(public_file, 'rb') as pub_file:
            self.public_key = serialization.load_pem_public_key(pub_file.read())

    def encrypt(self, plaintext):
        aes_key = Fernet.generate_key()
        f = Fernet(aes_key)
        ciphertext = f.encrypt(plaintext)

        encrypted_aes_key = self.public_key.encrypt(
            aes_key,
            RSA_PADDING
        )
        return encrypted_aes_key + ciphertext

    def decrypt(self, encrypted):
        encrypted_aes_key, ciphertext = encrypted[:256], encrypted[256:]
        aes_key = self.private_key.decrypt(
            encrypted_aes_key,
            RSA_PADDING
        )
        f = Fernet(aes_key)
        return f.decrypt(ciphertext)
