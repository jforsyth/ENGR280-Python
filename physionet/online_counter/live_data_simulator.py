import time
from pathlib import Path
import pandas as pd
from heartbeat_queue import HeartbeatQueue

class DataSimulator():
    def __init__(self):
        # Replicate these lines in Python console
        BASE_DIR = Path(__file__).resolve().parent.parent
        # read in file with better column names
        signal = pd.read_csv(BASE_DIR / 'data' / 'samples.csv', names=['time', 'ml2', 'v5'])
        # drop the bad data
        signal = signal.drop([0, 1])
        # set the correct types
        signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})
        self.raw = signal['v5'].to_numpy()
        self.hbq = HeartbeatQueue.get_instance()

    def start(self, queue, sampling_rate):
        refresh_rate = 1 / sampling_rate 
        for i in self.raw:
            queue.put(i)
            time.sleep(refresh_rate)
