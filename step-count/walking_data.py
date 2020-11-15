import pandas as pd
import numpy as np

class WalkingData():

    def __init__(self, filepath):
        signal = pd.read_csv(filepath,
                     names=['time', 'accel_x', 'accel_y', 'accel_z',
                            'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z'])
        signal = signal.drop([0])  # Drop bad data

        self.signal = signal.astype({'time': 'float32',
                                'accel_x': 'float32',
                                'accel_y': 'float32', 
                                'accel_z': 'float32'})
        
        accel_x = self.signal['accel_x'].to_numpy()
        accel_y = self.signal['accel_y'].to_numpy()
        accel_z = self.signal['accel_z'].to_numpy()

        raw = (accel_x**2 + accel_y**2 + accel_z**2)**(0.5)

        self.raw = raw - raw[0]


        # pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
        self.low_pass = np.convolve(self.raw, [0.023834522, 0.093047634, 0.232148599,
                                        0.301938491, 0.232148599, 0.093047634, 0.023834522])
        
        # pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
        self.band_pass = np.convolve(self.low_pass, [-0.000798178, -0.003095487, -
                                            0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])
        
        # Finds diff
        self.diff = np.diff(self.band_pass)
        
        # Squares diff
        self.squared = self.diff * self.diff
        
        # Applys a moving average
        weights = np.ones(38)
        self.moving_avg = np.convolve(self.squared, weights)
        