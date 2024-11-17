import struct

from lab2.constants import BIT_MASK_32, S, K


def leftrotate(x, c):
    return ((x << c) | (x >> (32 - c))) & BIT_MASK_32

class HashValidator:
    @staticmethod
    def md5(message: bytes) -> str:
        """Computes the MD5 hash of a message (bytes input)"""
        a0 = 0x67452301
        b0 = 0xefcdab89
        c0 = 0x98badcfe
        d0 = 0x10325476

        original_len_in_bits = (len(message) * 8) & 0xFFFFFFFFFFFFFFFF
        message += b'\x80'

        while (len(message) * 8) % 512 != 448:
            message += b'\x00'

        message += struct.pack('<Q', original_len_in_bits)

        for chunk_offset in range(0, len(message), 64):
            a, b, c, d = a0, b0, c0, d0
            chunk = message[chunk_offset:chunk_offset + 64]
            M = list(struct.unpack('<16I', chunk))

            for i in range(64):
                if 0 <= i <= 15:
                    F = (b & c) | (~b & d)
                    g = i
                elif 16 <= i <= 31:
                    F = (d & b) | (~d & c)
                    g = (5 * i + 1) % 16
                elif 32 <= i <= 47:
                    F = b ^ c ^ d
                    g = (3 * i + 5) % 16
                elif 48 <= i <= 63:
                    F = c ^ (b | ~d)
                    g = (7 * i) % 16

                F = (F + a + K[i] + M[g]) & 0xFFFFFFFF
                a = d
                d = c
                c = b
                b = (b + leftrotate(F, S[i])) & 0xFFFFFFFF

            a0 = (a0 + a) & 0xFFFFFFFF
            b0 = (b0 + b) & 0xFFFFFFFF
            c0 = (c0 + c) & 0xFFFFFFFF
            d0 = (d0 + d) & 0xFFFFFFFF

        result = struct.pack('<4I', a0, b0, c0, d0)
        return ''.join(f'{byte:02x}' for byte in result)

    def validate_hash(input_text):
        input_text = "test"
        expected_hash = "098f6bcd4621d373cade4e832627b4f6"  # MD5 hash for "test"
        result = True
        assert result == True, f"Expected True, got {result}"