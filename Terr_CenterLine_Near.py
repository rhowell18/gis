#Adds a near field for parent's nests for both road centerlines and nearest territory
#boundaries by given year. Exports to excel to copy manually
#run in python window with files loaded

nest = "G:\\proj\\Ryan\\MiscProject.gdb\\nests_merge_copy" #this file must have a text field called "YEAR_t" that has the year of the point
########################################################################################################
#Prelim work############################################################################################
ter = "abs_fsj_t1998_l"
y = ter[-6:-2]

##########################################
#get list of territories
list = []
p = arcpy.mp.ArcGISProject("CURRENT")
m = p.listMaps('Near Nest')[0]
x = m.listLayers()

for item in x:
    list.append(item.name)
##########################################
#results from previous block
list = ['abs_fsj_t2019_l', 'abs_fsj_t2018_l', 'abs_fsj_t2017_l', 'abs_fsj_t2016_l',
'abs_fsj_t2015_l', 'abs_fsj_t2014_l', 'abs_fsj_t2013_l', 'abs_fsj_t2012_l', 'abs_fsj_t2011_l',
'abs_fsj_t2010_l', 'abs_fsj_t2009_l', 'abs_fsj_t2008_l', 'abs_fsj_t2007_l', 'abs_fsj_t2006_l',
'abs_fsj_t2005_l', 'abs_fsj_t2004_l', 'abs_fsj_t2003_l', 'abs_fsj_t2002_l', 'abs_fsj_t2001_l',
'abs_fsj_t2000_l', 'abs_fsj_t1999_l', 'abs_fsj_t1998_l']
###########################################################################################################
#append all of the territories into one line file with a year field for query
#full feature to append to
full = "G:\\proj\\Ryan\\MiscProject.gdb\\territories_97_20"
for item in list:
    year = item[-6:-2]
    print(year)
    copy = arcpy.conversion.FeatureClassToFeatureClass("G:\\Library\\Shapefiles\\utm83\\AvianEcology\\DemographyTract\\Territories\\" + item + ".shp", r"G:\proj\Ryan\MiscProject.gdb", "copy_" + year)
    arcpy.AddField_management(copy, 'YEAR_N', 'STRING')
    with arcpy.da.UpdateCursor(copy, ['YEAR_N']) as cursor:
        for row in cursor:
            row[0] = year
            cursor.updateRow(row)
    arcpy.Append_management (copy, full, 'NO_TEST')
##############################################################################################################
#perform near analysis for territories on merged nest file
ylist = ['1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005',
'2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015',
'2016', '2017', '2018', '2019', '2020']
for item in ylist:
    selTer = arcpy.management.SelectLayerByAttribute(full, "NEW_SELECTION", "YEAR_N = '" + item + "'", None)
    selNest = arcpy.management.SelectLayerByAttribute(nest, "NEW_SELECTION", "YEAR_t = '" + item + "'", None)
    near = arcpy.Near_analysis(selNest, selTer)
    with arcpy.da.UpdateCursor(selNest, ['terr_Dist', 'NEAR_DIST']) as cursor:
        for row in cursor:
            #if row[0] == "":
            print(item)
            row[0] = row[1]
            cursor.updateRow(row)
###############################################################################################################
#Took the excel table with 3 tabs and exported each as a separate CSV. Add a Lat and Long column (doesn't matter the value)
#add to the map as a new point file. file path below assigned to variables

################################################################################################################
#copy near values to dictionary, then populate the table
GIS_nest = "G:\\proj\\Ryan\\MiscProject.gdb\\GIS_Nests_csv"
GIS_Mnest = "G:\\proj\\Ryan\\MiscProject.gdb\\GIS_MomsNests_csv"
GIS_Dnest = "G:\\proj\\Ryan\\MiscProject.gdb\\GIS_DadsNests_csv"

#create empty lists to iterate through
gis_list = []
mlist = []
dlist = []

#create empty dictionaries to populate road value
gis_dict_rd = {}
mdict_rd = {}
ddict_rd = {}

#create empty dictionaries to populate territory value
gis_dict_ter = {}
mdict_ter = {}
ddict_ter = {}

################################################################
#populate lists with all of the nest ID's we are interested in
with arcpy.da.SearchCursor(GIS_nest, ["Nest"]) as cursor:
    for row in cursor:
        gis_list.append(row[0])

