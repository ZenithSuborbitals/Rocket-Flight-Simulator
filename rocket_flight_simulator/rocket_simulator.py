import json
import numpy as np

from atmosphere import Atmosphere

class RocketSimulator(object):
    R_EARTH = 6371000 # meters
    G_0 = -9.80665 # m/s^2 (at sea level)


    def __init__(self, file='parameters.json'):
        with open(file, 'r') as inputf:
            self.parameters = json.load(inputf)

        self.atmosphere = Atmosphere()

        self.time = 0
        self.height = self.parameters['launch_height']
        self.velocity = 0
        self.acceleration = 0

        self.max_height = 0
        self.max_velocity = 0
        self.max_acceleration = 0

        self.mass = self.parameters['launch_mass']
        self.thrust = self.parameters['engine_impulse'] / self.parameters['burn_length']

        print(self.parameters)

        self.data = {}
        self.data['time'] = []
        self.data['height'] = []
        self.data['velocity'] = []
        self.data['acceleration'] = []



    def run_simulation(self, ticksize):
        self.ticksize = ticksize

        while self.height >= self.parameters['launch_height']:
            self.run_tick()
        print(self.max_height, self.max_velocity, self.max_acceleration)

    def run_tick(self):

        self.height += self.velocity * self.ticksize
        self.velocity += self.acceleration * self.ticksize

        force = self.thrust_force() + self.drag_force() + self.gravity_force()
        self.acceleration = force / self.mass

        self.data['time'].append(self.time)
        self.data['height'].append(self.height)
        self.data['velocity'].append(self.velocity)
        self.data['acceleration'].append(self.acceleration)

        self.update_mass()
        self.update_max_values()
        self.time += self.ticksize




    def drag_force(self):
        pressure = self.atmosphere.get_density_by_height(self.height)
        # Rocket is heading up
        if self.velocity >= 0:
            drag_coef = self.parameters['rocket_drag_coef']
        # Rocket is falling with parachute deployed
        else:
            drag_coef = self.parameters['parachute_drag_coef']

        # Drag force is the opposite direction of velocity
        if self.velocity > 0:
            direction = -1
        else:
             direction = 1

        print(self.height, (direction * drag_coef * pressure * self.velocity**2 * self.parameters['cross_sectional_area'] ) / 2, self.acceleration)
        return (direction * drag_coef * pressure * self.velocity**2 * self.parameters['cross_sectional_area'] ) / 2


    def gravity_force(self):
        return self.mass * self.get_g_at_alitude(self.height)

    def get_g_at_alitude(self, height):
        return self.G_0 * ((height + self.R_EARTH) / self.R_EARTH)**2


    def thrust_force(self):
        if self.time < self.parameters['burn_length']:
            return self.thrust
        else:
            return 0

    def update_mass(self):
        if self.time > self.parameters['burn_length']:
            return
        else:
            self.mass -= (self.parameters['propellent_mass'] / self.parameters['burn_length']) * self.ticksize

    def update_max_values(self):
        if self.height > self.max_height:
            self.max_height = self.height

        if self.velocity > self.max_velocity:
            self.max_velocity = self.velocity

        if self.acceleration > self.max_acceleration:
            self.max_acceleration = self.acceleration
