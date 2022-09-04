import numpy as np


class Track:
    def __init__(self, file):
        self.coords = np.loadtxt(file)
        self.start = self.coords[0]
        self.num_segments = 0


class Acceleration(Track):
    def __init__(self):
        super().__init__(file="./tracks/accel.txt")
        self.num_segments = 1
        self.end = self.coords[-1]
        self.start = self.coords[0]
        self.length = np.linalg.norm(self.end - self.start)


class Skidpad(Track):
    def __init__(self, file):
        super().__init__(file)
        self.num_segments = 5  # TODO - update this
        self.start = self.coords[0]


