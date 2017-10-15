import unittest

from rocket_flight_simulator.thruster import Thruster


class TestAtmosphere(unittest.TestCase):
    def setUp(self):
        self.thruster = Thruster()

    def test_thrust(self):
        # Beware of floating point number trickery here
        self.assertAlmostEqual(self.thruster.get_thrust_at_time(0), 97.86084)
