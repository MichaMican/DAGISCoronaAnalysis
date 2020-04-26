import os
import csv
import log


def loadHealthSpendingPerCapita():
    dataArray = []
    with open('../dat/temp/healthSpendingPerCapita.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            dataArray.append(row)

    groupedDict = {}
    for row in dataArray:
        try:
            groupedDict[row["COUNTRY"]].append(row)
        except KeyError:
            groupedDict[row["COUNTRY"]] = []
            groupedDict[row["COUNTRY"]].append(row)
        except Exception as error:
            log.logError("Error while grouping - Error: " + str(error))

    return groupedDict



def loadGoogleTrendsData():
    returnDict = {}
    for filename in os.listdir("../dat/temp/googleTrends/"):
        if(filename.endswith(".csv")):
            countryTrendsData = []
            with open('../dat/temp/googleTrends/' + filename) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=',')

                for row in csv_reader:
                    countryTrendsData.append(row)

            returnDict[filename.replace(".csv", "")] = countryTrendsData

    return returnDict

def loadCoronaCases():

    dataArray = []
    with open('../dat/temp/coronaCases.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            dataArray.append(row)

    groupedDict = {}
    for row in dataArray:
        try:
            groupedDict[row["geoId"]].append(row)
        except KeyError:
            groupedDict[row["geoId"]] = []
            groupedDict[row["geoId"]].append(row)
        except Exception as error:
            log.logError("Error while grouping - Error: " + str(error))

    return groupedDict

def loadGiniData():
    groupedDict = {}
    resultArray = []
    with open('../dat/temp/WorldBankGiniIndex.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            resultArray.append(row)

    for row in resultArray:
        try:
            groupedDict[row["Country Code"]] = row     
        except Exception as err:
            log.logError("Error while grouping - Error: " + str(err))

    return groupedDict