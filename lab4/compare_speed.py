import timeit
import os
from lab4.rsa_handler import RSAHandler
from lab3.rc5_cbc import RC5CBCPad

def measure_rsa_encryption_time(data_size):
    rsa = RSAHandler()
    data = os.urandom(data_size)
    start = timeit.default_timer()
    encrypted = rsa.encrypt(data)
    end = timeit.default_timer()
    return end - start

def measure_rsa_decryption_time(data_size):
    rsa = RSAHandler()
    data = os.urandom(data_size)
    encrypted = rsa.encrypt(data)
    start = timeit.default_timer()
    decrypted = rsa.decrypt(encrypted)
    end = timeit.default_timer()
    return end - start

def measure_rc5_encryption_time(data_size):
    from hashlib import md5
    key = md5(b"DefaultKey").digest()
    rc5 = RC5CBCPad(key)
    data = os.urandom(data_size)
    iv = os.urandom(8)
    start = timeit.default_timer()
    encrypted = rc5.encrypt(data, iv)
    end = timeit.default_timer()
    return end - start

def measure_rc5_decryption_time(data_size):
    from hashlib import md5
    key = md5(b"DefaultKey").digest()
    rc5 = RC5CBCPad(key)
    data = os.urandom(data_size)
    iv = os.urandom(8)
    encrypted = rc5.encrypt(data, iv)
    start = timeit.default_timer()
    decrypted = rc5.decrypt(encrypted, iv)
    end = timeit.default_timer()
    return end - start

def compare_speeds():
    sizes = [128, 1024, 4096, 16384, 65536, 1048576]
    results = []

    for size in sizes:
        rsa_enc_time = measure_rsa_encryption_time(size)
        rsa_dec_time = measure_rsa_decryption_time(size)
        rc5_enc_time = measure_rc5_encryption_time(size)
        rc5_dec_time = measure_rc5_decryption_time(size)
        results.append((size, rsa_enc_time, rsa_dec_time, rc5_enc_time, rc5_dec_time))

    print(f"{'Data Size (bytes)':<20}{'RSA Encrypt (s)':<15}{'RSA Decrypt (s)':<15}{'RC5 Encrypt (s)':<15}{'RC5 Decrypt (s)':<15}")
    print("-" * 80)
    for size, rsa_enc, rsa_dec, rc5_enc, rc5_dec in results:
        print(f"{size:<20}{rsa_enc:<15.6f}{rsa_dec:<15.6f}{rc5_enc:<15.6f}{rc5_dec:<15.6f}")

if __name__ == "__main__":
    compare_speeds()
