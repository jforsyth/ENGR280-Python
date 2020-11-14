import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

if len(sys.argv) == 1:
    print("usage: main.py (filename)")
    sys.exit(1)

signal = pd.read_csv(sys.argv[1],
                     names=['time', 'accel_x', 'accel_y', 'accel_z',
                            'gyro_x', 'gyro_y', 'gyro_z', 'mag_x', 'mag_y', 'mag_z'])

signal = signal.drop([0])  # Drop bad data

signal = signal.astype({'time': 'float32',
                        'accel_x': 'float32',
                        'accel_y': 'float32', 
                        'accel_z': 'float32',
                        'gyro_x': 'float32',
                        'gyro_y': 'float32', 
                        'gyro_z': 'float32'
                        })

x = signal['accel_x'].to_numpy()
y = signal['accel_y'].to_numpy()
z = signal['accel_z'].to_numpy()

raw = (x**2 + y**2 + z**2)**(0.5)

raw = raw - raw[0]  # Start first point at zero

### pass data through LOW PASS FILTER (fs=250Hz, fc=15, N=6) ###
low_pass = np.convolve(raw, [0.023834522, 0.093047634, 0.232148599,
                             0.301938491, 0.232148599, 0.093047634, 0.023834522])

### pass data through HIGH PASS FILTER (fs=250Hz, fc=5Hz, N=6) to create BAND PASS result ###
band_pass = np.convolve(low_pass, [-0.000798178, -0.003095487, -
                                   0.007692586, 0.989209446, -0.007692586, -0.003095487, -0.000798178])

# Finds diff
diff = np.diff(band_pass)

# Squares diff
squared = diff * diff

# Applys a moving average
weights = np.ones(38)
movingAvg = np.convolve(squared, weights)

movingAvgDiff = np.diff(movingAvg)**2

diffPeaks = argrelextrema(movingAvgDiff, np.greater, order=30)[0]

x = []
y = []

for i in diffPeaks:
    if movingAvgDiff[i] > 0.2:
        x.append(i)
        y.append(movingAvgDiff[i])

plt.plot(movingAvg)
plt.scatter(x,y, c='green')
plt.show()
