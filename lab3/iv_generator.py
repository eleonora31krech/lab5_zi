import struct

from lab3.constants import DEFAULT_A, DEFAULT_C, DEFAULT_M


class LemerRandom:
    def __init__(self, seed, a=DEFAULT_A, c=DEFAULT_C, m=DEFAULT_M):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def get_bytes(self, num_bytes):
        result = b''
        for _ in range(num_bytes):
            self.state = (self.a * self.state + self.c) % self.m
            result += struct.pack('B', self.state & 0xFF) #only last 8
        return result
