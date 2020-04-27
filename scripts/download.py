import requests
import os
from pytrends.request import TrendReq
import pytrends
from log import printProgressBar
import log
import datetime
import time
import dload

def downloadWorldPopulation():
    source = "https://population.un.org/wpp/Download/Files/1_Indicators%20(Standard)/CSV_FILES/WPP2019_TotalPopulationBySex.csv"
    target = "../dat/temp/population.csv"
    log.log("Downloading...")
    result = requests.get(source)
    open(target, "wb").write(result.content)
    log.log("Download finished!")

def downloadCoronaCases():
    source = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
    target = "../dat/temp/coronaCases.csv"
    log.log("Downloading...")
    result = requests.get(source)
    open(target, "wb").write(result.content)
    log.log("Download finished!")

def downloadGiniCoefficient():
    source = "http://api.worldbank.org/v2/en/indicator/SI.POV.GINI?downloadformat=csv"
    dload.save_unzip(source, extract_path='../dat/temp', delete_after=True)
    # Die ersten Zeilen des neu heruntergeladenen .csv Files müssen gelöscht werden!!! -> Sonst Error bei Grouping
    # Siehe ./dat/temp/API_SI.POV.GINI_DS2_en_csv_v2_988343.csv
    # try:
    #     os.rename("../dat/temp/API_SI.POV.GINI_DS2_en_csv_v2_988343.csv", "../dat/temp/WorldBankGiniIndex.csv")
    # except Exception:
    #     os.remove("../dat/temp/WorldBankGiniIndex.csv")
    #     os.rename("../dat/temp/API_SI.POV.GINI_DS2_en_csv_v2_988343.csv", "../dat/temp/WorldBankGiniIndex.csv")
    #     log.logInfo("The .csv file name is already assigned - deleting the old file")

    try:
        os.remove("../dat/temp/Metadata_Country_API_SI.POV.GINI_DS2_en_csv_v2_988343.csv")
        os.remove("../dat/temp/Metadata_Indicator_API_SI.POV.GINI_DS2_en_csv_v2_988343.csv")
    except Exception as err:
        log.logError("Removing unused .csv tables failed - Error: " + err)


def downloadHealthSpendingPerCapita():
    source = "http://apps.who.int/gho/athena/api/GHO/GHED_CHE_pc_US_SHA2011/?format=csv"
    target = "../dat/temp/healthSpendingPerCapita.csv"
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


