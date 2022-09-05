import numpy as np
import matplotlib.pyplot as plt

from awgn import AWGN
from hamming74 import Hamming74
from interleaver import BlockInterleaver
from qpsk import QPSK


def all_included():

    variance = np.linspace(0, 1, num=11, endpoint=True)

    # Generate random bits
    bits = np.random.randint(0, 2, 2**16)

    # Variables
    interleave_word_size = 16
    nbrBits = len(bits)

    # Initiating classes
    qpsk = QPSK()
    hamming = Hamming74()

    #######################################################################################
    # TX

    # Encode
    tx = np.reshape(bits, (int(nbrBits/4), 4))
    list = []
    for row in tx:
        list.append(hamming.encode(row))
    tx = np.ravel(list)
    nbrBits = len(tx)

    # Interleave
    interleaver = BlockInterleaver(
        int(interleave_word_size), int(nbrBits/interleave_word_size))
    tx = interleaver.interleave(tx)

    # Modulate with QPSK
    tx = qpsk.mod(tx)

    #######################################################################################
    # CHANNEL

    # Introduce AWGN noise
    list = []
    for i in variance:
        awgn = AWGN(np.sqrt(i))
        list.append(awgn.propagate(tx))
    tx = np.array(list)

    #######################################################################################
    # RX

    rx = tx

    # Demodulate, deinterleave and decode for all 11 variances
    all_arr = []
    #count = 0
    for row in rx:
        #print("Variance {}".format(variance[count]))
        # Demodulate
        list = []
        for i in range(nbrBits):
            list.append(qpsk.demod(row[i]))
        row = np.array(list)
        #print("done demod")
        # Deinterleave
        row = interleaver.deinterleave(row)
        #print("done deinterleave")
        # Decode
        row = np.reshape(row, (int(nbrBits/7), 7))
        list = []
        for row in row:
            list.append(hamming.decode(row))
        row = np.ravel(list)
        #print("done decode")
        all_arr.append(row)
        #count += 1

    # Calculate BER
    ber = np.zeros(11)
    for i in range(len(variance)):
        for j in range(len(bits)):
            if all_arr[i][j] != bits[j]:
                ber[i] += 1
    for i in range(len(ber)):
        ber[i] = ber[i]/len(bits)
        print("Variance: {:.1f}".format(
            variance[i]) + " | BER: {:.4f}".format(ber[i]) + " | {:.4f} percent".format(ber[i]*100))
        #plt.plot(variance, ber)
        #plt.show()

def qpsk_hamming():

    variance = np.linspace(0, 1, num=11, endpoint=True)

    # Generate random bits
    bits = np.random.randint(0, 2, 2**16)

    # Variables
    nbrBits = len(bits)

    # Initiating classes
    qpsk = QPSK()
    hamming = Hamming74()

    #######################################################################################
    # TX

    # Encode
    tx = np.reshape(bits, (int(nbrBits/4), 4))
    list = []
    for row in tx:
        list.append(hamming.encode(row))
    tx = np.ravel(list)
    nbrBits = len(tx)

    # Modulate with QPSK
    tx = qpsk.mod(tx)

    #######################################################################################
    # CHANNEL

    # Introduce AWGN noise
    list = []
    for i in variance:
        awgn = AWGN(np.sqrt(i))
        list.append(awgn.propagate(tx))
    tx = np.array(list)

    #######################################################################################
    # RX

    rx = tx

    # Demodulate, deinterleave and decode for all 11 variances
    all_arr = []
    count = 0
    for row in rx:
        # Demodulate
        list = []
        for i in range(nbrBits):
            list.append(qpsk.demod(row[i]))
        row = np.array(list)
        # Decode
        row = np.reshape(row, (int(nbrBits/7), 7))
        list = []
        for row in row:
            list.append(hamming.decode(row))
        row = np.ravel(list)
        all_arr.append(row)
        count += 1

    # Calculate BER
    ber = np.zeros(11)
    for i in range(len(variance)):
        for j in range(len(bits)):
            if all_arr[i][j] != bits[j]:
                ber[i] += 1
    for i in range(len(ber)):
        ber[i] = ber[i]/len(bits)
        print("Variance: {:.1f}".format(
            variance[i]) + " | BER: {:.4f}".format(ber[i]) + " | {:.4f} percent".format(ber[i]*100))
        #plt.plot(variance, ber)
        #plt.show()

def only_qpsk():

    variance = np.linspace(0, 1, num=11, endpoint=True)

    # Generate random bits
    bits = np.random.randint(0, 2, 2**16)

    nbrBits = len(bits)

    # Initiating classes
    qpsk = QPSK()

    #######################################################################################
    # TX

    # Modulate with QPSK
    tx = qpsk.mod(bits)

    #######################################################################################
    # CHANNEL

    # Introduce AWGN noise
    list = []
    for i in variance:
        awgn = AWGN(np.sqrt(i))
        list.append(awgn.propagate(tx))
    tx = np.array(list)

    #######################################################################################
    # RX

    rx = tx

    # Demodulate, deinterleave and decode for all 11 variances
    all_arr = []
    #count = 0
    for row in rx:
        #print("Variance {}".format(variance[count]))
        # Demodulate
        list = []
        for i in range(nbrBits):
            list.append(qpsk.demod(row[i]))
        row = np.array(list)
        #print("done demod")
        #count += 1
        all_arr.append(row)

    # Calculate BER
    ber = np.zeros(11)
    for i in range(len(variance)):
        for j in range(len(bits)):
            if all_arr[i][j] != bits[j]:
                ber[i] += 1
    for i in range(len(ber)):
        ber[i] = ber[i]/len(bits)
        print("Variance: {:.1f}".format(
            variance[i]) + " | BER: {:.4f}".format(ber[i]) + " | {:.4f} percent".format(ber[i]*100))
        #plt.plot(variance, ber)
        #plt.show()


if __name__ == '__main__':
    
    print("Only QPSK")
    only_qpsk()
    print("QPSK and Hamming74")
    qpsk_hamming()
    print("QPSK, Hamming and Interleaver")
    all_included()
