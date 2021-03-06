import log
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import datetime
import numpy as np
import pycountry
import math


def plotTopFlopGiniCoefficientOverview(newestGiniCoefficientPerCountryDict):

    sortedCountryKeys = sorted(newestGiniCoefficientPerCountryDict,key=lambda e: newestGiniCoefficientPerCountryDict[e]["value"], reverse=True)

    rankingPos = 0
    for countryKey in sortedCountryKeys:

        if rankingPos < 5 or rankingPos > (len(sortedCountryKeys) - 1 - 5):

            red = hex(255)
            green = hex(int(math.floor(rankingPos * 1/10 * 255)))
            blue = hex(0)

            if rankingPos > (len(sortedCountryKeys) - 1 - 5):

                red = hex(int(math.floor((len(sortedCountryKeys) - rankingPos) * 1/8 * 255)))
                green = hex(255)
                blue = hex(0)
                

            countryData = newestGiniCoefficientPerCountryDict[countryKey]
            plt.barh(pycountry.countries.get(alpha_2=countryKey).name + " (" + countryData["lastYearWithData"] + ")", countryData["value"], color="#"+str(red).replace("0x","").zfill(2)+str(green).replace("0x","").zfill(2)+str(blue).replace("0x","").zfill(2))

        elif rankingPos == 5:
            plt.barh("...", 0)

        rankingPos += 1

    figure = plt.gcf()
    figure.set_size_inches(19.2, 10.8)
    title = "Best and worst Gini-Coefficient in the world"
    plt.title(title)
    plt.savefig("../out/giniCoefficient/topFlopList.png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
    plt.clf()
    plt.close()

    

def plotTopFlopHealthSpendingCoronaCases(topFlopCountryData, population):

    topAndFlopArray = []
    topAndFlopArray.extend(topFlopCountryData["top"])
    topAndFlopArray.extend(topFlopCountryData["flop"])


    place = 0
    for countryData in topAndFlopArray:

        x = []
        totalCases = []
        yCasesPer100kCitizens = []
        totalDeaths = []
        yDeathsPer100kCitizens = []
        countryPopulation = population[countryData["alpha_2"]] * 1000

        if countryPopulation > 0:

            sortedCasesCountryData = sorted(countryData["coronaCases"], key=lambda e: int(
            e["year"]) * 10000 + int(e["month"]) * 100 + int(e["day"]))


            for caseData in sortedCasesCountryData:
                x.append(datetime.date(int(caseData["year"]), int(
                    caseData["month"]), int(caseData["day"])))
                
                if len(totalCases) > 0:
                    totalCases.append(totalCases[-1] + int(caseData["cases"]))
                else:
                    totalCases.append(int(caseData["cases"]))

                if len(totalDeaths) > 0:
                    totalDeaths.append(totalDeaths[-1] + int(caseData["deaths"]))
                else:
                    totalDeaths.append(int(caseData["deaths"]))

                yCasesPer100kCitizens.append((totalCases[-1]/countryPopulation) * 100000)
                yDeathsPer100kCitizens.append((totalDeaths[-1]/countryPopulation) * 100000)

            red = hex(85 * place)
            green = hex(255)
            blue = hex(0)

            if(place > 2):
                red = hex(255)
                green = hex(85 * (place%3))
                blue = hex(0)

            colorString = "#"+str(red).replace("0x","").zfill(2)+str(green).replace("0x","").zfill(2)+str(blue).replace("0x","").zfill(2)

            countryObj = pycountry.countries.get(alpha_2=countryData["alpha_2"])

            plt.figure(1)
            plt.plot_date(x, yCasesPer100kCitizens, color=colorString, linestyle='solid', marker='None', label=countryObj.name)
            plt.figure(2)
            plt.plot_date(x, yDeathsPer100kCitizens, color=colorString, linestyle='solid', marker='None', label=countryObj.name)
            place += 1

        else:
            log.logError("There is no countryPopulation data for " + countryData.alpha_2)

    plt.figure(1)
    figure = plt.gcf()
    figure.set_size_inches(19.2, 10.8)
    title = "cases per 100k of top and flop 3 per head spender"
    plt.title(title)
    plt.legend()
    plt.savefig("../out/healthSpending/cases.png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
    plt.clf()
    plt.close()

    plt.figure(2)
    figure = plt.gcf()
    figure.set_size_inches(19.2, 10.8)
    title = "deaths per 100k of top and flop 3 per head spender"
    plt.title(title)
    plt.legend()
    plt.savefig("../out/healthSpending/deaths.png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
    plt.clf()
    plt.close()


def plotCaseGoogleTrends(coronaCaseDataDict, googleTrendsDataDict):
    maxLength = len(coronaCaseDataDict)
    progress = 1
    for countryKey in coronaCaseDataDict:
        log.printProgressBar(progress, maxLength,
                             "Saving plot for " + countryKey)
        xCorona = []
        yCorona = []
        yCoronaTotal = []

        sortedCases = sorted(coronaCaseDataDict[countryKey], key=lambda e: int(
            e["year"]) * 10000 + int(e["month"]) * 100 + int(e["day"]))

        for countryDict in sortedCases:
            xCorona.append(datetime.date(int(countryDict["year"]), int(
                countryDict["month"]), int(countryDict["day"])))
            yCorona.append(int(countryDict["cases"]))
            if(len(yCoronaTotal) > 0):
                yCoronaTotal.append(
                    yCoronaTotal[len(yCoronaTotal) - 1] + int(countryDict["cases"]))
            else:
                yCoronaTotal.append(int(countryDict["cases"]))

        fig, ax1 = plt.subplots()

        ax1.bar(xCorona, yCorona)
        ax1.xaxis_date()

        fig.autofmt_xdate()

        ax1.set_xlim([datetime.date(2019, 12, 1), datetime.date.today()])
        ax1.set_ylabel('New cases')
        ax1.set_xlabel('Date')

        ax1.yaxis.label.set_color("blue")
        ax1.tick_params(axis='y', colors="blue")

        ax3 = ax1.twinx()
        ax3.plot_date(xCorona, yCoronaTotal, linestyle='solid',
                      marker='None', color='green')
        ax3.set_ylabel('total cases')

        ax3.yaxis.label.set_color("green")
        ax3.tick_params(axis='y', colors="green")

        if coronaCaseDataDict[countryKey][0]["countryCode"] in googleTrendsDataDict.keys():

            xTrends = []
            yTrends = []

            for dayData in googleTrendsDataDict[coronaCaseDataDict[countryKey][0]["countryCode"]]:
                datetimeTrends = datetime.datetime.strptime(
                    dayData["date"], "%Y-%m-%d")
                xTrends.append(datetimeTrends.date())
                yTrends.append(int(dayData["/m/01cpyy"]))

            ax2 = ax1.twinx()
            ax2.plot_date(xTrends, yTrends, linestyle='solid',
                          marker='None', color='red')
            ax2.set_ylabel('Interest in %')

            ax2.yaxis.label.set_color("red")
            ax2.tick_params(axis='y', colors="red")

            ax3.spines["right"].set_position(("axes", 1.05))

        figure = plt.gcf()
        figure.set_size_inches(19.2, 10.8)
        title = coronaCaseDataDict[countryKey][0]["areaName"]
        plt.title(title)
        plt.savefig("../out/caseNumberHistoryPerCountry/" + countryKey +
                    ".png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
        plt.clf()
        plt.close()
        progress += 1


def plotGiniData(giniDataDict):
    maxLength = len(giniDataDict)
    progress = 1

    for countryKey in giniDataDict:
        giniValue = []
        years = []
        log.printProgressBar(progress, maxLength, "Saving plot for " + countryKey)

        for countryGiniData in giniDataDict[countryKey]:
            for year in countryGiniData.keys():
                if year.isdecimal():
                    if(countryGiniData[year] != ''):
                        giniValue.append(float(countryGiniData[year]))
                        years.append(int(year))

        if len(giniValue) > 0:
            #plt.plot(years, giniValue, marker="o", linestyle= "solid")
            #bildet den den aktuellsten wert ab
            #plt.bar(years[len(years) - 1], giniValue[len(giniValue) - 1])
            #bildet alle werte ab
            plt.bar(years, giniValue)
            plt.ylabel('Gini-Coefficient')
            plt.xlabel('Year')
            # evtl dynamisch setzen?
            plt.xlim([1960, 2020])
            plt.ylim([0, 100])
            figure = plt.gcf()
            figure.set_size_inches(19.2, 10.8)
            if(countryKey == ""):
                plt.savefig("../out/giniCoefficient/noCountryCode_Gini.png",
                            bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
            else:
                plt.savefig("../out/giniCoefficient/" + countryKey +
                            "_Gini.png", bbox_inches=Bbox(np.array([[0, 0], [19.2, 10.8]])))
            # plt.show()
            plt.clf()
            plt.close()

        progress += 1
