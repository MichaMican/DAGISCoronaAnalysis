import os
import datetime
import sys

logFolder = "../log/"

def checkPath():
    exists = os.path.exists(logFolder)

    if not exists:
        print("[INFO] " + "A log folder was created here: " + os.path.abspath(logFolder))
        os.makedirs(logFolder)


def logError(logMessage):
    writeLog(logMessage, 3)
    print("[ERROR] " + logMessage, file=sys.stderr)

def logWarning(logMessage):
    writeLog(logMessage, 2)
    print("[WARNING] " + logMessage)

def logInfo(logMessage):
    writeLog(logMessage, 1)
    print("[INFO] " + logMessage)

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
