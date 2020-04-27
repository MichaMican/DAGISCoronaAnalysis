import csv
import log
import pycountry

def getTopFlopCountries(coronaCasesDataDict, healthSpendingDict, count):
    for countryKey in healthSpendingDict:
        healthSpendingDict[countryKey] = sorted(healthSpendingDict[countryKey], key=lambda e:
                                                int(e["YEAR"])
                                                )

    # sorted of dicts returns only keys as array
    sortedHealthSpendingCountryKeys = sorted(healthSpendingDict, key=lambda e:
                                             float(
                                                 healthSpendingDict[e][-1]["Numeric"])
                                             )

    topCountries = []

    counter = 0
    for countryKey in reversed(sortedHealthSpendingCountryKeys):
        try:
            country = pycountry.countries.get(alpha_3 = countryKey)
            conutryAlpha2 = country.alpha_2
            if conutryAlpha2 in coronaCasesDataDict.keys():
                counter += 1
                topCountries.append({"coronaCases": coronaCasesDataDict[conutryAlpha2], "healthSpending": healthSpendingDict[countryKey]})
            
            if counter >= count:
                break

        except Exception as e:
            log.logWarning("Error while preprocessing sortedHealthSpending " + str(e))
    
    flopCountries = []

    counter = 0
    for countryKey in sortedHealthSpendingCountryKeys:
        try:
            country = pycountry.countries.get(alpha_3 = countryKey)
            conutryAlpha2 = country.alpha_2
            if conutryAlpha2 in coronaCasesDataDict.keys():
                counter += 1
                flopCountries.append({"coronaCases": coronaCasesDataDict[conutryAlpha2], "healthSpending": healthSpendingDict[countryKey]})
            
            if counter >= count:
                break

        except Exception as e:
            log.logWarning("Error while preprocessing sortedHealthSpending " + str(e))

    return {
        "top": topCountries,
        "flop": flopCountries
    }

def saveGiniGroupedDataToCsv(giniDataDictionary):
    maxLength = len(giniDataDictionary)
    progress = 1
    dictArray = []
    for countryKey in giniDataDictionary:
        newestYearWithData = -1
        currentDataValue = -1
        for year in giniDataDictionary[countryKey].keys():
            if year.isdecimal():
                if giniDataDictionary[countryKey][year] != "":
                    newestYearWithData = year
                    currentDataValue = str(giniDataDictionary[countryKey][year])

        if int(newestYearWithData) > 0:
            dictArray.append({
                "countryKey": countryKey,
                "lastYearWithData": newestYearWithData,
                "value": currentDataValue,
            })

    try:
        with open("../dat/temp/latestGiniCoefficient.csv", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["countryKey", "lastYearWithData", "value"])
            writer.writeheader()
            for data in dictArray:
                writer.writerow(data)
    except IOError as err:
        log.logError("I/O Error - Error: " + str(err))