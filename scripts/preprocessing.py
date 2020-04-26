import csv
import log


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