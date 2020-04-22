import numpy as np
from pytrends.request import TrendReq
import csv
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import datetime
import os
from datetime import datetime

pytrend = TrendReq()

def main():
    createDir()
    dataArray = readCsv()
    dataDictionary = groupByCountry(dataArray)
    print("We have " + str(len(dataDictionary)) + " countries loaded")
    #plotData(dataDictionary)
    #saveGroupedDataToCsv(dataDictionary)
    downloadAllGoogleTrendsData(dataDictionary)
    

def downloadAllGoogleTrendsData(dataDict):
    maxLength = len(dataDict)
    progress = 0
    for countryKey in dataDict:
        printProgressBar(progress, maxLength, "Downloading Google Trends data for " + countryKey)
        geoId = dataDict[countryKey][0]["geoId"]
        if(geoId != "" and geoId != None and geoId != "N/A"):
            try:
                downloadGoogleTrendsDataForCountry(dataDict[countryKey][0]["geoId"])
            except Exception:
                pass
        progress += 1

def downloadGoogleTrendsDataForCountry(geoId):
    pytrend.build_payload(kw_list=['/m/01cpyy'], timeframe='2019-11-01 ' +
                          datetime.now().strftime("%Y-%m-%d"), geo='DE')

    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df.to_csv("./dat/temp/googleTrends/dailyInteressts/" + geoId + ".txt")

def createDir():
    try:
        os.mkdir("./out/")
    except FileExistsError:
        pass

    try:
        os.mkdir("./out/groupedData/")
    except FileExistsError:
        pass
    
    try:
        os.mkdir("./out/caseNumberHistoryPerCountry/")
    except FileExistsError:
        pass

    try:
        os.mkdir("./dat/temp/")
    except FileExistsError:
        pass

    try:
        os.mkdir("./dat/temp/googleTrends/")
    except FileExistsError:
        pass

    try:
        os.mkdir("./dat/temp/googleTrends/dailyInteressts/")
    except FileExistsError:
        pass

def saveGroupedDataToCsv(groupedData):
    maxLength = len(groupedData)
    progress = 1
    for countryKey in groupedData:
        printProgressBar(progress, maxLength, "Saving " + countryKey + ".csv")
        csv_file = countryKey + ".csv"
        try:
            with open("./out/groupedData/"+csv_file, 'w+') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["dateRep", "day", "month", "year", "cases", "deaths",
                                                             "geoId", "continentExp", "countryterritoryCode", "popData2018", "countriesAndTerritories"])
                writer.writeheader()
                for data in groupedData[countryKey]:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
        progress += 1


def readCsv():
    resultArray = []
    with open('./dat/(1)coronaCases.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            resultArray.append(row)

    return resultArray


def groupByCountry(dataArray):
    groupedDict = {}
    for row in dataArray:
        try:
            groupedDict[row["geoId"]].append(row)
        except KeyError:
            groupedDict[row["geoId"]] = []
            groupedDict[row["geoId"]].append(row)
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
        printProgressBar(progress, maxLength, "Saving plot for " + countryKey)
        days = []
        cases = []
        countryDictSorted = sorted(dataDict[countryKey], key=lambda e: int(
            e["year"]) * 10000 + (int(e["month"])) * 100 + (int(e["day"])))

        for countryDict in countryDictSorted:
            days.append(countryDict["dateRep"])
            cases.append(int(countryDict["cases"]))

        plt.plot(days, cases)
        plt.ylabel('New cases')
        plt.xlabel('Date')
        figure = plt.gcf()
        # manager.resize(*manager.window.maxsize())
        figure.set_size_inches(19.2, 10.8)
        plt.savefig("./out/caseNumberHistoryPerCountry/" + countryKey +
                    ".png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
        plt.clf()
        progress += 1


main()
