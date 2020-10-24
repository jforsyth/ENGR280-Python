import time
import pandas as pd
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from multiprocessing import Process, Queue


class DataVis():

    def __init__(self, queue, rate):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('Python EKG')
        self.plot1 = self.win.addPlot()
        self.plot2 = self.win.addPlot()

        self.data = np.empty(0) 
        self.queue = queue 

        # Filler data, not needed
        self.X = np.linspace(0, 3, 3)
        self.Y = np.linspace(0, 3, 3)

        self.curve1 = self.plot1.plot(self.X, self.Y)
        self.curve2 = self.plot2.plot(self.X, self.Y)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1 / rate)

        self.count = 0

    def update(self):
        self.update_curve_1()
        self.update_curve_2()

    def update_curve_1(self):
        self.data = self.data[-1000:]

        self.data = np.append(self.data, self.queue.get())

        length = len(self.data)

        # Update data
        self.X = np.linspace(0, length, length)
        self.Y = self.data

        self.plot1.setXRange(0, 1000)

        # Update graph data
        self.curve1.setData(self.X, self.Y)

    def update_curve_2(self):

        # Update data
        Y = self.filter(self.data)

        length = len(Y)
        X = np.linspace(0, length, length)

        self.plot2.setXRange(0, 1000)

        # Update graph data
        self.curve2.setData(X, Y)

    def filter(self, data):
        # Center data at zero instead of 5 or whatever it's normally at
        raw = data - data[0]

        ### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
        low_pass = np.convolve(raw, [0.023834522, 0.093047634, 0.232148599, 0.301938491, 0.232148599, 0.093047634, 0.023834522])

        ### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
        band_pass = np.convolve(low_pass, [-0.000798178, -0.003095487,-0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

        # Finds diff 
        diff = np.diff(band_pass)

        # Squares diff
        squared = diff * diff 

        # Applys a moving average
        weights = np.ones(38)
        movingAvg = np.convolve(squared, weights)

        return movingAvg


    def start(self):
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()
            self.plot1.close()
            self.plot2.close()
            self.win.close()

if __name__ == "__main__":
    q = Queue()
    for i in range(0, 1000):
        q.put(i)
    vis = DataVis(q, 250)

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
