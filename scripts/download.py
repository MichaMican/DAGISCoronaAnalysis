import requests
import os
from pytrends.request import TrendReq
from log import printProgressBar
import log
import datetime


def downloadCoronaCases():
    source = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    target = "../dat/temp/coronaCases.csv"
    log.log("Downloading...")
    result = requests.get(source)
    open(target, "wb").write(result.content)
    log.log("Download finished!")


def downloadGoogleTrendsData(geoIdArray):
    pytrend = TrendReq()
    maxLength = len(geoIdArray)
    progress = 0
    for geoId in geoIdArray:
        printProgressBar(progress, maxLength,
                         "Downloading Google Trends data for " + geoId)
        if(geoId != "" and geoId != None and geoId != "N/A"):
            try:
                pytrend.build_payload(kw_list=['/m/01cpyy'], timeframe='2019-11-01 ' + datetime.datetime.now().strftime("%Y-%m-%d"), geo='DE')
                interest_over_time_df = pytrend.interest_over_time()
                interest_over_time_df.to_csv("../dat/temp/googleTrends/" + geoId + ".csv")
            except Exception as error:
                log.logWarning("Downloading googletrends for geoId " + geoId + " failed - Errormessage was: " + error)
        progress += 1


