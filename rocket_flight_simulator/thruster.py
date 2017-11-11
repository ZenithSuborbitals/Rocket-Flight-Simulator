import csv
from math import floor

class Thruster(object):
    def __init__(self, file='thrust.csv'):
        self._data = []
        self.load_data(file)

    def load_data(self, file):
        with open(file, 'r') as data_file:
            csv_reader = csv.DictReader(data_file, delimiter = ',')
            for line in csv_reader:
                self._data.append(line)

        self.measurement_interval = float(self._data[1]['time']) - float(self._data[0]['time'])
        print(self.measurement_interval)


    # Assume regulatly spaced intervals in the data input file
    def get_thrust_at_time(self, time):
        if time < 0 or time > (self.measurement_interval * (len(self._data) - 1)):
            return 0

        base_index = floor(time / self.measurement_interval)
        base_value = float(self._data[base_index]['thrust (newtons)'])
        next_value = float(self._data[base_index + 1]['thrust (newtons)'])

        time_diff = time - float(self._data[base_index]['time'])

        value_change = ((base_value - next_value) *  (time_diff / self.measurement_interval))
        return (base_value + value_change)
