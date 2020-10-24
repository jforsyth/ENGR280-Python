import time
import pandas as pd
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from multiprocessing import Process, Queue


class DataVis():

    def __init__(self, queue, rate):
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle('pyqtgraph example: Scrolling Plots')
        self.plot1 = self.win.addPlot()

        self.data = []
        self.queue = queue 

        # Filler data, not needed
        self.X = np.linspace(0, 3, 3)
        self.Y = np.linspace(0, 3, 3)

        self.curve1 = self.plot1.plot(self.X, self.Y)

        self.count = 0

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1 / rate)

    def update(self):

        self.data.append(self.queue.get())
        length = len(self.data)

        # Update data
        self.X = np.linspace(0, length, length)
        self.Y = self.data

        self.count += 1

        # Update graph data
        self.curve1.setData(self.X, self.Y)

    def start(self):
        import sys
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == "__main__":
    q = Queue()
    for i in range(0, 1000):
        q.put(i)
    vis = DataVis(q, 250)

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
