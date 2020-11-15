import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from walking_data import WalkingData


# Checks to make sure file is run with a filename argument
if len(sys.argv) == 1:
    print("usage: main.py (filename)")
    sys.exit(1)

data = WalkingData(sys.argv[1])

print(f"Steps Counted from Walking Clusters: {data.get_steps(plot=True)}")

plt.show()