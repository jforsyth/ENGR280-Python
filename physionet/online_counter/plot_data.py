import time
import math
import pandas as pd
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from multiprocessing import Process, Queue

class DataVis():

    RANGE = 500
    MS_PER_S = 1000 # milliseconds
    HEART_MIN_REFACTORY_PERIOD = 250 # milliseconds

    def __init__(self, queue, rate):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('Python EKG')

        # Create two plots, one for raw data and
        # the other for data after filters, etc.
        self.plot1 = self.win.addPlot()
        self.plot2 = self.win.addPlot()

        # Create an empty np array to append data to
        self.data = np.empty(0) 

        # Set queue to multiprocess queue input
        self.queue = queue 

        # Filler data, not needed
        self.X = np.linspace(0, 3, 3)
        self.Y = np.linspace(0, 3, 3)

        pen = pg.mkPen(color=(141, 252, 93), width=3)

        # Set curves to plot on graph
        self.curve1 = self.plot1.plot(self.X, self.Y, pen=pen)
        self.curve2 = self.plot2.plot(self.X, self.Y, pen=pen)

        # Set refresh rate of graph to 1sec / sample rate
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1 / rate)

        self.count = 0
        self.heartbeat_counter = 0
        self.points_since_last_heartbeat = 0

        self.sampling_rate = rate

    def update(self):
        """
        Update all plots. Put update methods here
        """
        self.update_data()
        self.update_curve_1()
        self.update_curve_2()
        self.update_heartbeat_count()

        ''' USE FOR DEBUGGING TIME ISSUES
        self.count += 1
        if self.count % 250 == 0:
            print(time.perf_counter())
        '''

    def update_data(self):
        """
        Updates data range
        """
        # Set data to only last 1000 points
        # (analyzing all data slows down program)
        self.data = self.data[-self.RANGE:]

        # Gets next queue item
        next_point = self.queue.get()

        # Appends last queue item to data
        self.data = np.append(self.data, next_point)


    def update_curve_1(self):
        """
        Update raw data curve
        """
        length = len(self.data)

        # Update data
        self.X = np.linspace(0, length, length)
        self.Y = self.data

        self.plot1.setXRange(0, self.RANGE)

        # Update graph data
        self.curve1.setData(self.X, self.Y)

    def update_curve_2(self):
        """
        Update filtered data curve
        """
        # Update flter data
        self.filter_data = self.filter(self.data)

        length = len(self.filter_data)
        X = np.linspace(0, length, length)

        self.plot2.setXRange(0, self.RANGE)

        # Update graph data
        self.curve2.setData(X, self.filter_data)

    def update_heartbeat_count(self):
        if len(self.filter_data) > self.RANGE:
            last_filter_point = self.filter_data[100]

            if last_filter_point > 0.03 and self.points_since_last_heartbeat > math.ceil((self.sampling_rate / self.MS_PER_S) * self.HEART_MIN_REFACTORY_PERIOD):
                self.heartbeat_counter += 1
                self.points_since_last_heartbeat = 0
                print(f"*beep* {self.heartbeat_counter}")
            else:
                self.points_since_last_heartbeat += 1
        else:
            self.points_since_last_heartbeat += 1

    def filter(self, data):
        """
        Logic for filtering, diffing, and averaging data
        """
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
        """
        Open gui window and close processes after exiting
        """
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
        print("test")
