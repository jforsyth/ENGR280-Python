from file_utils import loadWithJSON

## Will load all Harrisonburg and Rockingham data into a list of lists
## Each element in the main list will contain a list of two items, the str:date and int:cases
harrisonburg_data = loadWithJSON('harrisonburg.json')
rockingham_data = loadWithJSON('rockingham.json')

## Print all elements in the list as an example
for data in harrisonburg_data:
    date = data[0]
    cases = data[1]

#creating an empty list for dates and cases so that each code index for the lists match to call each easily
hburgDateLst = []
hburgCaseLst = []
#sifting through json files to add data to lists to easily access them
for data in harrisonburg_data:
    hburgDate = data[0]
    hburgCase = data[1]
    hburgDateLst.append(hburgDate)
    hburgCaseLst.append(hburgCase)

rockDateLst = []
rockCaseLst = []
for data in rockingham_data:
    rockDate = data[0]
    rockCase = data[1]
    rockDateLst.append(rockDate)
    rockCaseLst.append(rockCase)

#sifting through to find the change over each 24 hour period in hburg
hburgChangeLst = []
i = 1
while i < len(hburgCaseLst):
    hburgChange = hburgCaseLst[i] - hburgCaseLst[i-1]
    hburgChangeLst.append(hburgChange)
    i += 1

peakHburgCaseGrowth = max(hburgChangeLst)
peakHburgDate = hburgDateLst[hburgChangeLst.index(peakHburgCaseGrowth) + 1]

#sifting through to find the change over each 24 hour period in rock
rockChangeLst = []
a = 1
while a < len(rockCaseLst):
    rockChange = rockCaseLst[a] - rockCaseLst[a-1]
    rockChangeLst.append(rockChange)
    a += 1

peakRockCaseGrowth = max(rockChangeLst)
peakRockDate = rockDateLst[rockChangeLst.index(peakRockCaseGrowth) + 1]

#Now we are attempting at a window in hburg
hburgWeekLst = []
q = 0
while q < (len(hburgChangeLst) - 7):
    hburgWeek = sum(hburgChangeLst[q: (q+8)])
    hburgWeekLst.append(hburgWeek)
    q += 1

peakHburgWeekGrowth = max(hburgWeekLst)
peakHburgWeekBeginning = hburgDateLst[hburgWeekLst.index(peakHburgWeekGrowth) + 1]
peakHburgWeekEnd = hburgDateLst[hburgWeekLst.index(peakHburgWeekGrowth) + 8]

#same for rock
rockWeekLst = []
w = 0
while w < (len(rockChangeLst) - 7):
    rockWeek = sum(rockChangeLst[w: (w+8)])
    rockWeekLst.append(rockWeek)
    w += 1

peakRockWeekGrowth = max(rockWeekLst)
peakRockWeekBeginning = rockDateLst[rockWeekLst.index(peakRockWeekGrowth) + 1]
peakRockWeekEnd = rockDateLst[rockWeekLst.index(peakRockWeekGrowth) + 8]

print(" ")
print('When was the first positive COVID case in Rockingham County and Harrisonburg?')
print(" ")#easy, first case is on the first recorded day clearly
print("The first case was on " + str(hburgDateLst[0]) + " and there were " + str(hburgCaseLst[0]) + " reported cases in Harrisonburg")
print("The first case was on " + str(rockDateLst[0]) + " and there were " + str(rockCaseLst[0]) + " reported cases in Rockingham")
print(" ")
print('What day was the maximum number of cases recorded in Harrisonburg and Rockingham County?')
print(" ")#here we go
print("The highest rise in cases happened on " + str(peakHburgDate) + " with " + str(peakHburgCaseGrowth) + " new cases in Harrisonburg")
print("The highest rise in cases happened on " + str(peakRockDate) + " with " + str(peakRockCaseGrowth) + " new cases in Rockingham")
print(" ")
print('What was the worst week in the city/county for new COVID cases? '
      'When was the rise in cases the fastest over a seven day period?')
#we did it
print(" ")
print('The worst week of case growth was ' + str(peakHburgWeekGrowth) + ' cases which occured between ' +
      str(peakHburgWeekBeginning) + " to " + str(peakHburgWeekEnd) + ' in Harrisonburg')
print('The worst week of case growth was ' + str(peakRockWeekGrowth) + ' cases which occured between ' +
      str(peakRockWeekBeginning) + " to " + str(peakRockWeekEnd) + ' in Rockingham')