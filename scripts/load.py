import os
import csv

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
        except Exception:
            print("Error while grouping")

    return groupedDict