import time
import pandas as pd
import numpy as np
import pylab as plt
from multiprocessing import Process, Queue

class DataVis():

    def __init__(self):
        self.data = []
        self.X = np.linspace(0,3,3)
        self.Y = np.linspace(0,3,3)
        plt.ion()
        self.graph = plt.plot(self.X,self.Y, color="green")[0]

    def read_data_loop(self, queue, sampling_rate):
        draw_rate = 1 / sampling_rate

        while True:
            if not queue.empty():
                for _ in range(0,10):
                    self.data.append(queue.get())
                length = len(self.data)
                plt.xlim(length-1000, length+100)
                plt.ylim(4,6)
                self.X = np.linspace(0, length, length)
                self.Y = self.data
                self.graph.set_xdata(self.X)
                self.graph.set_ydata(self.Y)
                plt.draw()
                plt.pause(draw_rate)
            else:
                plt.pause(draw_rate)

if __name__ == "__main__":
    q = Queue()
    for i in range(0,1000):
        q.put(i)
    vis = DataVis() 
    vis.read_data_loop(q, 250)