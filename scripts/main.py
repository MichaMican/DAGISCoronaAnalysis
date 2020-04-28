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

    #log.logInfo("Downloading corona cases")
    #download.downloadCoronaCases()
    log.logInfo("Loading corona cases into memory")
    coronaCases = load.loadCoronaCases()

    #download.downloadWorldPopulation()
    population = load.loadPopulationGroupedByYear()

    #download.downloadHealthSpendingPerCapita()
    healthSpendingDict = load.loadHealthSpendingPerCapita()

    plot.plotTopFlopHealthSpendingCoronaCases(preprocessing.getTopFlopCountries(coronaCases, healthSpendingDict, 3), preprocessing.extractCountryPopulationForYear(population, "2020"))

    log.logInfo("Downloading country borders")
    download.downloadCountryBorders()
    log.logInfo("Downloading Google trends data")
    download.downloadGoogleTrendsData(coronaCases.keys())
    log.logInfo("Loading Google trends data into memory")
    googleTrends = load.loadGoogleTrendsData()
    log.logInfo("Creating Plots")
    plot.plotCaseGoogleTrends(coronaCases, googleTrends)
    # log.logInfo("Drawing maps")
    # draw.generateWorldMaps()
    
    log.logInfo("Loading Gini-Coefficient data into memory")
    giniCoefficient = load.loadGiniData()
    log.logInfo("Creating Gini-Coefficient Plots")
    plot.plotGiniData(giniCoefficient)
    log.logInfo("Creating Gini-Coefficient csv Table")
    preprocessing.saveGiniGroupedDataToCsv(giniCoefficient)

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
        "../out/",
        "../out/caseNumberHistoryPerCountry/",
        "../out/maps/",
        "../out/healthSpending/"
    ])

main()