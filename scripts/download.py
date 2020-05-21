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
import dload
import pandas as pd


def request(source, target):
    log.log("Downloading...")
    result = requests.get(source)
    open(target, "wb").write(result.content)
    log.log("Download finished!")

def downloadWorldPopulation():
    source = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv"
    target = "../dat/temp/population.csv"
    request(source, target)

def downloadCoronaCases():
    source = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    target = "../dat/temp/coronaCases.csv"
    request(source, target)

def downloadCountryBorders():
    source = "https://opendata.arcgis.com/datasets/252471276c9941729543be8789e06e12_0.zip"
    dload.save_unzip(source, extract_path='../dat/temp/countryBorders', delete_after=True)

def downloadGiniCoefficient():
    source = "https://api.worldbank.org/v2/en/indicator/SI.POV.GINI?downloadformat=csv"
    path = "../dat/temp/giniData/"
    target = path + "GiniData.zip"
    request(source, target)

    with zipfile.ZipFile(target, 'r') as zipObj:
        zipObj.extractall(path)

    if(os.path.exists(path + "WorldBankGiniIndex.csv")):
        os.remove(path + "WorldBankGiniIndex.csv")

    for filename in os.listdir(path):
        if(filename == "API_SI.POV.GINI_DS2_en_csv_v2_1068836.csv"):
            try:
                os.rename(path + "API_SI.POV.GINI_DS2_en_csv_v2_1068836.csv", path + "WorldBankGiniIndex.csv")
            except Exception as error:
                log.logError("Renaming failed - Error: " + str(error))
        else:
            try:
                os.remove(path + filename)
            except Exception:
                log.logError("Removing unused .csv tables failed - Error")

    log.log("Deleting first 4 rows of WorldBankGiniIndex.csv ...")
    dataFrame = pd.read_csv(path + "WorldBankGiniIndex.csv", skiprows=4)
    dataFrame.to_csv(path + "WorldBankGiniIndex.csv", index=False)
    log.log("Deleting rows finished!")


def downloadHealthSpendingPerCapita():
    source = "http://apps.who.int/gho/athena/api/GHO/GHED_CHE_pc_US_SHA2011/?format=csv"
    target = "../dat/temp/healthSpendingPerCapita.csv"
    request(source, target)


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
        if geoId == "GB":
            geoIdForGoolge = "GB-ENG"

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


