from load import loadCoronaCases, loadGoogleTrendsData
from plot import plotCaseGoogleTrends
from download import downloadCoronaCases, downloadGoogleTrendsData
import log
import os

def main():
    log.logInfo("Creating Directories")
    createAllDir()
    log.logInfo("Downloading corona cases")
    downloadCoronaCases()
    log.logInfo("Loading corona cases into memor")
    coronaCases = loadCoronaCases()
    #log.logInfo("Downloading Google trends data")
    #downloadGoogleTrendsData(coronaCases.keys())
    log.logInfo("Loading Google trends data into memory")
    googleTrends = loadGoogleTrendsData()
    log.logInfo("Creating Plots")
    plotCaseGoogleTrends(coronaCases, googleTrends)

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