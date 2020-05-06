from pathlib import Path
import plot
import draw
import load
import download
import preprocessing
import log
import os

scriptPath = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptPath)
log.logInfo("Scriptpath: " + str(scriptPath))

def main():

    log.logInfo("Creating Directories")
    createAllDir()

    log.logInfo("Downloading corona cases")
    download.downloadCoronaCases()
    log.logInfo("Loading corona cases into memory")
    coronaCases = load.loadCoronaCases()
    coronaCasesByDay = load.loadCoronaCases("date")

    log.logInfo("Downloading world popoulation")
    download.downloadWorldPopulation()
    log.logInfo("Loading world popoulation into memory")
    population = load.loadPopulationGroupedByYear()
    
    log.logInfo("Downloading health spending data")
    download.downloadHealthSpendingPerCapita()
    log.logInfo("Loading health spending data into memory")
    healthSpendingDict = load.loadHealthSpendingPerCapita()
    log.logInfo("Plotting topFlop health spender")
    plot.plotTopFlopHealthSpendingCoronaCases(preprocessing.getTopFlopCountries(coronaCases, healthSpendingDict, 3), preprocessing.extractCountryPopulationForYear(population, "2020"))

    log.logInfo("Downloading country borders")
    download.downloadCountryBorders()
    log.logInfo("Downloading Google trends data")
    download.downloadGoogleTrendsData(coronaCases.keys())
    log.logInfo("Loading Google trends data into memory")
    googleTrends = load.loadGoogleTrendsData()
    log.logInfo("Creating Plots")
    plot.plotCaseGoogleTrends(coronaCases, googleTrends)
    log.logInfo("Drawing corona case maps")
    preprocessing.generateCoronaCaseWorldMaps(coronaCasesByDay)

    log.logInfo("Downloading Gini-Coefficient")
    download.downloadGiniCoefficient()
    
    log.logInfo("Loading Gini-Coefficient data into memory")
    giniCoefficient = load.loadGiniData()
    log.logInfo("Creating Gini-Coefficient Plots")
    plot.plotGiniData(giniCoefficient)
    log.logInfo("Creating Gini-Coefficient grouped dictionary")
    newestGiniCoefficientDict = preprocessing.getNewestGiniCoefficientDict(giniCoefficient)
    log.logInfo("Creating top flop gini coef. plot")
    plot.plotTopFlopGiniCoefficientOverview(newestGiniCoefficientDict)
    log.logInfo("Creating gini coef map")
    preprocessing.generateGiniCoefficientMap(newestGiniCoefficientDict)
    log.logInfo("Creating gini-cases coef map")
    preprocessing.generateGiniCoronaMap(coronaCases, newestGiniCoefficientDict, preprocessing.extractCountryPopulationForYear(population, "2020"))
    log.logInfo("Creating health spending per capita map")
    preprocessing.generateHealthSpendingMap(healthSpendingDict)

def createDir(dirname):
    Path(dirname).mkdir(parents = True, exist_ok = True)

def createDirs(dirnames):
    for dirname in dirnames:
        createDir(dirname)

def createAllDir():
    createDirs([
        "../dat/temp/",
        "../dat/temp/googleTrends/",
        "../dat/temp/countryBorders/",
        "../dat/temp/giniData/",
        "../out/",
        "../out/caseNumberHistoryPerCountry/",
        "../out/maps/",
        "../out/maps/cases/",
        "../out/maps/deaths/",
        "../out/maps/giniCaseCoef/",
        "../out/maps/giniDeathCoef/",
        "../out/healthSpending/",
        "../out/giniCoefficient/"
    ])

main()