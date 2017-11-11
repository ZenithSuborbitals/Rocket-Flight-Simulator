from pyqtgraph.Qt import QtCore
from PyQt5.Qt import QMutex
import json
import numpy as np
from time import sleep

from atmosphere import Atmosphere
from thruster import Thruster

class RocketSimulator(QtCore.QObject):
    R_EARTH = 6371000 # meters
    G_0 = -9.80665 # m/s^2 (at sea level)

    new_data  = QtCore.pyqtSignal(object)


    def __init__(self, ticksize, param_file='parameters.json'):
        QtCore.QObject.__init__(self)
        self.load_data(param_file)


    def load_data(self, param_file):
        with open(param_file, 'r') as inputf:
            self.parameters = json.load(inputf)

        # Set imported parameters as properties
        for parameter in self.parameters:
            setattr(self, parameter, self.parameters[parameter])
        # use for threadsafe commnications with the GUI thread
        self.mutex = QMutex()

        self.atmosphere = Atmosphere()
        self.initial_pressure = self.atmosphere.get_pressure_by_height(self.launch_height)

        # TODO Error analysis vs. ticksize
        self.ticksize = 0.0001

        self.time = 0
        self.height = self.launch_height
        self.velocity = 0
        self.acceleration = 0

        self.max_height = 0
        self.max_velocity = 0
        self.max_acceleration = 0

        self.mass = self.launch_mass

        self.thruster = Thruster()
        self.data = {}
        self.data['time'] = []
        self.data['height'] = []
        self.data['velocity'] = []
        self.data['acceleration'] = []


    def run_simulation(self):

        while self.height >= self.launch_height:
            self.run_tick()
        print(self.max_height, self.max_velocity, self.max_acceleration)

    def run_tick(self):

        self.height += self.velocity * self.ticksize
        self.velocity += self.acceleration * self.ticksize

        force = self.thrust_force() + self.drag_force() + self.gravity_force()
        self.acceleration = force / self.mass

        locked = False
        if self.mutex.tryLock(10):

            self.new_data.emit([self.time, self.height, self.velocity, self.acceleration])
            self.mutex.unlock()

        self.data['time'].append(self.time)
        self.data['height'].append(self.height)
        self.data['velocity'].append(self.velocity)
        self.data['acceleration'].append(self.acceleration)

        self.update_mass()
        self.update_max_values()
        self.time += self.ticksize

    def drag_force(self):
        density = self.atmosphere.get_density_by_height(self.height)
        # Rocket is heading up
        if self.velocity >= 0:
            drag_coef = self.rocket_drag_coef
            area = self.cross_sectional_area
        # Rocket is falling with parachute deployed
        else:
            drag_coef = self.parachute_drag_coef
            area = self.parachute_area

        # Drag force is the opposite direction of velocity
        if self.velocity > 0:
            direction = -1
        else:
             direction = 1

        return (direction * drag_coef * density * self.velocity**2 * area ) / 2


    def gravity_force(self):
        return self.mass * self.get_g_at_alitude(self.height)

    def get_g_at_alitude(self, height):
        return self.G_0 * ((height + self.R_EARTH) / self.R_EARTH)**2


    def thrust_force(self):
        if self.time < self.burn_length:
            return self.thruster.get_thrust_at_time(self.time) + self.get_vacuum_thrust()
        else:
            return 0
    # Max no VT: 905.0415775968264
    # Max w/ VT:
    def get_vacuum_thrust(self):
        return (self.initial_pressure - self.atmosphere.get_pressure_by_height(self.height)) * self.exit_area

    def update_mass(self):
        if self.time > self.burn_length:
            return
        else:
            self.mass -= (self.propellent_mass / self.burn_length) * self.ticksize

    def update_max_values(self):
        if self.height > self.max_height:
            self.max_height = self.height

        if self.velocity > self.max_velocity:
            self.max_velocity = self.velocity

        if self.acceleration > self.max_acceleration:
            self.max_acceleration = self.acceleration
