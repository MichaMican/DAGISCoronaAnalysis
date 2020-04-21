import requests

source = "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv"
target = "dat/coronaCases.csv"

print("Downloading...")
result = requests.get(source)
open(target, "wb").write(result.content)
print("Download finished!")