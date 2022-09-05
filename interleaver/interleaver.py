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


if __name__ == '__main__':
    n = 7       # Code word length
    d = 5       # Separation distance

    # Generate random data
    bits = np.random.randint(0, 2, n * d)

    # Create an Interleaver
    interleaver = BlockInterleaver(n, d)

    interleaved = interleaver.interleave(bits)
    deinterleaved = interleaver.deinterleave(interleaved)

    print('Origianl bitarray: {}'.format(bits))
    print('Interleaved: {}'.format(interleaved))
    print('De-interleaved: {}'.format(deinterleaved))


    print('Original data = Deinterleaved: {}'.format(np.array_equal(bits, deinterleaved)))
