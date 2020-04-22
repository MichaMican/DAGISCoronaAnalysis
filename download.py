import requests
import os

source = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
target = "dat/temp/coronaCases.csv"

try:
    os.mkdir("./dat/")
except FileExistsError:
    pass

try:
    os.mkdir("./dat/temp/")
except FileExistsError:
    pass

print("Downloading...")
result = requests.get(source)
open(target, "wb").write(result.content)
print("Download finished!")