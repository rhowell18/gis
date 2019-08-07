# Created 2/20/19 from instructions from
# http://gis4geomorphology.com/roughness-topographic-position/
# step 1


import arcpy
from arcpy import env
from arcpy.sa import *

### set workspace
workspace = arcpy.GetParameterAsText(0)#r"E:\School\GIS\Python\pythontest.gdb"


###script arguments
elevation = arcpy.GetParameterAsText(1)
size = arcpy.GetParameterAsText(2)
outRaster = arcpy.GetParameterAsText(3)

###set up rasters
arcpy.AddMessage("Calculating min, max, mean...")
minElev = FocalStatistics(elevation, NbrRectangle(int(size), int(size), 'CELL'), 'MINIMUM')
maxElev = FocalStatistics(elevation, NbrRectangle(int(size), int(size), 'CELL'), 'MAXIMUM')
meanElev = FocalStatistics(elevation, NbrRectangle(int(size), int(size), 'CELL'), 'MEAN')

###raster calculator
arcpy.AddMessage("Calculating TPI...")
tpi = (meanElev - minElev) / (maxElev - minElev)

###save raster
arcpy.AddMessage("Saving Raster...")
tpi.save(outRaster)
arcpy.AddMessage("Save Complete...")

###delete intermediate data
arcpy.AddMessage("Deleting intermediate data...")
arcpy.Delete_management(minElev)
arcpy.Delete_management(maxElev)
arcpy.Delete_management(meanElev)
