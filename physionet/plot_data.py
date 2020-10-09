import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from pathlib import Path

##### Replicate these lines in Python console

BASE_DIR = Path(__file__).resolve().parent

# read in file with better column names
signal = pd.read_csv(BASE_DIR / 'samples.csv', names=['time', 'ml2', 'v5'])

# drop the bad data
signal = signal.drop([0, 1])

# set the correct types
signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})

data_array = np.array(signal['v5'])
data_peaks = argrelextrema(data_array, np.greater_equal, order=100)[0]


x = []
y = []
for i in range(0,len(data_peaks)):
    if i != len(data_peaks) - 1:
        if data_peaks[i+1] - data_peaks[i] > 10:
            x.append(data_peaks[i]+2)
            y.append(data_array[data_peaks[i]])
    else:
            x.append(data_peaks[i]+2)
            y.append(data_array[data_peaks[i]])
    
print(len(x))

#plot the data
signal['v5'].plot()

plt.scatter(x,y,c='orange', s=100)
#now show the plot for real
plt.show()