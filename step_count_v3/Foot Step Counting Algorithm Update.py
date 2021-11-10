import pandas
import matplotlib.pyplot as plt
import sys

file = pandas.read_csv(sys.argv[1])
window = 20
s = 0
time_between_steps = 0
threshold = 750
peaksum = 0

steps = []
vals = []

alldata = []

avg_peak_multiplier = 0.25

for i in range (0, len(file) - window): #So it only runs to the last starting window value and not to the end of the length
    #DATA PIPELINE
    a =((file["x"][i:i+ window])**2 + (file["y"][i:i+ window])**2 + (file["z"][i:i+ window])**2)**(1/2) #Magnitude of Acceleration for the window
    b = a.diff() #diff of magnitude of acceleration
    c = b**2 #square of diff
    d = c.rolling(window = 5).mean() #taking the rolling average
    e = d[window/2 + i] #evaluation point of the window

    #DETECTION
    leftmax = d[5:10].max() #maximum of 5 values to the left of e
    rightmax = d[11:].max() #maximum of values to the right of e in the window 

    alldata.append(e)

    if e > leftmax and e > rightmax and e > threshold and time_between_steps > 1: 
        #print(f"leftmax: {leftmax}, rightmax: {rightmax}, e: {e}")
        s += 1
        time_between_steps = 0
        steps.append(i)
        vals.append(e)
        peaksum += e
        avg_peak = peaksum / s
        threshold = avg_peak * avg_peak_multiplier
    else:
        time_between_steps += 1
    
    if time_between_steps > 5 and avg_peak_multiplier > 0.2:
        avg_peak_multiplier -= 0.1

# plt.plot(alldata)
# plt.scatter(steps, vals, color="orange")
# plt.show()
    
    
print (f"{s} steps")
print(steps)