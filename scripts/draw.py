from shapefile import Reader as ShapeFileReader
from glob import glob as getMatchingFiles
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, Normalize
from load import loadCoronaCases
import log


# Open shape file from folder
def getShapeFileReader(folder):
    shapeFiles = getMatchingFiles(folder + "*.shp")
    return ShapeFileReader(shapeFiles[0])

# Associate the column names with column numbers
def getFieldIDs(sf):
    fieldIDs = {}

    for i, field in enumerate(sf.fields, start = -1):
        # Ignore 'DeletionFlag'
        if i >= 0:
            fieldIDs[field[0]] = i
    
    return fieldIDs


def drawShape(shape, color):
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
        plt.fill(x, y, c = color)


def getMaxValueOnDay(dataOnDay):
    maxValue = 0

    for value in dataOnDay.values():
        maxValue = max(maxValue, value)
    
    return maxValue


def getLinearNormalizer(min, max):
    return Normalize(vmin = min, vmax = max)


def generateMaps(data, targetFolder = "../out/maps/", mapShpPath = "../dat/temp/countryBorders/", shapeIDFieldName = 'ISO', legendUnits = None, getNormalizer = getLinearNormalizer, colorMap = 'Reds', dpi = 300):
    # Read border shapefile
    sf = getShapeFileReader(mapShpPath)
    fieldIDs = getFieldIDs(sf)

    # Get number of maps to generate
    mapCount = len(data)
    
    currentMapNum = 0
    for mapId, dataOnDay in data.items():
        # Update progress bar
        currentMapNum = currentMapNum + 1
        log.printProgressBar(currentMapNum, mapCount, "Generating maps. Current map: " + mapId)

        # Determine max cases and deaths on given day
        maxValue = getMaxValueOnDay(dataOnDay)

        # Create figure
        fig = plt.figure()
        plt.tight_layout()
        plt.axis("off")
        cmap = plt.get_cmap(colorMap, 100)


        for shapeRecord in sf.iterShapeRecords():
            shape = shapeRecord.shape
            record = shapeRecord.record
            shapeID = record[fieldIDs[shapeIDFieldName]]

            # Get cases and deaths for corrent country, on current day
            value = 0
            if shapeID in dataOnDay:
                value = dataOnDay[shapeID]
            
            # Determine draw color
            color = cmap(value)

            # Draw shape
            drawShape(shape, color)
        
        sm = plt.cm.ScalarMappable(cmap = cmap, norm = getNormalizer(0, maxValue))
        sm.set_array([])
        plt.colorbar(sm, orientation = 'horizontal', label = legendUnits)

        # Display
        plt.savefig(
            targetFolder + mapId.replace('/', '-') + ".png",
            dpi = dpi,
            bbox_inches = 'tight',
            #pad_inches = 0,
            transparent = False
        )
        
        plt.close(fig)


def sortByCountry(coronaCasesOnDay, key = "cases"):
    coronaCasesByCountry = {}

    for coronaCases in coronaCasesOnDay:
        iso = coronaCases["geoId"]
        coronaCasesByCountry[iso] = int(coronaCases[key])
    
    return coronaCasesByCountry


def generateCoronaCaseWorldMaps():
    # Get daily values
    coronaCasesByDay = loadCoronaCases("dateRep")

    # Map daily cases to their countries format
    coronaCases = {}
    for day, coronaCasesOnDay in coronaCasesByDay.items():
        coronaCases[day] = sortByCountry(coronaCasesOnDay)

    generateMaps(coronaCases, legendUnits = "New covid-19 cases")