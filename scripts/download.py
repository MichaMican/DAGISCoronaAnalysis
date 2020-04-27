import requests
import os
import csv
from pytrends.request import TrendReq
import pytrends
from log import printProgressBar
import zipfile
import log
import datetime
import time
import pandas as pd


def downloadCoronaCases():
    #evtl. für requests ne extra funktion aufmachen @zukunftsphilipp
    source = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    target = "../dat/temp/coronaCases.csv"
    log.log("Downloading...")
    result = requests.get(source)
    open(target, "wb").write(result.content)
    log.log("Download finished!")

def downloadGiniCoefficient():
    source = "https://api.worldbank.org/v2/en/indicator/SI.POV.GINI?downloadformat=csv"
    path = "../dat/temp/giniData/"
    target = path + "GiniData.zip"
    log.log("Downloading...")
    result = requests.get(source)
    open(target, "wb").write(result.content)
    log.log("Download finished!")

    with zipfile.ZipFile(target, 'r') as zipObj:
        zipObj.extractall(path)
    #an der stelle die csv scho umbenennen!!!

    #!!funktioniert nur wenn worldbankginiindex.csv vorher schon in dem ordner ist ansonsten läuft das script leer!!
    for filename in os.listdir(path):
        if(filename == "WorldBankGiniIndex.csv"):
            log.log("Deleting first 4 rows of WorldBankGiniIndex.csv ...")
            dataFrame = pd.read_csv(path + "WorldBankGiniIndex.csv", skiprows=4)
            dataFrame.to_csv(path + "WorldBankGiniIndex.csv", index=False)
            log.log("Deleting rows finished!")

        elif(filename == "API_SI.POV.GINI_DS2_en_csv_v2_988343.csv"):
            try:
                os.rename(path + "API_SI.POV.GINI_DS2_en_csv_v2_988343.csv", path + "WorldBankGiniIndex.csv")
            except Exception:
                os.remove(path + "WorldBankGiniIndex.csv")
                os.rename(path + "API_SI.POV.GINI_DS2_en_csv_v2_988343.csv", path + "WorldBankGiniIndex.csv")
                log.logInfo("The .csv file name is already assigned - deleting the old file")
        else:
            try:
                os.remove(path + filename)
            except Exception:
                log.logError("Removing unused .csv tables failed - Error")

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


