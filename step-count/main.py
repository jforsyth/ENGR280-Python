import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from data_utils import find_maxima_groups, find_walking_maxima_groups, find_extrema
from walking_data import WalkingData


# Checks to make sure file is run with a filename argument
if len(sys.argv) == 1:
    print("usage: main.py (filename)")
    sys.exit(1)


# Create data object
data = WalkingData(sys.argv[1])

movingAvgDiff = np.diff(data.moving_avg)**2
diffPeaks = argrelextrema(movingAvgDiff, np.greater_equal, order=10)[0]

# Finds relative maximas on the diff of the moving average (squared for no negatives)
x = []
y = []
for i in diffPeaks:
    if movingAvgDiff[i] > 0.01:
        x.append(i)
        y.append(0)


# Finds groups of maximas spaced less than MAXIMA_SPACING apart
maxima_groups = find_maxima_groups(x, 100)

# Finds groups of maximas that fit criteria of walking
walking_maxima_groups = find_walking_maxima_groups(maxima_groups, 1000, 0, data.moving_avg)


# Create list of numpy arrays to be step counted 
data_containing_steps = []
for data_range in walking_maxima_groups:
    data_containing_steps.append(data.moving_avg[data_range[0]:data_range[1]])


# For each step counted array, add points to x and y list 
# for plotting and counting
all_steps = []
for data in data_containing_steps:
    extrema = find_extrema(data, 15, 10)
    all_steps += extrema[0]
    x = extrema[0]
    y = extrema[1]
    plt.plot(data)
    plt.scatter(x,y,c="orange")

print(f"Clusters of Maxima:\n{maxima_groups}\n")
print(f"Clusters of Maxima that Fit \"Walking\" Criteria:\n{walking_maxima_groups}\n")
print(f"Steps Counted from Walking Clusters: {len(all_steps)}")

plt.show()