import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema


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

    def get_steps(self, plot=False):

        movingAvgDiff = np.diff(self.moving_avg)**2
        diffPeaks = argrelextrema(movingAvgDiff, np.greater_equal, order=10)[0]

        # Finds relative maximas on the diff of the moving average (squared for no negatives)
        x = []
        y = []
        for i in diffPeaks:
            if movingAvgDiff[i] > 0.01:
                x.append(i)
                y.append(0)

        # Finds groups of maximas spaced less than MAXIMA_SPACING apart
        maxima_groups = self._find_maxima_groups(x, 100)

        # Finds groups of maximas that fit criteria of walking
        walking_maxima_groups = self._find_walking_maxima_groups(
            maxima_groups, 1000, 0, self.moving_avg)

        # Create list of numpy arrays to be step counted
        data_containing_steps = []
        for data_range in walking_maxima_groups:
            data_containing_steps.append(
                self.squared[data_range[0]:data_range[1]])

        # For each step counted array, add points to x and y list
        # for plotting and counting
        x = []
        y = []
        for data in data_containing_steps:
            extrema = self._find_extrema(data, 15, 10)
            x += extrema[0]
            y += extrema[1]
            if plot:
                plt.plot(data)
                plt.scatter(x,y,c="orange")
                plt.show()

        return len(x)

    def _find_maxima_groups(self, maxima_array, spacing):
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

    def _find_walking_maxima_groups(self, maxima_groups, min_length, min_avg_value, moving_avg_data):
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

    def _find_extrema(self, data_array, min_spacing, order):
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
        MIN_HEIGHT = max(data_array) / 10 # Peaks must be higher than 1/10th the highest point to be considered
        # Find relative extrema on the dataset (points that are higher than n points to their left and right)
        data_peaks = argrelextrema(
            data_array, np.greater_equal, order=order)[0]
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
