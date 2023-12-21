import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

pressureData = pd.read_csv(r"C:\Users\tgalyon\Desktop\pressure_converter\input.csv",index_col=False,skiprows=6)
time = []
pressure = []

time = pressureData.iloc[:,0]
pressure = pressureData.iloc[:,1]

def getDate(inputTime):
    global finalDateList
    finalDateList = []
    for i in inputTime:
        dateFormat = "%m/%d/%Y %H:%M:%S %p"
        n = datetime.strptime(i,dateFormat).date()
        finalDateList.append(n)
    

def getUniqueDay(inputDate):
    global uniqueDay
    uniqueDay = []
    for i in inputDate:
        if i not in uniqueDay:
            uniqueDay.append(i)

def removeZeros(inputData,inputTime):
    global finalTime
    global finalPressure
    global finalDate
    global monthDay
    monthDay = []
    finalTime = []
    finalPressure = []
    finalDate = []
    index = 0
    for item in inputData:
        if item > 10:
            finalPressure.append(item)
            finalTime.append((5 + (index * 5))/(24*60))
            finalDate.append(finalDateList[index])
            index += 1
    for i in finalDate:
        monthDay.append(str(i.month)+str(i.day))

def cleanData(inputData,inputTime,inputDate):
    for i in range(5):
        inputData.pop()    
        inputTime.pop()
        inputDate.pop()

def getDailyAverage(uniqueData, inputTime, finalPressure):
    tempSum = []
    global dailyAverage
    dailyAverage = []
    for i in uniqueData:
        for idn, n in enumerate(inputTime):
            if idn == (len(inputTime) - 1):
                tempSum.append(finalPressure[inputTime.index(n)])
                dailyAverage.append(np.average(tempSum))
                tempSum.clear()
            elif i == n:
                tempSum.append(finalPressure[inputTime.index(n)])

def getDailyMax(uniqueData, inputTime, finalPressure):
    tempMax = 0
    global dailyMax
    dailyMax = []
    for i in uniqueData:
        for idn, n in enumerate(inputTime):
            if i == n:
                if finalPressure[idn] > tempMax:
                    tempMax = (finalPressure[idn])
                    if idn == (len(inputTime) - 1):
                        dailyMax.append(tempMax)
                        tempMax = 0
            else:
                if idn == (len(inputTime) - 1):
                    dailyMax.append(tempMax)
                    tempMax = 0

def getDailyMin(uniqueData, inputTime, finalPressure):
    tempMin = 1000
    global dailyMin
    dailyMin = []
    for i in uniqueData:
        for idn, n in enumerate(inputTime):
            if i == n:
                if finalPressure[idn] < tempMin:
                    tempMin = (finalPressure[idn])
                    if idn == (len(inputTime) - 1):
                        dailyMin.append(tempMin)
                        tempMin = 1000
            else:
                if idn == (len(inputTime) - 1):
                    dailyMin.append(tempMin)
                    tempMin = 1000

def getAverage(input):
    global averageDailyMean
    averageDailyMean = round(np.average(input),1)

def getMax(input):
    global averageDailyMax
    averageDailyMax = round(np.average(input),1)

def getMin(input):
    global averageDailyMin
    averageDailyMin = round(np.average(input),1)

def getStats(input):
    global globalMin
    global globalMax
    global globalMean
    globalMin = round(np.min(input),1)
    globalMax = round(np.max(input),1)
    globalMean = round(np.average(input),1)

getDate(time) 
removeZeros(pressure, time)
getUniqueDay(monthDay)
getDailyAverage(uniqueDay, monthDay, finalPressure)
getDailyMax(uniqueDay, monthDay, finalPressure)
getDailyMin(uniqueDay, monthDay, finalPressure)
getAverage(dailyAverage)
getMax(dailyMax)
getMin(dailyMin)
getStats(finalPressure)

print("Daily Min: " + str(averageDailyMin))
print("Daily Max: " + str(averageDailyMax))
print("Daily Average "  + str(averageDailyMean))
print(" ")
print("Global Min: " + str(globalMin))
print("Global Max: " + str(globalMax))
print("Global Average: " + str(globalMean))

data = {
    "Date of Reading": pd.Series(finalDate), 
    "Time (Days)": pd.Series(finalTime), 
    "Pressure": pd.Series(finalPressure), 
    "Daily Average": pd.Series(averageDailyMean), 
    "Daily Min": pd.Series(averageDailyMin), 
    "Daily Max": pd.Series(averageDailyMax),
    "Global Average": pd.Series(globalMean),
    "Global Min": pd.Series(globalMin),
    "Global Max": pd.Series(globalMax)
    }

df = pd.DataFrame(data)
df.to_csv(r"C:\Users\tgalyon\Desktop\pressure_converter\out.csv")

plt.plot(finalTime,finalPressure, color = "blue")
plt.title("Pressure vs. Time", size = 18)
plt.xlabel("Time (Days)", size = 12)
plt.ylabel("Pressure (psi)", size = 12)
plt.xticks(np.arange(np.min(finalTime), np.max(finalTime), 1))
plt.xlim(min(finalTime),max(finalTime))
plt.rc('lines', linewidth = 4)
plt.grid(linestyle = "--")
plt.rcParams['figure.dpi']=360
plt.text(x=1, y=min(finalPressure), s="Average Daily Max: " + str(averageDailyMax), \
    color = "black", fontsize = 10)
plt.text(x=1, y=min(finalPressure) + 5, s="Average Daily Min: " + str(averageDailyMin), \
    color = "black", fontsize = 10)
plt.text(x=1, y=min(finalPressure) + 10, s="Average Daily Mean: " + str(averageDailyMean), \
    color = "black", fontsize = 10)
plt.show()

#Written and developed by Tyler C. Galyon