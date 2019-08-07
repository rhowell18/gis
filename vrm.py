import arcpy
from arcpy import env
from arcpy.sa import *

outWorkspace = arcpy.GetParameterAsText(0)
baseRaster = arcpy.GetParameterAsText(1)#Raster(r'E:\School\GIS\Python\pythontest.gdb\elevation')
scale = arcpy.GetParameterAsText(2)
outRaster = arcpy.GetParameterAsText(3)

###calculate slope and aspect, convert to radians
arcpy.AddMessage("Calculating slope and aspect, convert to radians...")
slope = Slope(baseRaster, "DEGREE") * 0.0175
aspect = Aspect(baseRaster)
aspectcorr = Con(aspect == -1, 0, aspect)
aspectrad = aspectcorr * 0.0175

###apply sin and cosine to slope
arcpy.AddMessage("Apply sin and cosine to slope...")
sinSlp = Sin(slope)#xy raster
cosSlp = Cos(slope)#z raster

###apply sin and cosine to aspect, convert negative to zero
arcpy.AddMessage("Apply sin and cosine to aspect...")
sinAsp = Sin(aspectrad)
cosAsp = Cos(aspectrad)

###x, y, and z values
###xy = sinSlp
#z = cosSlp
arcpy.AddMessage("Calculate x, y, and z values...")
rasterX = sinSlp * sinAsp
rasterY = sinSlp * cosAsp

###focal sum function for desired scale
arcpy.AddMessage("Calculate Focal Stats...")
xSum = FocalStatistics(rasterX, NbrRectangle(int(scale), int(scale), "CELL"), 'SUM', 'NODATA')
ySum = FocalStatistics(rasterY, NbrRectangle(int(scale), int(scale), "CELL"), 'SUM', 'NODATA')
zSum = FocalStatistics(cosSlp, NbrRectangle(int(scale), int(scale), "CELL"), 'SUM', 'NODATA')

###apply VRM
arcpy.AddMessage("Calculate VRM...")
vrm = 1 - (SquareRoot(Square(xSum) + Square(ySum) + Square(zSum)) / Square(int(scale)))
vrmcorr = Con(vrm < 0, 0, vrm)

###save Raster
arcpy.AddMessage("Saving VRM...")
vrmcorr.save(outRaster)
arcpy.AddMessage("Save Complete")

###delete intermediate Data
arcpy.AddMessage("Deleting intermediate data...")
arcpy.Delete_management(slope)
arcpy.Delete_management(aspect)
arcpy.Delete_management(aspectcorr)
arcpy.Delete_management(aspectrad)
arcpy.Delete_management(sinSlp)
arcpy.Delete_management(cosSlp)
arcpy.Delete_management(sinAsp)
arcpy.Delete_management(cosAsp)
arcpy.Delete_management(rasterX)
arcpy.Delete_management(rasterY)
arcpy.Delete_management(xSum)
arcpy.Delete_management(ySum)
arcpy.Delete_management(zSum)
arcpy.AddMessage("Complete")
