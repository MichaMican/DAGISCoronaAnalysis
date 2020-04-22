import os

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