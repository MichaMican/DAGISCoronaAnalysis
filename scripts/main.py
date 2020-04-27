from load import loadCoronaCases, loadGoogleTrendsData, loadGiniData
from plot import plotCaseGoogleTrends, plotGiniData
from download import downloadCoronaCases, downloadGoogleTrendsData, downloadGiniCoefficient
from preprocessing import saveGiniGroupedDataToCsv
import log
import os

scriptPath = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptPath)
log.logInfo("Scriptpath: " + str(scriptPath))

def main():
    log.logInfo("Creating Directories")
    createAllDir()
    log.logInfo("Downloading corona cases")
    downloadCoronaCases()
    log.logInfo("Downloading gini data")
    downloadGiniCoefficient()
    log.logInfo("Loading corona cases into memory")
    coronaCases = loadCoronaCases()
    log.logInfo("Downloading Google trends data")
    downloadGoogleTrendsData(coronaCases.keys())
    log.logInfo("Loading Google trends data into memory")
    googleTrends = loadGoogleTrendsData()
    log.logInfo("Loading Gini-Coefficient data into memory")
    giniCoefficient = loadGiniData()
    log.logInfo("Creating Google trends Plots")
    plotCaseGoogleTrends(coronaCases, googleTrends)
    log.logInfo("Creating Gini-Coefficient Plots")
    plotGiniData(giniCoefficient)
    log.logInfo("Creating Gini-Coefficient csv Table")
    saveGiniGroupedDataToCsv(giniCoefficient)

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

    try:
        os.makedirs("../dat/temp/giniData/")
    except FileExistsError:
        pass

main()