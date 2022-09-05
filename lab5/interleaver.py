import numpy as np


class BlockInterleaver:

    def __init__(self, word_length, separation_distance=2**3):
        self.D = separation_distance
        self.N = word_length
        self.block_size = self.D * self.N

    def interleave(self, bitarray):
        """

        :param bitarray:
        :return:
        """
        bitarray = np.reshape(bitarray, (self.N, self.D), order='C')
        bitarray = np.reshape(bitarray, (self.D, self.N), order='F')
        bitarray = np.ravel(bitarray)
        return bitarray

    def deinterleave(self, bitarray):
        """

        :param bitarray:
        :return:
        """
        bitarray = np.reshape(bitarray, (self.D, self.N), order='C')
        bitarray = np.reshape(bitarray, (self.N, self.D), order='F')
        bitarray = np.ravel(bitarray)
        return bitarray
