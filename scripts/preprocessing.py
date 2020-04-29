import csv
import log
import pycountry


def extractCountryPopulationForYear(populationRaw, year):
    population = {}
    for countryPopulation in populationRaw[year]:
        if countryPopulation["VarID"] == '2':
            country = pycountry.countries.get(
                numeric=countryPopulation["LocID"].zfill(3))
            if country != None:
                population[country.alpha_2] = float(
                    countryPopulation["PopTotal"])
            else:
                log.logWarning(
                    "Countrycode of " + countryPopulation["Location"] + "couldnt be parsed")

    return population


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
            country = pycountry.countries.get(alpha_3=countryKey)
            conutryAlpha2 = country.alpha_2
            if conutryAlpha2 in coronaCasesDataDict.keys():
                counter += 1
                topCountries.append(
                    {"coronaCases": coronaCasesDataDict[conutryAlpha2], "healthSpending": healthSpendingDict[countryKey], "alpha_2": conutryAlpha2})

            if counter >= count:
                break

        except Exception as e:
            log.logWarning(
                "Error while preprocessing sortedHealthSpending " + str(e))

    flopCountries = []

    counter = 0
    for countryKey in sortedHealthSpendingCountryKeys:
        try:
            country = pycountry.countries.get(alpha_3=countryKey)
            conutryAlpha2 = country.alpha_2
            if conutryAlpha2 in coronaCasesDataDict.keys():
                counter += 1
                flopCountries.append(
                    {"coronaCases": coronaCasesDataDict[conutryAlpha2], "healthSpending": healthSpendingDict[countryKey], "alpha_2": conutryAlpha2})

            if counter >= count:
                break

        except Exception as e:
            log.logWarning(
                "Error while preprocessing sortedHealthSpending " + str(e))

    return {
        "top": topCountries,
        "flop": flopCountries,
    }


def getNewestGiniCoefficientDict(giniDataDictionary):
    returnDict = {}
    for countryKey in giniDataDictionary:
        newestYearWithData = -1
        currentDataValue = -1
        for countryGiniData in giniDataDictionary[countryKey]:
            for year in countryGiniData.keys():
                if year.isdecimal():
                    if countryGiniData[year] != "":
                        newestYearWithData = year
                        currentDataValue = str(countryGiniData[year])

        countryObj = pycountry.countries.get(alpha_3=countryKey)

        if int(newestYearWithData) > 0 and countryObj != None:
            returnDict[countryObj.alpha_2] = {
                "countryKey_alpha2": countryObj.alpha_2,
                "countryKey_alpha3": countryObj.alpha_3,
                "lastYearWithData": newestYearWithData,
                "value": currentDataValue,
            }
        else:
            if int(newestYearWithData) > 0:
                if countryKey.lower() == 'XKX'.lower():
                    returnDict['XK'] = {
                        "countryKey_alpha2": 'XK',
                        "countryKey_alpha3": 'XKX',
                        "lastYearWithData": newestYearWithData,
                        "value": currentDataValue,
                    }
                else:
                    log.log(countryKey + " was skipped because it has an invalid alpha 3 country key")
            else:
                log.log(countryKey +
                        " was skipped because it has no Gini-Coefficient data")

    return returnDict
