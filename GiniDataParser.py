import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import datetime
import os


def main():
    createDir()
    dataArray = readCsv()
    dataDictionary = groupByCountry(dataArray)
    print("We have " + str(len(dataDictionary)) + " countries loaded")
    #plotData(dataDictionary)
    saveGroupedDataToCsv(dataDictionary)
    
def createDir():
    try:
        os.mkdir("./out/")
    except FileExistsError:
        pass

    try:
        os.mkdir("./dat/temp/")
    except FileExistsError:
        pass

def readCsv():
    resultArray = []
    with open('./dat/(2)WorldBankGiniIndex.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            resultArray.append(row)

    return resultArray

def groupByCountry(dataArray):
    groupedDict = {}
    for row in dataArray:
        try:
            groupedDict[row["Country Code"]] = row     
        except Exception:
            print("Error while grouping")

    return groupedDict

def printProgressBar(progress, maxLength, message=""):
    os.system('cls')
    loadingStr = "["
    for x in range(30):
        if((progress/maxLength) * 30 >= x):
            loadingStr += "█"
        else:
            loadingStr += "-"

    loadingStr += "]"
    print(loadingStr)
    print("Finished: "+str(progress)+"/"+str(maxLength))
    print(message)

def saveGroupedDataToCsv(dataDictionary):
    maxLength = len(dataDictionary)
    progress = 1
    dictArray = []
    for countryKey in dataDictionary:
        newestYearWithData = -1
        currentDataValue = -1
        for year in dataDictionary[countryKey].keys():
            if year.isdecimal():
                if dataDictionary[countryKey][year] != "":
                    newestYearWithData = year
                    currentDataValue = str(dataDictionary[countryKey][year])

        if int(newestYearWithData) > 0:
            dictArray.append({
                "countryKey": countryKey,
                "lastYearWithData": newestYearWithData,
                "value": currentDataValue,
            })

    try:
        with open("./dat/temp/latestGiniCoefficient.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["countryKey", "lastYearWithData", "value"])
            writer.writeheader
            for data in dictArray:
                writer.writerow(data)
    except IOError:
        print("I/O error")


def plotData(dataDict):
    maxLength = len(dataDict)
    progress = 1

    for countryKey in dataDict:
        giniValue = []
        years = []
        printProgressBar(progress, maxLength, "Saving plot for " + countryKey)

        for year in dataDict[countryKey]:
            if year.isdecimal():         
                if(dataDict[countryKey][year] != ''):
                    giniValue.append(float(dataDict[countryKey][year]))
                    years.append(int(year))




        if len(giniValue) > 0:
            #plt.plot(years, giniValue, marker="o", linestyle= "solid")
            
            #bildet den den aktuellsten wert ab
            #plt.bar(years[len(years) - 1], giniValue[len(giniValue) - 1])

            #bildet alle werte ab
            plt.bar(years, giniValue)
            plt.ylabel('Gini-Coefficient')
            plt.xlabel('Year')
            #evtl dynamisch setzen?
            plt.xlim([1960, 2020])
            plt.ylim([0,100])
            figure = plt.gcf()
            figure.set_size_inches(19.2, 10.8)
            if(countryKey == ""):
                plt.savefig("./out/giniCoefficient/noCountryCode_Gini.png",
                            bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
            else:
                plt.savefig("./out/giniCoefficient/" + countryKey +
                            "_Gini.png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
            #plt.show()
            plt.clf()
            plt.close()

        progress += 1


        

main()