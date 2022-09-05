from numpy.random import normal


class AWGN:

    def __init__(self, std):
        self.std = std

    def propagate(self, x):
        complex_noise = normal(0, (self.std)/2, x.shape) + 1j*normal(0, (self.std)/2, x.shape) 
        return x + complex_noise
