from plot_data import DataVis
from live_data_simulator import DataSimulator
from multiprocessing import Process, Queue

SAMPLING_RATE = 250 #hz

data_sim = DataSimulator()
data_vis = DataVis()

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=data_sim.start, args=(q, SAMPLING_RATE))
    p1.start()
    data_vis.read_data_loop(q, SAMPLING_RATE)