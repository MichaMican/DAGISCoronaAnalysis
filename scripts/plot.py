from log import printProgressBar
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import datetime
import numpy as np

def plotCaseGoogleTrends(coronaCaseDataDict, googleTrendsDataDict):
    maxLength = len(coronaCaseDataDict)
    progress = 1
    for countryKey in coronaCaseDataDict:
        printProgressBar(progress, maxLength, "Saving plot for " + countryKey)
        xCorona = []
        yCorona = []

        for countryDict in coronaCaseDataDict[countryKey]:
            xCorona.append(datetime.date(int(countryDict["year"]), int(countryDict["month"]), int(countryDict["day"])))
            yCorona.append(int(countryDict["cases"]))

        fig, ax1 = plt.subplots()
        ax1.bar(xCorona, yCorona)
        ax1.xaxis_date()

        fig.autofmt_xdate()
        ax1.set_xlim([datetime.date(2019, 12, 1), datetime.date.today()])

        ax1.set_ylabel('New cases')
        ax1.set_xlabel('Date')

        if coronaCaseDataDict[countryKey][0]["geoId"] in googleTrendsDataDict.keys():
            
            xTrends = []
            yTrends = []

            for dayData in googleTrendsDataDict[coronaCaseDataDict[countryKey][0]["geoId"]]:
                datetimeTrends = datetime.datetime.strptime(dayData["date"], "%Y-%m-%d")
                xTrends.append(datetimeTrends.date())
                yTrends.append(int(dayData["/m/01cpyy"]))
            
            ax2 = ax1.twinx() 
            ax2.plot_date(xTrends, yTrends, linestyle='solid', marker='None', color='red')
            ax2.set_ylabel('Interest in %')
            
            ax1.yaxis.label.set_color("blue")
            ax1.tick_params(axis='y', colors="blue")

            ax2.yaxis.label.set_color("red")
            ax2.tick_params(axis='y', colors="red")

        figure = plt.gcf()
        figure.set_size_inches(19.2, 10.8)
        plt.savefig("../out/caseNumberHistoryPerCountry/" + countryKey +
                    ".png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
        plt.clf()
        plt.close()
        progress += 1
