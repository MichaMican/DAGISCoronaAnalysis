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

    draw.generateMaps({"Ginikoeffizient": dataToDraw}, colorMap = 'coolwarm', legendUnits = "Neuester Ginikoeffizient")

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
    healthspending = {}

    for countryKey in healthSpendingDict:
        sortedHealthSpendingByYear = sorted(healthSpendingDict[countryKey], key=lambda e:
                                                int(e["YEAR"])
                                                )
        
        countryKeyConverter = pycountry.countries.get(alpha_3 = sortedHealthSpendingByYear[-1]["COUNTRY"])

        if countryKeyConverter != None:
            healthspending[countryKeyConverter.alpha_2] = float(sortedHealthSpendingByYear[-1]["Numeric"])

    draw.generateMaps({"Healthspending": healthspending}, colorMap = 'RdYlGn', targetFolder="../out/healthSpending/", legendUnits = "Pro Kopf ausgaben für das Gesundheitssystem in USD")




def generateGiniCoronaMap(coronaCasesDataDict, newestGiniCoefficientDict, populationOfYear):

    dataForMapCase = {}
    dataForMapDeaths = {}

    convertedCasesDataDict = convertCasesDeathsToTotalCases(coronaCasesDataDict)

    for countryKey, casesOfCountry in convertedCasesDataDict.items():

        for dayCaseOfCountry in casesOfCountry:
            if dayCaseOfCountry["date"] not in dataForMapCase.keys():
                dataForMapCase[dayCaseOfCountry["date"]] = {}
                dataForMapDeaths[dayCaseOfCountry["date"]] = {}

            if countryKey in newestGiniCoefficientDict.keys() and countryKey in populationOfYear.keys():
                dataForMapCase[dayCaseOfCountry["date"]][countryKey] = newestGiniCoefficientDict[countryKey]["value"]/100 * (dayCaseOfCountry["totalCases"]/(populationOfYear[countryKey] * 1000)) * 100000
                dataForMapDeaths[dayCaseOfCountry["date"]][countryKey] = newestGiniCoefficientDict[countryKey]["value"]/100 * (dayCaseOfCountry["totalDeaths"]/(populationOfYear[countryKey] * 1000)) * 100000

    draw.generateMaps(dataForMapCase, colorMap = 'coolwarm', targetFolder = "../out/maps/giniCaseCoef/", legendUnits = "Ginikoeffizient * Coronafälle pro 100.000 Einwohner")
    draw.generateMaps(dataForMapDeaths, colorMap = 'coolwarm', targetFolder = "../out/maps/giniDeathCoef/", legendUnits = "Ginikoeffizient * Coronatodesfälle pro 100.000 Einwohner")

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



def getGroupedValues(valuesOnDay, valueKey, groupKey):
    valuesByCountry = {}

    for values in valuesOnDay:
        iso = values[groupKey]
        valuesByCountry[iso] = int(values[valueKey])
    
    return valuesByCountry


def __dateToSortableNumber(dateString):
    (day, month, year) = dateString.split('/')
    return int(year + month + day) # 01/01/2020 -> 20200101

def generateCoronaCaseWorldMaps(coronaCasesByDay):
    sortedDates = sorted(coronaCasesByDay.keys(), key=__dateToSortableNumber)

    # Map daily cases to their countries format
    coronaCases = {}
    coronaDeaths = {}
    coronaCasesTotal = {}
    coronaDeathsTotal = {}
    coronaCasesTotalSoFar = {}
    coronaDeathsTotalSoFar = {}
    for day in sortedDates:
        coronaCasesOnDay = coronaCasesByDay[day]
        coronaCases[day] = getGroupedValues(coronaCasesOnDay, "cases", "countryCode")
        coronaDeaths[day] = getGroupedValues(coronaCasesOnDay, "deaths", "countryCode")

        coronaCasesTotalToday = {}
        coronaDeathsTotalToday = {}

        for country, casesToday in coronaCases[day].items():
            casesSoFar = 0

            if country in coronaCasesTotalSoFar:
                casesSoFar = coronaCasesTotalSoFar[country]
            
            coronaCasesTotalToday[country] = casesSoFar + casesToday

        for country, deathsToday in coronaDeaths[day].items():
            deathsSoFar = 0

            if country in coronaDeathsTotalSoFar:
                deathsSoFar = coronaDeathsTotalSoFar[country]
            
            coronaDeathsTotalToday[country] = deathsSoFar + deathsToday
        
        coronaCasesTotal[day] = coronaCasesTotalToday
        coronaDeathsTotal[day] = coronaDeathsTotalToday
        coronaCasesTotalSoFar = coronaCasesTotalToday
        coronaDeathsTotalSoFar = coronaDeathsTotalToday

    # Generate maps
    draw.generateMaps(coronaCases, legendUnits = "Neue Coronafälle pro Tag", targetFolder = "../out/maps/cases/")
    draw.generateMaps(coronaDeaths, legendUnits = "Neue Coronatodesfälle pro Tag", targetFolder = "../out/maps/deaths/")
    draw.generateMaps(coronaCasesTotal, legendUnits = "Coronafälle gesamt", targetFolder = "../out/maps/casesTotal/")
    draw.generateMaps(coronaDeathsTotal, legendUnits = "Coronatodesfälle gesamt", targetFolder = "../out/maps/deathsTotal/")

    # Generate GIFs
    log.printProgressBar(0, 4, "Generating GIFs. Current GIF: covid-19 cases")
    caseMapFiles = map(lambda date: "../out/maps/cases/" + date.replace('/', '-') + ".png", sortedDates)
    draw.generateGIF("../out/maps/cases.gif", caseMapFiles)
    
    log.printProgressBar(1, 4, "Generating GIFs. Current GIF: covid-19 deaths")
    deathMapFiles = map(lambda date: "../out/maps/deaths/" + date.replace('/', '-') + ".png", sortedDates)
    draw.generateGIF("../out/maps/deaths.gif", deathMapFiles)

    log.printProgressBar(2, 4, "Generating GIFs. Current GIF: covid-19 cases total")
    totalCaseMapFiles = map(lambda date: "../out/maps/casesTotal/" + date.replace('/', '-') + ".png", sortedDates)
    draw.generateGIF("../out/maps/casesTotal.gif", totalCaseMapFiles)
    
    log.printProgressBar(3, 4, "Generating GIFs. Current GIF: covid-19 deaths total")
    totalDeathMapFiles = map(lambda date: "../out/maps/deathsTotal/" + date.replace('/', '-') + ".png", sortedDates)
    draw.generateGIF("../out/maps/deathsTotal.gif", totalDeathMapFiles)

    log.printProgressBar(4, 4, "Generating GIFs. Done!")
