import os
import csv
import log


def loadPopulationOfYear(year):
    dataArray = []
    with open('../dat/temp/population.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            dataArray.append(row)

    populationOfYear = [data for data in dataArray if data["Time"] == year and data["Variant"] == "Medium"]

    populationOfYearDict = {}

    for countryPopulation in populationOfYear:
        populationOfYearDict[countryPopulation["LocID"]] = countryPopulation

    return populationOfYearDict


COMMA = ','

def loadCSV(filepath, delimiter = COMMA):
    dataArray = []

    with open(filepath) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = delimiter)
        for row in csv_reader:
            dataArray.append(row)
    
    return dataArray


def loadGroupedCSV(filename, group, delimiter = COMMA):
    dataArray = loadCSV(filename, delimiter)

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


def loadHealthSpendingPerCapita():
    return loadGroupedCSV('../dat/temp/healthSpendingPerCapita.csv', "COUNTRY")

def loadCoronaCases(group = "geoId"):
    return loadGroupedCSV('../dat/temp/coronaCases.csv', group)

def loadGiniData():
    return loadGroupedCSV('../dat/temp/WorldBankGiniIndex.csv', "Country Code")

def loadGoogleTrendsData():
    returnDict = {}
    for filename in os.listdir("../dat/temp/googleTrends/"):
        if(filename.endswith(".csv")):
            countryTrendsData = loadCSV('../dat/temp/googleTrends/' + filename)
            returnDict[filename.replace(".csv", "")] = countryTrendsData

    return returnDict
