# Rocket Flight Simulator

A python application that uses Euler's method to computationally solve the nonlinear, 2nd order differential equation that represents the vertical flight of a rocket. Uses 1st order approximations for atmospheric density and engine thrust data.

![Simulator](https://image.prntscr.com/image/Ll-SqvFVRhaifLjRa7ZVhg.png "Flight Simulator Program")


### Installation
`pip3 install -r requirements.txt`

### Libraries used
* `pyqt5` - Qt with python bindings to build the GUI
* `pyqtgraph` - Graphing module for pyqt to render graphs
* `numpy` - Array data types for graphing (requirement of `pyqtgraph`)



### Usage
`python3 rocket_flight_simulator/main.py`


### Citations
http://www.dtic.mil/dtic/tr/fulltext/u2/729858.pdf - for coefficient of drag of a parachute
