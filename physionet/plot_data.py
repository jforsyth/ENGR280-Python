import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from pathlib import Path

# Replicate these lines in Python console

BASE_DIR = Path(__file__).resolve().parent
ORDER = 100
MIN_SPACING = 10

# read in file with better column names
signal = pd.read_csv(BASE_DIR / 'samples.csv', names=['time', 'ml2', 'v5'])

# drop the bad data
signal = signal.drop([0, 1])

# set the correct types
signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})

data_array = np.array(signal['v5'])

# Find relative extrema on the dataset (points that are higher than n points to their left and right)
data_peaks = argrelextrema(data_array, np.greater_equal, order=ORDER)[0]

x = []
y = []

for i in range(0, len(data_peaks)):

    # If not the last data point
    if i != len(data_peaks) - 1:

        # Only include point if it's at least 10 points away from last peak
        # This avoids heartbeats with small plateaus at the top being marked twice
        if data_peaks[i+1] - data_peaks[i] > MIN_SPACING:
            x.append(data_peaks[i]+2)  # +2 to adjust for removed points
            y.append(data_array[data_peaks[i]])

    # Mark the last point normally
    else:
        x.append(data_peaks[i]+2)
        y.append(data_array[data_peaks[i]])

print(len(x))

# plot the data
signal['v5'].plot()

plt.scatter(x, y, c='orange', s=100)
# now show the plot for real
plt.show()
