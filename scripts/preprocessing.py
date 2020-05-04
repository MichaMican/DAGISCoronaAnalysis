import csv
import log
import pycountry
import draw


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


def generateGiniCoefficientMap(newestGiniCoefficientDict):

    dataToDraw = {}

    for countryKey, countryGiniCoefData in newestGiniCoefficientDict.items():
        dataToDraw[countryKey] = countryGiniCoefData["value"]

    draw.generateMaps({"gini-coeff": dataToDraw}, colorMap = 'RdYlGn')

def convertCasesDeathsToTotalCases(coronaCasesDataDict):

    convertedDict = coronaCasesDataDict.copy()

    for countryKey, coronaCasesOfCountry in convertedDict.items():
        totalDeaths = []
        totalCases = []

        sortedCornaCasesOfCountry = sorted(coronaCasesOfCountry, key=lambda e: int(
            e["year"]) * 10000 + int(e["month"]) * 100 + int(e["day"]))

        for coronaCasesDaily in sortedCornaCasesOfCountry:
            if len(totalCases) > 0:
                totalCases.append(totalCases[-1] + int(coronaCasesDaily["cases"]))
                coronaCasesDaily["totalCases"] = totalCases[-1]
                
            else:
                totalCases.append(int(coronaCasesDaily["cases"]))
                coronaCasesDaily["totalCases"] = totalCases[-1]

            if len(totalDeaths) > 0:
                totalDeaths.append(totalDeaths[-1] + int(coronaCasesDaily["deaths"]))
                coronaCasesDaily["totalDeaths"] = totalCases[-1]

            else:
                totalDeaths.append(int(coronaCasesDaily["deaths"]))
                coronaCasesDaily["totalDeaths"] = totalCases[-1]

    return convertedDict
            
def generateHealthSpendingMap(healthSpendingDict):

    dataForMapGeneration = {"healthspending": {}}

    for countryKey in healthSpendingDict:
        sortedHealthSpendingByYear = sorted(healthSpendingDict[countryKey], key=lambda e:
                                                int(e["YEAR"])
                                                )
        
        countryKeyConverter = pycountry.countries.get(alpha_3 = sortedHealthSpendingByYear[-1]["COUNTRY"])

        if countryKeyConverter != None:
            dataForMapGeneration["healthspending"][countryKeyConverter.alpha_2] = float(sortedHealthSpendingByYear[-1]["Numeric"])

    draw.generateMaps(dataForMapGeneration, colorMap = 'RdYlGn', targetFolder="../out/healthSpending/")




def generateGiniCoronaMap(coronaCasesDataDict, newestGiniCoefficientDict, populationOfYear):

    dataForMapCase = {}
    dataForMapDeaths = {}

    convertedCasesDataDict = convertCasesDeathsToTotalCases(coronaCasesDataDict)

    for countryKey, casesOfCountry in convertedCasesDataDict.items():

        for dayCaseOfCountry in casesOfCountry:
            if dayCaseOfCountry["dateRep"] not in dataForMapCase.keys():
                dataForMapCase[dayCaseOfCountry["dateRep"]] = {}
                dataForMapDeaths[dayCaseOfCountry["dateRep"]] = {}

            if countryKey in newestGiniCoefficientDict.keys() and countryKey in populationOfYear.keys():
                dataForMapCase[dayCaseOfCountry["dateRep"]][countryKey] = newestGiniCoefficientDict[countryKey]["value"]/100 * (dayCaseOfCountry["totalCases"]/(populationOfYear[countryKey] * 1000)) * 100000
                dataForMapCase[dayCaseOfCountry["dateRep"]][countryKey] = newestGiniCoefficientDict[countryKey]["value"]/100 * (dayCaseOfCountry["totalDeaths"]/(populationOfYear[countryKey] * 1000)) * 100000

    draw.generateMaps(dataForMapCase, colorMap = 'RdYlGn', targetFolder="../out/maps/giniCaseCoef/")
    draw.generateMaps(dataForMapDeaths, colorMap = 'RdYlGn', targetFolder="../out/maps/giniDeathCoef/")

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
                        currentDataValue = float(countryGiniData[year])

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
                    log.log(
                        countryKey + " was skipped because it has an invalid alpha 3 country key")
            else:
                log.log(countryKey +
                        " was skipped because it has no Gini-Coefficient data")

    return returnDict
