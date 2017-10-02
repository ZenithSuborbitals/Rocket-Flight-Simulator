from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import sys

from rocket_simulator import RocketSimulator


def init_charts():
    global layout, height_curve, velocity_curve, acceleration_curve
    height_plot = pg.PlotWidget(title="<h1> Height (AGL) </h1>")
    height_curve = height_plot.plot(pen=(255,0,0)) # Pure red, rgb value
    height_plot.enableAutoRange('xy', True)  # Keep auto-scrolling and size adjustments

    velocity_plot = pg.PlotWidget(title="<h1> Velocity (m/s) </h1>")
    velocity_curve = velocity_plot.plot(pen=(0,255,0))
    velocity_plot.enableAutoRange('xy', True)

    acceleration_plot = pg.PlotWidget(title="<h1> Acceleration (m/s^2) </h1>")
    acceleration_curve = acceleration_plot.plot(pen=(0,0,255))
    acceleration_plot.enableAutoRange('xy', True)

    # Add plots to layout
    layout.addWidget(height_plot, 0, 1, 1, 1) # plot goes on right side, spanning 3 rows
    layout.addWidget(velocity_plot, 1, 1, 1, 1)
    layout.addWidget(acceleration_plot, 2, 1, 1, 1)

def init_param_list():
    global layout
    params = QtGui.QGridLayout()

    i = 0
    for param in simulator.parameters:
        param_text = ' '.join(param.split('_')).title()

        label_slot = QtGui.QLabel()
        label_slot.setText(param_text + ":")

        display_slot = QtGui.QLabel()
        display_slot.setText(str(simulator.parameters[param]))

        params.addWidget(label_slot, i, 0)
        params.addWidget(display_slot, i, 1)
        i+=1


    # Add widgets to the layout in their proper positions
    layout.addLayout(params, 0, 0, 3, 1)   # button goes in upper-left


def update_charts():
    global simulator, height_curve, velocity_curve, acceleration_curve

    height_curve.setData(simulator.data['time'], simulator.data['height'])
    velocity_curve.setData(simulator.data['time'], simulator.data['velocity'])
    acceleration_curve.setData(simulator.data['time'], simulator.data['acceleration'])

# Main
app = QtGui.QApplication([])
simulator = RocketSimulator()

win = QtGui.QWidget()

win.resize(1000,600)
win.setWindowTitle('Rocket Simulator')
layout = QtGui.QGridLayout()
win.setLayout(layout)

pg.setConfigOptions(antialias=True)

init_charts()
init_param_list()

win.show()

# Run update every 10ms
timer = QtCore.QTimer()
timer.timeout.connect(update_charts)
timer.start(10)


simulator.run_simulation(0.1)
sys.exit(app.exec_())
