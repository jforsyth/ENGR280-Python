from scipy.signal import argrelextrema
import numpy as np
import pandas as pd
import math

MIN_QRS_WAVE = 30 # milliseconds
MAX_QRS_WAVE = 150 # milliseconds
MS_PER_S = 1000 # milliseconds


def find_extrema(data_array, sampling_rate):
    MIN_HEIGHT = max(data_array) / 10 # Peaks must be higher than 1/10th the highest point to be considered 
    MIN_SPACING = math.ceil(sampling_rate * MIN_QRS_WAVE / MS_PER_S) # Samples in shortest possible QRS
    ORDER = math.ceil(sampling_rate * MAX_QRS_WAVE / MS_PER_S) # Samples in longest possible QRS

    # Find relative extrema on the dataset (points that are higher than n points to their left and right)
    data_peaks = argrelextrema(data_array, np.greater_equal, order=ORDER)[0]

    x = []
    y = []

    for i in range(0, len(data_peaks)):

        # If not the last data point
        if i != len(data_peaks) - 1:

            # Only include point if it's at least MIN_SPACING points away from last peak
            # This avoids heartbeats with small plateaus at the top being marked twice
            if data_peaks[i+1] - data_peaks[i] > MIN_SPACING:
                # Also checks if the point is above MIN_HEIGHT
                if data_array[data_peaks[i]] > MIN_HEIGHT:
                    x.append(data_peaks[i]) 
                    y.append(data_array[data_peaks[i]])

        # Mark the last point normally
        else:
            x.append(data_peaks[i]+2)
            y.append(data_array[data_peaks[i]])

    return x, y
