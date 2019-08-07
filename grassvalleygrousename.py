import arcpy

###define main point file to append to
full =
#define feature to be appended to full
appF =

#########################################################################
###assign name############################################################
assignName = {'159073' : 'A2S8f', '159081' : 'N3S6f', '159086' : 'N5S6f', '159105' : 'N9F6f',
              '166637' : 'C10F7f'}
print("dictionary set")

#add name field
arcpy.AddField_management(appF, "NAME", "TEXT")
###loop through assignName and write into existing column
cursor = arcpy.da.UpdateCursor(appF, ["ID", "NAME"])
print("cursor set")

for updateRow in cursor:
    if updateRow[0] in assignName:
        print("starting loop")
        updateRow[1] = assignName[updateRow[0]]
        print(str(updateRow[1]) + " completed")
        cursor.updateRow(updateRow)
        print("row updated")
    else:
        print("this did not work")

del cursor

###append and delete identical
point_append = arcpy.Append_management (appF, full, 'NO_TEST')
delete_identical = arcpy.DeleteIdentical_management(full, ["ID", "ENTRY_DATE", "LAT", "LON"])
