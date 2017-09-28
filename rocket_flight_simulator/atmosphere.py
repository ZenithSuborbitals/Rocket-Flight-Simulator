import csv

# Interface to the data contained in atmosphere.csv
class Atmosphere(object):
    HEIGHT_MIN = -304.8
    HEIGHT_MAX = 85344
    # Public
    def __init__(self,file='atmosphere.csv'):
        self._data = []

        with open(file, 'r') as data_file:
            csv_reader = csv.DictReader(data_file, delimiter = ',')
            for line in csv_reader:
                self._data.append(line)

    def get_attribute_by_height(self, height, attribute):
                index = self._get_index_by_height(height)

                if index < 0 or index > len(self._data):
                    print('Index out of bounds: ', index)
                    return -1

                # Perform a linear approximation if between terms
                base_height = float(self._data[index]['alt (m)'])
                height_diff = height - base_height
                if height_diff < 0.1: # allow for floating point inexactness
                    return float(self._data[index][attribute])
                else:
                    next_index = index + 1
                    next_height = float(self._data[next_index]['alt (m)'])
                    delta_height = float(next_height - base_height)

                    base_attribute = float(self._data[index][attribute])
                    next_attribute = float(self._data[next_index][attribute])
                    delta_attribute = next_attribute - base_attribute

                    return base_attribute + (delta_attribute * height_diff) / delta_height

    def get_pressure_by_height(self, height):
        return self.get_attribute_by_height(height, 'press (kpa)')

    def get_density_by_height(self, height):
        return self.get_attribute_by_height(height, 'dens (kg/cu.m)')


    # Private
    @staticmethod
    def _get_index_by_height(height):
        if height < Atmosphere.HEIGHT_MIN or height > Atmosphere.HEIGHT_MAX:
            return -1

        if height < 19812:
            return int((height / 304.8) + 1)
        elif height >= 19812:
            return int(66 + ((height / 1524) - 13))
