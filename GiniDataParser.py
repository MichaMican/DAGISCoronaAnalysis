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
    plotData(dataDictionary)
    
def createDir():
    try:
        os.mkdir("./out/")
    except FileExistsError:
        pass

    try:
        os.mkdir("./out/groupedGiniData/")
    except FileExistsError:
        pass

def readCsv():
    resultArray = []
    with open('./dat/(3)WorldBankGiniIndex.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            resultArray.append(row)

    return resultArray

def groupByCountry(dataArray):
    groupedDict = {}
    for row in dataArray:
        try:
            groupedDict[row["Country Code"]].append(row)
        except KeyError:
            groupedDict[row["Country Code"]] = []
            groupedDict[row["Country Code"]].append(row)
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

def plotData(dataDict):
    maxLength = len(dataDict)
    progress = 1

    for countryKey in dataDict:
        giniValue = []
        years = []
        printProgressBar(progress, maxLength, "Saving plot for " + countryKey)

        for countryDict in dataDict[countryKey]:

            for year in countryDict.keys():
                if year.isdecimal():
                    if(countryDict[year] != ''):
                        giniValue.append(float(countryDict[year]))
                        years.append(int(year))
                        

        progress += 1

        plt.plot(years, giniValue)
        plt.ylabel('Gini-Coefficient')
        plt.xlabel('Year')
        #bitte dynamisch setzen
        plt.xlim([1960, 2020])
        plt.ylim([0,100])
        figure = plt.gcf()
        figure.set_size_inches(19.2, 10.8)
        if(countryKey == ""):
            pass
            #plt.savefig("./out/caseNumberHistoryPerCountry/noCountryCode.png",
            #            bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
        else:
            pass
            #plt.savefig("./out/caseNumberHistoryPerCountry/" + countryKey +
            #            ".png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
        plt.show()
        plt.clf()
        plt.close()

        


main()