import numpy as np


class Hamming74:

    def __init__(self):
        """
        G is the Generator matrix
        H is the Parity check matrix
        """

        # TODO: ASSING THE MISSING MATRICES (non-systematic)
        p = np.array([[1, 1, 0, 1], [1, 0, 1, 1], [0, 1, 1, 1]])
        temp = np.hstack((p.T, np.identity(4)))
        temp[:, [2, 3]] = temp[:, [3, 2]]
        self.G = temp.astype(int)
        temp = np.hstack((np.identity(3), p))
        temp[:, [2, 3]] = temp[:, [3, 2]]
        self.H = temp.astype(int)

    def encode(self, data):
        """§§
        :param data: np.array where each position represents a bit {0, 1}.
        :return: np.array representing the code word.
        """
        #Transform the input data into the code word
        #print("G: {}".format(self.G))
        #print("H: {}".format(self.H))
        code_word = np.matmul(data, self.G) % 2
        return code_word

    def decode(self, code_word):

       # param code_word: np.array where each position represents a bit {0, 1}.

        #Calculate syndrome vector
        z = np.matmul(code_word, self.H.T) % 2
        #Calculate the position of the error if s is non-zero (i.e. error exists)
        if np.sum(z) != 0:
            sum = 0
            for i in range(len(z)):
                sum += z[i]*(2**i)
            #Correct error
            code_word[int(sum)-1] = (code_word[int(sum)-1] + 1) % 2
        R = np.array([[0, 0, 1, 0, 0, 0, 0],[0, 0, 0, 0, 1, 0, 0],[0, 0, 0, 0, 0, 1, 0],[0, 0, 0, 0, 0, 0, 1]])
        return np.matmul(R, code_word)
