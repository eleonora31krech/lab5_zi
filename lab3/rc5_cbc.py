import os
import struct

from lab3.constants import WORD_SIZE, NUM_ROUNDS, BLOCK_SIZE, P_CONST, Q_CONST


class RC5CBCPad:
    def __init__(self, key, word_size=WORD_SIZE, num_rounds=NUM_ROUNDS):
        self.block_size = BLOCK_SIZE
        self.word_size = word_size
        self.num_rounds = num_rounds
        self.key = self._pad_key(key, self.block_size)

    def _pad_key(self, key, block_size):
        key_len = len(key)
        if key_len >= block_size:
            return key[:block_size]
        else:
            return key + b'\x00' * (block_size - key_len)

    def _xor_bytes(self, a, b):
        return bytes(x ^ y for x, y in zip(a, b))

    def _pad_data(self, data):
        padding_len = self.block_size - len(data) % self.block_size
        padding = bytes([padding_len] * padding_len)
        return data + padding

    def _unpad_data(self, data):
        padding_len = data[-1]
        if padding_len < 1 or padding_len > self.block_size:
            raise ValueError("Invalid padding")
        if data[-padding_len:] != bytes([padding_len] * padding_len):
            raise ValueError("Invalid padding")
        unpadded_data = data[:-padding_len]

        return unpadded_data

    def _split_blocks(self, data):
        return [data[i:i + self.block_size] for i in range(0, len(data), self.block_size)]

    def encrypt(self, plaintext, iv):
        plaintext = self._pad_data(plaintext)
        blocks = self._split_blocks(plaintext)
        ciphertext = b''
        prev_block = iv
        for block in blocks:
            block = self._xor_bytes(block, prev_block)
            cipher = self._rc5_encrypt_block(block)
            ciphertext += cipher
            prev_block = cipher
        return iv + ciphertext

    def decrypt(self, ciphertext, iv):
        blocks = self._split_blocks(ciphertext)
        plaintext = b''
        prev_block = iv

        for block in blocks:
            decrypted_block = self._rc5_decrypt_block(block)
            plaintext += self._xor_bytes(decrypted_block, prev_block)
            prev_block = block

        plaintext = self._unpad_data(plaintext)
        return plaintext

    def _rc5_encrypt_block(self, block):
        A, B, C, D = struct.unpack('!HHHH', block)
        round_keys = self._expand_key()
        for i in range(self.num_rounds):
            A = (A + round_keys[2 * i]) & ((1 << self.word_size) - 1)
            B = (B + round_keys[2 * i + 1]) & ((1 << self.word_size) - 1)
            A ^= B

            A = (A << (B % self.word_size)) | (A >> (self.word_size - (B % self.word_size)))
            A &= ((1 << self.word_size) - 1)
            C = (C + round_keys[2 * i]) & ((1 << self.word_size) - 1)
            D = (D + round_keys[2 * i + 1]) & ((1 << self.word_size) - 1)
            C ^= D
            C = (C << (D % self.word_size)) | (C >> (self.word_size - (D % self.word_size)))
            C &= ((1 << self.word_size) - 1)
        return struct.pack('!HHHH', A, B, C, D)

    def _rc5_decrypt_block(self, block):
        A, B, C, D = struct.unpack('!HHHH', block)
        round_keys = self._expand_key()
        for i in range(self.num_rounds - 1, -1, -1):
            C = (C >> (D % self.word_size)) | (C << (self.word_size - (D % self.word_size)))
            C &= ((1 << self.word_size) - 1)
            C ^= D
            D = (D - round_keys[2 * i + 1]) & ((1 << self.word_size) - 1)
            C = (C - round_keys[2 * i]) & ((1 << self.word_size) - 1)
            A = (A >> (B % self.word_size)) | (A << (self.word_size - (B % self.word_size)))
            A &= ((1 << self.word_size) - 1)
            A ^= B
            B = (B - round_keys[2 * i + 1]) & ((1 << self.word_size) - 1)
            A = (A - round_keys[2 * i]) & ((1 << self.word_size) - 1)
        return struct.pack('!HHHH', A, B, C, D)

    def _expand_key(self):
        num_key_words = len(self.key) // (self.word_size // 8)
        round_keys = [(P_CONST + (i * Q_CONST)) & ((1 << self.word_size) - 1) for i in range(2 * (self.num_rounds + 1))]
        key_words = list(struct.unpack('!' + 'H' * num_key_words, self.key))
        i = j = 0
        A = B = 0
        for _ in range(3 * max(len(key_words), 2 * (self.num_rounds + 1))):
            A = round_keys[i] = (round_keys[i] + A + B) & ((1 << self.word_size) - 1)
            B = key_words[j] = (key_words[j] + A + B) & ((1 << self.word_size) - 1)
            i = (i + 1) % (2 * (self.num_rounds + 1))
            j = (j + 1) % len(key_words)

        return round_keys

    def generate_seed(self):
        """Generate seed for IV generation"""
        return int.from_bytes(os.urandom(4), byteorder='big') #elder on the beginning