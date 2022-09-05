from operator import indexOf
import numpy as np

__all__ = ["QPSK"]


class QPSK:

    def __init__(self):
        # Gray coded QPSK
        self.constellation_map = np.array([ 1 + 1j, -1 + 1j, 1 - 1j, -1 - 1j ])

    def mod(self, bits: int) -> complex:
        """
        :param bits: Integer representation of the bits to be modulated.
        :type bits: int
        :return: The complex constellation symbol
        :rtype: complex
        """
        try:
            return self.constellation_map[bits]
        except IndexError:
            raise ValueError('{} is to large for this constellation.'
                             .format(bin(bits)))

    def demod(self, received_symbol: complex) -> int:
        """
        :param received_symbol: The complex symbol to be demodulated.
        :type received_symbol: np.array[complex]
        :return: The demodulated bits, represented with its Integer value.
        :rtype: int
        """
        eDist = []
        for symbol in self.constellation_map:
            eDist.append(np.linalg.norm(symbol - received_symbol))
        return eDist.index(min(eDist))


# if __name__ == '__main__':
#     qpsk = QPSK()

#     tx_symbol = qpsk.mod(2)
#     rx_bits = qpsk.demod(tx_symbol)

#     print('Sending {0:b}'.format(2))
#     print('Mapped to symbol {}'.format(tx_symbol))
#     print('Symbol {0} demapped to {1:b}'.format(tx_symbol, rx_bits))
