from shapefile import Reader as ShapeFileReader
from glob import glob as getMatchingFiles
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex, Normalize
import imageio
from load import loadCoronaCases
import log


# Open shape file from folder
def __getShapeFileReader(folder):
    # Find first .shp file in given folder
    shapeFile = getMatchingFiles(folder + "*.shp")[0]
    return ShapeFileReader(shapeFile)

# Associate the column names with column numbers
def __getFieldIDs(sf):
    fieldIDs = {}

    for i, field in enumerate(sf.fields, start = -1):
        # Ignore 'DeletionFlag'
        if i >= 0:
            fieldIDs[field[0]] = i
    
    return fieldIDs


def __drawShape(shape, color):
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
        plt.fill(x, y, c = color, linewidth = 0)


def __getExtremeValuesForMap(dataInMap):
    maxValue = None
    minValue = None

    for value in dataInMap.values():
        if maxValue == None:
            maxValue = value
        else:
            maxValue = max(maxValue, value)

        if minValue == None:
            minValue = value
        else:
            minValue = min(minValue, value)
    
    return (minValue, maxValue)


def getLinearNormalizer(min, max):
    return Normalize(vmin = min, vmax = max)


def generateMaps(data, targetFolder = "../out/maps/", mapShpPath = "../dat/temp/countryBorders/", shapeIDFieldName = 'ISO', legendUnits = None, getNormalizer = getLinearNormalizer, colorMap = 'Reds', noDataColor = '#000000', dpi = 300):
    # Read border shapefile
    sf = __getShapeFileReader(mapShpPath)
    fieldIDs = __getFieldIDs(sf)

    # Get number of maps to generate
    mapCount = len(data)
    
    currentMapNum = 0
    for mapId, dataInMap in data.items():
        # Update progress bar
        log.printProgressBar(currentMapNum, mapCount, "Generating maps. Current map: " + mapId)
        currentMapNum = currentMapNum + 1

        # Determine max value for given map
        minValue, maxValue = __getExtremeValuesForMap(dataInMap)

        # Create figure
        fig = plt.figure()
        plt.title(mapId)
        plt.tight_layout()
        plt.axis('off')
        cmap = plt.get_cmap(colorMap)
        normalize = getNormalizer(minValue, maxValue)


        for shapeRecord in sf.iterShapeRecords():
            shape = shapeRecord.shape
            record = shapeRecord.record
            shapeID = record[fieldIDs[shapeIDFieldName]]

            # Get value for corrent country, for current map
            value = None
            if shapeID in dataInMap:
                value = normalize(dataInMap[shapeID])
            
            # Determine draw color
            color = noDataColor
            if value != None:
                color = cmap(value)

            # Draw shape
            __drawShape(shape, color)
        
        sm = plt.cm.ScalarMappable(cmap = cmap, norm = normalize)
        sm.set_array([])
        plt.colorbar(sm, orientation = 'horizontal', label = legendUnits)

        # Display
        plt.savefig(
            targetFolder + mapId.replace('/', '-') + ".png",
            dpi = dpi,
            #bbox_inches = 'tight',
            #pad_inches = 0,
            transparent = False
        )
        
        plt.close(fig)


def generateGIF(target, sourceFileNames, frameLength = 0.5):
    with imageio.get_writer(target, mode = 'I', duration = frameLength) as writer:
        for sourceFileName in sourceFileNames:
            image = imageio.imread(sourceFileName)
            writer.append_data(image)