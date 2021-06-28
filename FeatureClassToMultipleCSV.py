####################################################################################################
#This tool takes one input point file and writes all rows into an existing CSV. The fields
#that are copied are derived from the existing CSV.
#Created for M. West in Restoration Ecology Lab, Archbold Biological Station. Use case was to
#populate 4 CSVs for use with an Access database.
#NOTE THAT THE DICTIONARIES ARE HARD CODED - MAKE EDITS FOR OTHER APPLICATIONS
#Author: R Howell, June 2021, howell.ryan12@gmail.com
##################################################################################################
import arcpy
import csv

#parameterized variables
inter = arcpy.GetParameterAsText(0)#geodatabase for intermediate data (geodatabase)
table_in = arcpy.GetParameterAsText(1)#GIS table (feature class)
csv_in = arcpy.GetParameterAsText(2)#CSV table to append (file)
type = arcpy.GetParameterAsText(3)#identify which of the CSVs you are working with, and which dictionary to use (string)
####################################################################################
#Dictionaries for column names - use even if names don't differ between CSV and GIS table
#KEY----> CSV field : GIS field
burrow_data_dict = {"ObsDate" : "SurveyDate", "BurrowNum" : "BurrowNum", "ActivityStatus" : "Status",
                    "Width_cm" : "Width", "Aspect" : "Aspect", "Occupied" : "Occupied",
                    "Occupancy_Method" : "OccMethod", "OccupancyMethod" : "Occupancy_",
                    "OtherVert" : "OtherVert"}

burrow_coords_dict = {"UTM_N" : "Northing", "BurrowNum" : "BurrowNum", "UTM_E" : "Easting",
                    "PDOP" : "Max_PDOP", "ObsDate" : "SurveyDate"}

burrow_import_dict = {"BurrowNum" : "BurrowNum", "ManUnit" : "ManUnit"}

stake_pulled_dict = {"BurrowNum" : "BurrowNum", "DateStakeRemoved" : "StakePull"}
#####################################################################################
#Set up as a function so that the dictionary used can vary based on type parameter
def wCSV(table, dict):
    #this might be irrelevant when running a script tool instead of testing in python window
    table_field_list = arcpy.ListFields(table)
    table_field_list_name = [] #This is the only product out of this code that we need#########################################################
    for item in table_field_list:
        table_field_list_name.append(item.name)
    ####################################################################################
    #make a copy of the GIS table - this is so that it is a feature class, not a shapefile,
    #and you can have a field name with more than 10 characters
    table_copy = arcpy.conversion.FeatureClassToFeatureClass(table, inter, "table_copy")
    ######################################################################################
    ################################################################################
    #create lists of CSV fields
    f= open(csv_in)
    csv_f = csv.reader(f)

    field_list = []
    for row in csv_f:
        field_list.append(row)
    f.close()

    new_field_list = field_list[0]
    ################################################################################
    #add a field to the point layer if it isn't there, temporarily, so the code will run
    delList = []
    for item in new_field_list:
        print(item)
        if item in table_field_list_name:
            print(item + " in list")
        elif item in dict and dict[item] in table_field_list_name:
            print(item + " in dict")
        else:
            arcpy.AddField_management(table_copy, item, "TEXT")
            delList.append(item)
    #################################################################################
    #create a new list, new_table_field_list_name, which converts the fields from CSV to
    #the correct names in the GIS table
    new_table_field_list_name = []
    for field in new_field_list:
        if field in dict:
            new_table_field_list_name.append(dict[field])
        else:
            new_table_field_list_name.append(field)
    #################################################################################
    #populates list_of_row_values, a list of lists. Each sublist has values for each field
    #for one row (in the field order of the CSV file)
    list_of_row_values = [] #this is a list of lists
    with arcpy.da.SearchCursor(table_copy, new_table_field_list_name) as cursor:
        for row in cursor:
            list = []
            for item in new_table_field_list_name:
                ind = new_table_field_list_name.index(item)
                list.append(str(row[ind]))
            list_of_row_values.append(list)
    ##################################################################################
    #opens the CSV file, iterates through the sub-lists within the list_of_row_values list
    #each item in the sublist is then written across the row in the CSV, then it goes on
    #to the next sublist
    for L in list_of_row_values:
        with open(csv_in, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(L)
    ###################################################################################
    #delete the intermediate feature class
    arcpy.Delete_management(table_copy)

#######################################################################################
#run the function based on the type parameter
if type == "BurrowCoords":
    wCSV(table_in, burrow_coords_dict)
elif type == "BurrowData":
    wCSV(table_in, burrow_data_dict)
elif type == "Burrows_Import":
    wCSV(table_in, burrow_import_dict)
elif type == "StakePull":
    sel = arcpy.management.SelectLayerByAttribute(table_in, "NEW_SELECTION", "StakePull IS NOT NULL", None)
    wCSV(sel, stake_pulled_dict)
    ######################################################
    #delete any field where the stake pull column is null
