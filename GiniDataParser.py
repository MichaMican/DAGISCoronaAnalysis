import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import datetime
import os

def main():
    createDir()
    dataArray = readCsv()
    dataDictionary = groupByCountry(dataArray)
    print("We have " + str(len(dataDictionary)) + " countries loaded")


def createDir():
    try:
        os.mkdir("./out/")
    except FileExistsError:
        pass

    try:
        os.mkdir("./out/groupedGiniData/")
    except FileExistsError:
        pass

def readCsv():
    resultArray = []
    with open('./dat/(2)IncomeDistributionDatabase_OECD.csv') as csv_file:

        csv_reader = csv.DictReader(csv_file, delimiter=',')

        for row in csv_reader:
            resultArray.append(row)

    return resultArray

def groupByCountry(dataArray):
    groupedDict = {}
    for row in dataArray:
        try:
            groupedDict[row["LOCATION"]].append(row)
        except KeyError:
            groupedDict[row["LOCATION"]] = []
            groupedDict[row["LOCATION"]].append(row)
        except Exception:
            print("Error while grouping")

    return groupedDict

main()