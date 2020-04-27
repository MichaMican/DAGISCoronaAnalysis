from shapefile import Reader as ShapeFileReader
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from load import loadCoronaCases
import log


# Associate the column names with column numbers
def getFieldIDs(sf):
    fieldIDs = {}

    for i, field in enumerate(sf.fields, start = -1):
        # Ignore 'DeletionFlag'
        if i >= 0:
            fieldIDs[field[0]] = i
    
    return fieldIDs


def drawShape(shape, value):
    # Itarte through the parts of the shape
    for i in range(len(shape.parts)):
        partStart = shape.parts[i]

        # Get the ID of the last point of this part
        if i == len(shape.parts) - 1:
            partEnd = len(shape.points)
        else:
            partEnd = shape.parts[i + 1]
        
        # Draw this part
        x = [i[0] for i in shape.points[partStart:partEnd]]
        y = [i[1] for i in shape.points[partStart:partEnd]]
        plt.fill(x, y, to_hex((value, 0, value)))


def getMaxValuesOnDay(coronaCasesOnDay):
    maxCases = 0
    maxDeaths = 0

    for coronaCases in coronaCasesOnDay:
        maxCases = max(maxCases, int(coronaCases["cases"]))
        maxDeaths = max(maxDeaths, int(coronaCases["deaths"]))
    
    return (maxCases, maxDeaths)


def sortByCountry(coronaCasesOnDay):
    coronaCasesByCountry = {}

    for coronaCases in coronaCasesOnDay:
        iso = coronaCases["geoId"]

        countryCases = {}
        countryCases["cases"] = int(coronaCases["cases"])
        countryCases["deaths"] = int(coronaCases["deaths"])
        coronaCasesByCountry[iso] = countryCases
    
    return coronaCasesByCountry


def generateWorldMaps(targetFolder = "../out/maps/"):
    # Read border shapefile
    shp_path = "../dat/temp/countryBorders/UIA_World_Countries_Boundaries"
    sf = ShapeFileReader(shp_path)
    fieldIDs = getFieldIDs(sf)


    # Get daily values
    coronaCasesByDay = loadCoronaCases("dateRep")

    # Get number of days
    dayCount = len(coronaCasesByDay)
    
    currentDayNum = 0
    for day, coronaCasesOnDay in coronaCasesByDay.items():
        # Update progress bar
        currentDayNum = currentDayNum + 1
        log.printProgressBar(currentDayNum, dayCount, "Generating world maps. Current day: " + day)

        # Sort daily cases by country
        coronaCasesByCountry = sortByCountry(coronaCasesOnDay)

        # Determine max cases and deaths on given day
        maxCases, maxDeaths = getMaxValuesOnDay(coronaCasesOnDay)

        # Get name of day (used for filename)
        dayName = day.replace('/', '-')

        # Create figure
        figure = plt.figure()
        plt.tight_layout()
        plt.axis("off")


        for shapeRecord in sf.iterShapeRecords():
            shape = shapeRecord.shape
            record = shapeRecord.record
            iso = record[fieldIDs["ISO"]]
            area = record[fieldIDs["Shape__Are"]]

            # Get cases and deaths for corrent country, on current day
            cases = 0
            deaths = 0
            if iso in coronaCasesByCountry:
                coronaCases = coronaCasesByCountry[iso]
                cases = coronaCases["cases"]
                deaths = coronaCases["deaths"]
            
            # Determine draw color
            relativeCases = 0
            if maxCases != 0:
                relativeCases = cases / maxCases

            # Draw shape
            drawShape(shape, relativeCases)

        # Display
        plt.savefig(
            targetFolder + dayName + ".png",
            dpi = 300,
            transparent = False,
            bbox_inches = 'tight',
            pad_inches = 0
        )
        
        plt.close(figure)