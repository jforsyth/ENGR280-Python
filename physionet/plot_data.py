import pandas as pd
import matplotlib.pyplot as plt

##### Replicate these lines in Python console

# read in file with better column names
signal = pd.read_csv('samples.csv', names=['time', 'ml2', 'v5'])

# drop the bad data
signal = signal.drop([0, 1])

# set the correct types
signal = signal.astype({'ml2': 'float32', 'v5': 'float32'})

#plot the data
signal['v5'].plot()

#now show the plot for real
plt.show()