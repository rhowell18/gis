###this script generates a line file from the grouse database and then
###marks points that are over 2km for further inspection on if they are
###accurate or not

import arcpy

point =
output =
date = #format Jan01_19

#create line
line = arcpy.PointsToLine_management(point, output + "\\" + date, "NAME")
print("line created")

#split into polyline by vertex
line_split = arcpy.SplitLine_management(line, output + "\\" + date + "_s")
print("line split")

#add length field, calculate
length = arcpy.AddField_management(line_split, "length_m", "DOUBLE")
print("length field added")
arcpy.CalculateGeometryAttributes_management(line_split, [["length_m", "LENGTH_GEODESIC"]], "METERS")
print("geometry calculated")

###mark as possible problem
prob = arcpy.AddField_management(line_split, "mark", "TEXT")
print("mark field added")
cursor = arcpy.da.UpdateCursor(line_split, ["length_m", "mark"])
print("cursor created")

for updateRow in cursor:
    if updateRow[0] > 2000:
        updateRow[1] = 1
    elif updateRow[0] <= 2000:
        updateRow[1] = 0
    cursor.updateRow(updateRow)

del cursor
print("complete")


#This is to automatically mark the points but it's not working, try again later
#line_split_2 = arcpy.SelectLayerByAttribute_management(line_split, "NEW_SELECTION",
#" 'mark' = '1' ")
###select points by location
#point_select = arcpy.SelectLayerByLocation_management(point, "INTERSECT", line_split_2)

#cursorp = arcpy.da.UpdateCursor(point_select, ["line_mark"])
#for update in cursorp:
#    update[0] = 1
#    cursorp.updateRow(update)

#del cursorp
