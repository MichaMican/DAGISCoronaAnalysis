import plot
import load
import download
import preprocessing
import log
import os

scriptPath = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptPath)
log.logInfo("Scriptpath: " + str(scriptPath))

def main():

    download.downloadHealthSpendingPerCapita()
    healthSpendingDict = load.loadHealthSpendingPerCapita()

    log.logInfo("Creating Directories")
    createAllDir()
    log.logInfo("Downloading corona cases")
    download.downloadCoronaCases()
    log.logInfo("Loading corona cases into memor")
    coronaCases = load.loadCoronaCases()
    log.logInfo("Downloading Google trends data")
    download.downloadGoogleTrendsData(coronaCases.keys())
    log.logInfo("Loading Google trends data into memory")
    googleTrends = load.loadGoogleTrendsData()
    log.logInfo("Creating Plots")
    plot.plotCaseGoogleTrends(coronaCases, googleTrends)
    
    log.logInfo("Loading Gini-Coefficient data into memory")
    giniCoefficient = load.loadGiniData()
    log.logInfo("Creating Gini-Coefficient Plots")
    plot.plotGiniData(giniCoefficient)
    log.logInfo("Creating Gini-Coefficient csv Table")
    preprocessing.saveGiniGroupedDataToCsv(giniCoefficient)

def createAllDir():

    try:
        os.makedirs("../dat/temp/")
    except FileExistsError:
        pass

    try:
        os.makedirs("../dat/temp/googleTrends/")
    except FileExistsError:
        pass

    try:
        os.makedirs("../out/caseNumberHistoryPerCountry/")
    except FileExistsError:
        pass

main()