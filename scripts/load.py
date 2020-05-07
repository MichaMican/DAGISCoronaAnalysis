import os
import csv
import log
import pycountry


COMMA = ','

def loadCSV(filepath, delimiter = COMMA):
    dataArray = []

    with open(filepath) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = delimiter)
        for row in csv_reader:
            dataArray.append(row)
    
    return dataArray


def groupCSV(dataArray, group):
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


def loadGroupedCSV(filename, group, delimiter = COMMA):
    dataArray = loadCSV(filename, delimiter)
    return groupCSV(dataArray, group)

def loadPopulationGroupedByYear():
    return loadGroupedCSV('../dat/temp/population.csv', "Time")

def loadHealthSpendingPerCapita():
    return loadGroupedCSV('../dat/temp/healthSpendingPerCapita.csv', "COUNTRY")

def loadCoronaCases(group = "countryCode"):
    coronaCases = loadCSV('../dat/temp/coronaCases.csv')

    fixedCoronaCases = []

    for report in coronaCases:
        country = pycountry.countries.get(alpha_3 = report["countryterritoryCode"])

        areaName = report["countriesAndTerritories"].replace("_", " ")
        countryCode = report["geoId"] #This isn't technically correct, but keeps the corner cases in the dataset

        if country != None:
            areaName = country.name
            countryCode = country.alpha_2

        fixedCoronaCases.append({
            "areaName": areaName,
            "countryCode": countryCode,
            "cases": report["cases"],
            "deaths": report["deaths"],
            "date": report["dateRep"],
            "year": report["year"],
            "month": report["month"],
            "day": report["day"]
        })

    groupedCoronaCases = groupCSV(fixedCoronaCases, group)
    return groupedCoronaCases

def loadGiniData():
    return loadGroupedCSV('../dat/temp/giniData/WorldBankGiniIndex.csv', "Country Code")

def loadGoogleTrendsData():
    returnDict = {}
    for filename in os.listdir("../dat/temp/googleTrends/"):
        if(filename.endswith(".csv")):
            countryTrendsData = loadCSV('../dat/temp/googleTrends/' + filename)
            returnDict[filename.replace(".csv", "")] = countryTrendsData

    return returnDict
