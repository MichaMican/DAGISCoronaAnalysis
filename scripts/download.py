import requests
import os
from pytrends.request import TrendReq
import pytrends
from log import printProgressBar
import log
import datetime
import time


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
    tooManyRequestGeoIdArray = []
    for geoId in geoIdArray:
        printProgressBar(progress, maxLength,
                         "Downloading Google Trends data for " + geoId)

        geoIdForGoolge = geoId

        #special cases
        if geoId == "UK":
            geoIdForGoolge = "GB-ENG"
        if geoId == "EL":
            geoIdForGoolge = "GR"

        if(geoIdForGoolge != "" and geoIdForGoolge != None and geoIdForGoolge != "N/A"):
            try:
                pytrend.build_payload(kw_list=['/m/01cpyy'], timeframe='2019-11-01 ' + datetime.datetime.now().strftime("%Y-%m-%d"), geo=geoIdForGoolge)
                interest_over_time_df = pytrend.interest_over_time()
                interest_over_time_df.to_csv("../dat/temp/googleTrends/" + geoId + ".csv")
            except pytrends.exceptions.ResponseError as error:
                if error.response.status_code == 429:
                    log.logInfo("Google is mad at us that we make so much requests so were waiting for a minute before continuing (geoId will be redownloaded at the end)")
                    tooManyRequestGeoIdArray.append(geoId)
                    time.sleep(60)
                else:
                    log.logError("Downloading googletrends for geoId " + geoId + " failed - Errormessage was: " + str(error))

            except Exception as error:
                log.logWarning("Downloading googletrends for geoId " + geoId + " failed - Errormessage was: " + str(error))
        progress += 1
    if len(tooManyRequestGeoIdArray) > 0:
        downloadGoogleTrendsData(tooManyRequestGeoIdArray)


