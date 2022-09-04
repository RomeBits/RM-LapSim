import numpy as np


class Car:
    def __init__(self, car_data, engine_data):
        f = open(car_data, "r")
        self.params = {}
        
        for i in f:
            self.params[i.split()[0]] = i.split()[1]
        f.close()

        self.params['total_mass'] = self.params['driver_mass'] + self.params['car_mass']

        f = open(engine_data, "r")
        self.engine = np.genfromtxt(f, delimiter=',')
        f.close()

    def calc_forward_step(self):
        pass
