from file_utils import loadWithJSON
import numpy


def dumb_moving_average(thing):
      max = 0
      index = -1
      for i in range(0,len(thing)-7):
            value = thing[i:i+7]
            value = sum(value)
            if value>max:
                  max=value
                  index=i+7

      return (index,value)

## Will load all Harrisonburg and Rockingham data into a list of lists
## Each element in the main list will contain a list of two items, the str:date and int:cases
harrisonburg_data = loadWithJSON('harrisonburg.json')
rockingham_data = loadWithJSON('rockingham.json')

## Print all elements in the list as an example
#for data in harrisonburg_data:
#    date = data[0]
#    cases = data[1]
#    print('On '+date + ' there were '+ str(cases) +' cases in Harrisonburg')

###################################################################
print('\n\nWhen was the first positive COVID case in Rockingham County and Harrisonburg?')

print("First in Harrisonburg was " + str(harrisonburg_data[0][0]))
print("First in Rockingham County was " + str(rockingham_data[0][0]))
###################################################################

###################################################################
print('\n\nWhat day was the maximum number of cases recorded in Harrisonburg and Rockingham County?')
#assuming dating is continous in the json files....

harrisonburg_delta = list()
for i in range(0,len(harrisonburg_data)-1):
      current_day = harrisonburg_data[i]
      following_day = harrisonburg_data[i+1]

      case_change = following_day[1] - current_day[1]

      harrisonburg_delta.append((case_change))

rockingham_delta = list()
for i in range(0,len(rockingham_data)-1):
      current_day = rockingham_data[i]
      following_day = rockingham_data[i + 1]

      case_change = following_day[1] - current_day[1]

      rockingham_delta.append(case_change)


h_index = numpy.argmax(harrisonburg_delta, axis=0)

h_starting_cases = harrisonburg_data[h_index][1]
h_starting_day = harrisonburg_data[h_index][0]

h_ending_cases = harrisonburg_data[h_index + 1][1]
h_ending_day = harrisonburg_data[h_index + 1][0]

h_delta = h_ending_cases - h_starting_cases
print("Worst Harrisonburg day was " + str(h_ending_day) + " with " + str(h_ending_cases) + ". This was a jump of " + str(h_delta) + " from " + str(h_starting_cases) + " on the previous day.")

r_index = numpy.argmax(rockingham_delta, axis=0)
r_starting_cases = rockingham_data[r_index][1]
r_starting_day = rockingham_data[r_index][0]

r_ending_cases = rockingham_data[r_index + 1][1]
r_ending_day = rockingham_data[r_index + 1][0]

r_delta = r_ending_cases - r_starting_cases
print("Worst Rockingham day was " + str(r_ending_day) + " with " + str(r_ending_cases) + ". This was a jump of " + str(r_delta) + " from " + str(r_starting_cases) + " on the previous day.")

###################################################################


print('\n\nWhat was the worst week in the city/county for new COVID cases? '
      'When was the rise in cases the fastest over a seven day period?')

averages = numpy.convolve(harrisonburg_delta, [1,1,1,1,1,1,1])

numpy_method_averages = numpy.argmax(averages)
numpy_method_totals = averages[numpy_method_averages]
numpy_method_date = harrisonburg_data[numpy_method_averages + 1]

bad_method_averages = dumb_moving_average(harrisonburg_delta)
bad_method_date = harrisonburg_data[bad_method_averages[0]]
bad_method_total = bad_method_averages[1]


print("The worst rise over a seven day period for Harrisonburg resulted in " + str(numpy_method_totals) + " from the week ending "+str(numpy_method_date))

print('\n\nEnd!!!')