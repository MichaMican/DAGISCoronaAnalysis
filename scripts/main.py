from load import loadCoronaCases, loadGoogleTrendsData
from plot import plotCaseGoogleTrends
from download import downloadCoronaCases, downloadGoogleTrendsData
import os

def main():
    createAllDir()
    downloadCoronaCases()
    coronaCases = loadCoronaCases()
    downloadGoogleTrendsData(coronaCases.keys())
    googleTrends = loadGoogleTrendsData()
    plotCaseGoogleTrends(coronaCases, googleTrends)

def createAllDir():
    try:
        os.mkdir("../dat/")
    except FileExistsError:
        pass

    try:
        os.mkdir("../dat/temp/")
    except FileExistsError:
        pass

    try:
        os.mkdir("../dat/temp/")
    except FileExistsError:
        pass

    try:
        os.mkdir("../dat/temp/googleTrends/")
    except FileExistsError:
        pass

    try:
        os.mkdir("../out/")
    except FileExistsError:
        pass

    try:
        os.mkdir("../out/caseNumberHistoryPerCountry/")
    except FileExistsError:
        pass

main()