import numpy as np


class Track:
    def __init__(self, file):
        self.coords = np.loadtxt(file)
        self.start = self.coords[0]
        self.num_segments = 1




