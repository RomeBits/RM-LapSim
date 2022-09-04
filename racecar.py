import numpy as np
from scipy.interpolate import interp1d, interp2d
from matplotlib import pyplot as plt


class Car:
    def __init__(self, car_data, engine_data):
        f = open(car_data, "r")
        self.params = {}
        
        for i in f:
            self.params[i.split()[0]] = i.split()[1]
        f.close()

        f = open(engine_data, "r")
        self.engine = np.genfromtxt(f, delimiter=',')
        self.engine_rpm = self.engine[:, 0]
        self.engine_torque = self.engine[:, 1]
        f.close()

        self.engine_force = None
        self.max_speed = None
        self.ggs = None

    def calc_forward_step(self):
        pass

    def engine_calcs(self):
        pass
        # Interpolate to 250 rpm increments
        x = np.array(self.engine_rpm).astype(np.float)
        y = np.array(self.engine_torque).astype(np.float)
        xx = np.linspace(x.min(), x.max(), int(x.max() / 250))
        interp = interp1d(x, y)
        yy = interp(xx)
        eng_rpm = xx
        eng_torque = yy

        # Get force multiplier for each gear
        final_drive = float(self.params['final_drive']) * float(self.params['primary_drive'])
        multiplier = []
        tire_circ = 2 * np.pi * float(self.params['tire_radius'])
        min_gear_ratio = 0
        max_gear_ratio = 0
        for i in range(len(self.params['gear_ratios'])):
            gear_ratio = float(self.params['gear_ratios'][i]) * final_drive
            if min_gear_ratio == 0 or gear_ratio < min_gear_ratio:
                min_gear_ratio = gear_ratio
            if max_gear_ratio == 0 or gear_ratio > max_gear_ratio:
                max_gear_ratio = gear_ratio
            multiplier.append(tire_circ / gear_ratio)
        max_speed = (max(eng_rpm) / 60) * tire_circ / min_gear_ratio
        min_force = eng_torque[0] * max_gear_ratio / float(self.params['tire_radius'])

        # # Get the wheel torque and wheel speed curves for each gear
        wheel_speed = []
        wheel_force = []
        for i in range(len(multiplier)):
            speed_mult = multiplier[i]
            force_mult = (tire_circ / multiplier[i]) / float(self.params['tire_radius'])
            wheel_speed.append(eng_rpm * speed_mult / 60)  # m/s
            wheel_force.append(eng_torque * force_mult)  # N

        # Interpolate the wheel force for each gear
        vehicle_speed = np.linspace(0, max_speed, int(max_speed / 0.1))
        for i in range(len(wheel_speed)):
            interp = interp1d(wheel_speed[i], wheel_force[i], fill_value=(min_force, 0), bounds_error=False)
            wheel_force[i] = interp(vehicle_speed)

        # Take the maximum wheel force at each speed
        vehicle_force = np.zeros(len(vehicle_speed), dtype=float)
        for i in range(len(wheel_force)):
            vehicle_force = np.maximum(vehicle_force, wheel_force[i])

        # Set the speed and wheel force arrays
        self.engine_force = interp1d(vehicle_speed, vehicle_force)
        self.max_speed = np.max(vehicle_speed)

        plt.plot(vehicle_speed, vehicle_force, 'g.')
        plt.show()

    def create_gg_plot(self):
        x = np.linspace(0, self.max_speed, 100)
        y = np.linspace(self.peak_brake(x), self.peak_accel(x), 100)
        xx, yy = np.meshgrid(x, y)
        z = self.get_max_lat(xx, yy)
        self.ggs = interp2d(x, y, z, kind='cubic')