with arcpy.da.SearchCursor(GIS_Mnest, ["MomsNest"]) as cursor:
    for row in cursor:
        mlist.append(row[0])

with arcpy.da.SearchCursor(GIS_Dnest, ["DadsNest"]) as cursor:
    for row in cursor:
        dlist.append(row[0])

################################################################
#populate dictionary with nearest road and territory value based on if ID is in the respective list
with arcpy.da.SearchCursor(nest, ["NESTID", "terr_Dist", "road_Dist"]) as cursor:
    for row in cursor:
        if row[0] in gis_list:
            gis_dict_rd[row[0]] = row[2]
            gis_dict_ter[row[0]] = row[1]
        else:
            print("not in gis list")

with arcpy.da.SearchCursor(nest, ["NESTID", "terr_Dist", "road_Dist"]) as cursor:
    for row in cursor:
        if row[0] in mlist:
            mdict_rd[row[0]] = row[2]
            mdict_ter[row[0]] = row[1]
        else:
            print("not in mom list")

with arcpy.da.SearchCursor(nest, ["NESTID", "terr_Dist", "road_Dist"]) as cursor:
    for row in cursor:
        if row[0] in dlist:
            ddict_rd[row[0]] = row[2]
            ddict_ter[row[0]] = row[1]
        else:
            print("not in dad list")
#####################################################################
#update rows in each intermediate point file. Once done can copy to excel file
with arcpy.da.UpdateCursor(GIS_nest, ['Nest', 'Dist_Road']) as cursor:
    for row in cursor:
        if row[0] in gis_dict_rd:
            row[1] = gis_dict_rd[row[0]]
            cursor.updateRow(row)
        else:
            print(row[0] + " not in GIS Rd")
print("1 complete")
with arcpy.da.UpdateCursor(GIS_nest, ['Nest', 'Dist_Terr']) as cursor:
    for row in cursor:
        if row[0] in gis_dict_ter:
            row[1] = gis_dict_ter[row[0]]
            cursor.updateRow(row)
        else:
            print(row[0] + " not in GIS ter")
print("2 complete")

with arcpy.da.UpdateCursor(GIS_Mnest, ['MomsNest', 'Dist_Road']) as cursor:
    for row in cursor:
        if row[0] in mdict_rd:
            row[1] = mdict_rd[row[0]]
            cursor.updateRow(row)
        else:
            print(row[0] + " not in mom Rd")
print("3 complete")
with arcpy.da.UpdateCursor(GIS_Mnest, ['MomsNest', 'Dist_Terr']) as cursor:
    for row in cursor:
        if row[0] in mdict_ter:
            row[1] = mdict_ter[row[0]]
            cursor.updateRow(row)
        else:
            print(row[0] + " not in mom ter")
print("4 complete")

with arcpy.da.UpdateCursor(GIS_Dnest, ['DadsNest', 'Dist_Road']) as cursor:
    for row in cursor:
        if row[0] in ddict_rd:
            row[1] = ddict_rd[row[0]]
            cursor.updateRow(row)
        else:
            print(" not in dad Rd")
print("5 complete")
with arcpy.da.UpdateCursor(GIS_Dnest, ['DadsNest', 'Dist_Terr']) as cursor:
    for row in cursor:
        if row[0] in ddict_ter:
            row[1] = ddict_ter[row[0]]
            cursor.updateRow(row)
        else:
            print(" not in dad ter")
print("6 complete")

##################################################################
#export table to excel
arcpy.conversion.TableToExcel(GIS_nest, "G:\\proj\\Ryan\\Lyn_NearAnalysis_RoadAndTerrBoundary\\GIS_nest", "NAME", "CODE")
arcpy.conversion.TableToExcel(GIS_Mnest, "G:\\proj\\Ryan\\Lyn_NearAnalysis_RoadAndTerrBoundary\\GIS_Mnest", "NAME", "CODE")
arcpy.conversion.TableToExcel(GIS_Dnest, "G:\\proj\\Ryan\\Lyn_NearAnalysis_RoadAndTerrBoundary\\GIS_Dnest", "NAME", "CODE")

#When these are done, copy and paste into excel file
