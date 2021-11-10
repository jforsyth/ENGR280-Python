import pandas as pd
import matplotlib.pyplot as plt
import sys

data = pd.read_csv(sys.argv[1])

WINDOW = 10

try:
    threshold = int(sys.argv[2])
except:
    threshold = 200

steps = 0
state = "init"

accel = []
diff = []
square = []
avg = []
avg2 = []
index = 0
sum = 0
pts_since_step = 0
all_steps = []

while True:

    if state == "init":
        state = "load"

    elif state == "load":
        # Loads data into arrays if not full
        if len(accel) == 0:
            accel.append((data['x'][index]**2 + data['y'][index]**2 + data['z'][index]**2)**0.5)
            index += 1
            pts_since_step += 1
        elif len(accel) < WINDOW:
            accel.append((data['x'][index]**2 + data['y'][index]**2 + data['z'][index]**2)**0.5)
            state = "process"
        else:
            # Sets new data into circular arrays
            accel[index % WINDOW] = (data['x'][index]**2 + data['y'][index]**2 + data['z'][index]**2)**0.5
            state = "process"


    elif state == "process":
        if len(diff) < WINDOW:
            diff.append(accel[(index) % WINDOW] - accel[(index-1) % WINDOW])
            square.append(diff[(index-1) % WINDOW]**2)
            avg.append(0)
            sum += square[(index-1) % WINDOW]
            state = "load"
            pts_since_step += 1
        else:
            diff[(index-1) % WINDOW] = accel[index % WINDOW] - accel[(index-1) % WINDOW]
            sum -= square[(index-1) % WINDOW]
            square[(index-1) % WINDOW] = diff[index % WINDOW]**2
            sum += square[(index-1) % WINDOW]
            avg[index % WINDOW] = sum / WINDOW
            avg2.append(sum/WINDOW)
            state = "count"

    elif state == "count":
        point = avg[index % WINDOW]

        if point > 200:
            print("", end="")

        left_of_point = []
        right_of_point = []
        for i in range(1, WINDOW//2 + 1):
            left_of_point.append(avg[(index-i) % WINDOW])
            right_of_point.append(avg[(index+i) % WINDOW])

        if point > max(left_of_point) and point > max(right_of_point) and point > threshold and pts_since_step > 15:
            steps += 1
            all_steps.append(index)
            pts_since_step = 0
        else:
            pts_since_step += 1

        # if pts_since_step > 10:
        #     threshold -= 2

        state = "load"

        index += 1
        if index >= len(data):
            state = "done"
        else:
            state = "load"

    elif state == "done":
        break

try:
    if sys.argv[2] == "-g" or sys.argv[3] == "-g" :
        print(steps)
        plt.plot(avg2)
        plt.vlines(all_steps, 0, 1000, color="orange")
        plt.show()
except:
    print(steps)
    print(all_steps)