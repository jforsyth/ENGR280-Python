from plot_data import DataVis
from live_data_simulator import DataSimulator
import multiprocessing as mp

SAMPLING_RATE = 250 #hz


if __name__ == '__main__':
    # Queue to use between data simulator and grapher
    q = mp.Queue()
    

    # Starts async process of appending "live" data to queue
    data_sim = DataSimulator('samples.csv')

    p1 = mp.Process(target=data_sim.start, args=(q, SAMPLING_RATE))
    p1.start()

    # Plots data from queue based on sample rate given
    data_vis = DataVis(q, SAMPLING_RATE)
    data_vis.start()

    p1.join()