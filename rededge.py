import arcpy
from arcpy import env
from arcpy.sa import *

outWorkspace = arcpy.GetParameterAsText(0)
cell = arcpy.GetParameterAsText(1)
blue = arcpy.GetParameterAsText(2)
green = arcpy.GetParameterAsText(3)
red = arcpy.GetParameterAsText(4)
nir = arcpy.GetParameterAsText(5)
rededge = arcpy.GetParameterAsText(6)
outName = arcpy.GetParameterAsText(7)

###create empty raster datasets
arcpy.AddMessage("making raster datasets")
blue_T = arcpy.CreateRasterDataset_management(outWorkspace, "blue.tif", cell, '32_BIT_FLOAT', "", 1, "", "", "", "", "")
green_T = arcpy.CreateRasterDataset_management(outWorkspace, "green.tif", cell, '32_BIT_FLOAT', "", 1, "", "", "", "", "")
red_T = arcpy.CreateRasterDataset_management(outWorkspace, "red.tif", cell, '32_BIT_FLOAT', "", 1, "", "", "", "", "")
nir_T = arcpy.CreateRasterDataset_management(outWorkspace, "nir.tif", cell, '32_BIT_FLOAT', "", 1, "", "", "", "", "")
rededge_T = arcpy.CreateRasterDataset_management(outWorkspace, "rededge.tif", cell, '32_BIT_FLOAT', "", 1, "", "", "", "", "")

#####################################################################################
#Merge layers####################################################################
###combine blue layers#####################################################
arcpy.AddMessage("Merging blue...")
bluex = arcpy.Mosaic_management(blue, blue_T)
#################################################################################
#Combine green layers#############################################################
arcpy.AddMessage("Merging green...")
greenx = arcpy.Mosaic_management(green, green_T)
#Combine red layers#############################################################
arcpy.AddMessage("Merging red...")
redx = arcpy.Mosaic_management(red, red_T)
#Combine red layers#############################################################
arcpy.AddMessage("Merging NIR...")
nirx = arcpy.Mosaic_management(nir, nir_T)
#Combine red layers#############################################################
arcpy.AddMessage("Merging red edge...")
rededgex = arcpy.Mosaic_management(rededge, rededge_T)
##############################################################################

#composite bands
arcpy.AddMessage("Running Composite Bands...")
list = [bluex, greenx, redx, nirx, rededgex]
arcpy.CompositeBands_management(list, outWorkspace + "\\" + outName)
