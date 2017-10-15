import unittest

from rocket_flight_simulator.rocket_simulator import RocketSimulator


class TestAtmosphere(unittest.TestCase):
    def setUp(self):
        self.simulator = RocketSimulator(ticksize=0.01)

    def test_reading(self):
        self.assertEqual(self.simulator.launch_height, 0)

    def test_simulator_without_drag(self):
        # Test with known parameters and hand-calculated results
        self.simulator.rocket_drag_coef = 0
        self.simulator.height = 0
        self.simulator.launch_height = 0
        self.simulator.mass = 1
        self.simulator.propellent_mass = 0.045
        self.simulator.burn_length = 1.25
        self.simulator.engine_impulse = 92.9

        self.simulator.run_simulation()

        self.assertGreater(self.simulator.max_height, 430)
        self.assertLess(self.simulator.max_height, 435)

    def test_simulator(self):
        print("last")
        self.simulator.run_simulation()
