import unittest

from rocket_flight_simulator.atmosphere import Atmosphere


class TestAtmosphere(unittest.TestCase):
    def setUp(self):
        self.atmosphere = Atmosphere()

    def test_indexing(self):
        self.assertEqual(Atmosphere._get_index_by_height(0), 1)
        self.assertEqual(Atmosphere._get_index_by_height(85344), 109)

    def test_pressure(self):
        # Beware of floating point number trickery here
        self.assertAlmostEqual(self.atmosphere.get_pressure_by_height(0), 101.3245403)
        self.assertAlmostEqual(self.atmosphere.get_pressure_by_height(4572), 57.2075233)
        self.assertAlmostEqual(self.atmosphere.get_pressure_by_height(85344), 0.000419289)

        pressure = self.atmosphere.get_pressure_by_height(84000)
        self.assertLess(pressure, 0.000547752)
        self.assertGreater(pressure, 0.000419289)

        pressure = self.atmosphere.get_pressure_by_height(10000)
        self.assertGreater(pressure, 26.26240922)
        self.assertLess(pressure, 27.51208812)
