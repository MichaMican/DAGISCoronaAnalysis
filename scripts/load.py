import os
import csv
import log

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

def loadCoronaCases(group = "geoId"):

    dataArray = []
    with open('../dat/temp/coronaCases.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            dataArray.append(row)

    groupedDict = {}
    for row in dataArray:
        try:
            groupedDict[row[group]].append(row)
        except KeyError:
            groupedDict[row[group]] = []
            groupedDict[row[group]].append(row)
        except Exception as error:
            log.logError("Error while grouping - Error: " + str(error))

    return groupedDict