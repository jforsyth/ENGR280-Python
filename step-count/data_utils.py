from scipy.signal import argrelextrema
import numpy as np

def find_maxima_groups(maxima_array, spacing):
    """
    Finds groups of local maximas based on
        spacing from one another. 

    Parameters:
    maxima_array (list): List containing indicies of maximas
    spacing (int): Maximum distance between points to still 
        be considered in a group

    Returns:
    list of lists: Indcies representing "groups" of maximas
    """
    groups = []
    start = maxima_array[0]
    end = maxima_array[0]
    for i in range(0, len(maxima_array) - 1):
        if maxima_array[i+1] - maxima_array[i] > spacing:
            end = maxima_array[i]
            groups.append([start, end])
            start = maxima_array[i + 1]
        if i == len(maxima_array) - 2:
            end = maxima_array[-1]
            groups.append([start, end])

    return groups


def find_walking_maxima_groups(maxima_groups, min_length, min_avg_value, moving_avg_data):
    """
    Given clusters of maximas, determines which fall into the criteria
    of "walking."

    Parameters:
    maxima_groups (list of lists): Lists of indicies of where maxima clusters begin
        and end
    min_length (int): Minimum length of cluster to be considered walking
    min_avg_value (int): Minimum average value of range to be considered walking

    Returns:
    list of lists: List of indicies defining the beginning and ending of clusters
        that fit the criteria of walking.
    """
    walking_groups = []
    for i in maxima_groups:
        if i[1] - i[0] > min_length:
            if np.average(moving_avg_data[i[0]:i[1]]) > min_avg_value:
                walking_groups.append(i)
    return walking_groups


def find_extrema(data_array, min_spacing, order):
    """
    Finds extrema over a data array that fit specific criteria.

    Parameters:
    data_array (numpy.array): Array over which to find extrema
    min_spacing (int): Minimum number of data points between extrema
    order (int): Number of points over which the extrema should be
        a relative maxima of

    Returns:
    Tuple of lists: list of x values for extrema and corresponding list
        of y values
    """
    MIN_HEIGHT = 0.1# max(data_array) / 10 # Peaks must be higher than 1/10th the highest point to be considered 

    # Find relative extrema on the dataset (points that are higher than n points to their left and right)
    data_peaks = argrelextrema(data_array, np.greater_equal, order=order)[0]

    data_peaks_filter = data_array[data_peaks] > MIN_HEIGHT

    above_data_peaks = data_peaks[data_peaks_filter]

    x = []
    y = []

    for i in range(0, len(above_data_peaks)):

        # If not the last data point
        if i != len(above_data_peaks) - 1:

            #print(f"{above_data_peaks[i+1]} - {above_data_peaks[i]} = {above_data_peaks[i+1] - above_data_peaks[i]}")

            # Only include point if it's at least MIN_SPACING points away from last peak
            # This avoids heartbeats with small plateaus at the top being marked twice
            if above_data_peaks[i+1] - above_data_peaks[i] > min_spacing:
                x.append(above_data_peaks[i]) 
                y.append(data_array[above_data_peaks[i]])

        # Mark the last point normally
        else:
            x.append(above_data_peaks[i])
            y.append(data_array[above_data_peaks[i]])

    return x, y
