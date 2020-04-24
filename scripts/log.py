import os
import datetime
import sys

logFolder = "../log/"

class bcolors:
    INFO = '\033[94m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def checkPath():
    exists = os.path.exists(logFolder)

    if not exists:
        print(bcolors.INFO + "[INFO] " + "A log folder was created here: " + os.path.abspath(logFolder) + bcolors.ENDC)
        os.makedirs(logFolder)


def logError(logMessage):
    writeLog(logMessage, 3)
    print(bcolors.ERROR + "[ERROR] " + logMessage + bcolors.ENDC)

def logWarning(logMessage):
    writeLog(logMessage, 2)
    print(bcolors.WARNING + "[WARNING] " + logMessage)

def logInfo(logMessage):
    writeLog(logMessage, 1)
    print(bcolors.INFO + "[INFO] " + logMessage + bcolors.ENDC)

def log(logMessage):
    writeLog(logMessage, 0)
    print(logMessage)


#type 0 = normal; 1 = Info; 2 = warning; 3 = error;
def writeLog(logMessage, logType=0):
    checkPath()
    typeString = " "
    if logType == 1:
        typeString = " [INFO] "
    elif logType == 2:
        typeString = " [WARNING] "
    elif logType == 3:
        typeString = " [ERROR] "

        with open(logFolder  + "ERROR" + datetime.datetime.now().strftime("%Y-%m-%d")+".log", "a+") as file:
            file.write(datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + typeString + "- " + logMessage + "\n")

    with open(logFolder + datetime.datetime.now().strftime("%Y-%m-%d")+".log", "a+") as file:
        file.write(datetime.datetime.now().strftime("%d.%m.%Y - %H:%M:%S") + typeString + "- " + logMessage + "\n")

def printProgressBar(progress, maxLength, message=""):
    os.system('cls')
    loadingStr = "["
    for x in range(30):
        if((progress/maxLength) * 30 >= x):
            loadingStr += "█"
        else:
            loadingStr += "-"

    loadingStr += "]"
    print(loadingStr)
    print("Finished: "+str(progress)+"/"+str(maxLength))
    print(message)