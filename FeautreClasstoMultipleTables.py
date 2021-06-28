###############################################################################
#This tool takes a master shapefile and exports a collection of tables for import
#into an access database. It was created for M. West in the Restoration Ecology lab
#for use on gopher tortoise burrows collected year over year.
#Created by R. Howell, June 2021 using ArcGIS Pro 2.7

import arcpy
import os
###############################################################################
###assign variables
master = arcpy.GetParameterAsText(0)#master shapefile that is going to be split (feature class)
inter = arcpy.GetParameterAsText(1)#workspace for intermediate data (workspace)
outTable = arcpy.GetParameterAsText(2)#location of output excel tables(folder)
fields_1 = arcpy.GetParameterAsText(3)#first list of fields that you want to keep (multi value list)
name_f1 = arcpy.GetParameterAsText(4)#output name of first output (string)
fields_2 = arcpy.GetParameterAsText(5)#second list of fields that you want to keep (multi value list)
name_f2 = arcpy.GetParameterAsText(6)#output name of second output (string)
fields_3 = arcpy.GetParameterAsText(7)#third list of fields that you want to keep (multi value list)
name_f3 = arcpy.GetParameterAsText(8)#output name of third output (string)
fields_4 = arcpy.GetParameterAsText(9)#fourth list of fields that you want to keep (multi value list)
name_f4 = arcpy.GetParameterAsText(10)#output name of fourth output (string)
delinter = arcpy.GetParameterAsText(11)#checked if you want to delete intermediate date. Checked by default (Boolean)

#create intermediate data folder
arcpy.AddMessage(inter + "\\intermediate")
arcpy.AddMessage(os.path.isdir(inter + "\\intermediate"))

if os.path.isdir(inter + "\\intermediate") == False:
    os.mkdir(inter + "\\intermediate")
################################################################################
################################################################################
####first table export
#Create a copy, list fields to check
li1 = fields_1.split(";")
arcpy.AddMessage("Creating table 1...")
c1 = arcpy.conversion.FeatureClassToFeatureClass(master, inter + "\\intermediate", "master_copy_1")
c1f = arcpy.ListFields(c1)
print(c1f)
#arcpy.AddMessage('length of first list: ' + str(len(c1f)))

#iterate through the list of fields. If it is NOT included in fields to keep parameter, add to a delete list
del_list_1 = []
print('length of list raw: ' + str(len(del_list_1)))
#arcpy.AddMessage('length of list raw: ' + str(len(del_list_1)))

for item in c1f:
    #arcpy.AddMessage("type = " + str(item.type))
    if item.type == 'OID' or item.type == 'Geometry':
        print(item.type)
    else:
        if item.name in li1:
            print("keep")
            #arcpy.AddMessage("1: " + str(item.name))
        else:
            del_list_1.append(item)
            #arcpy.AddMessage("2: " + str(item.name))

print(del_list_1)
print('length of list after: ' + str(len(del_list_1)))
#arcpy.AddMessage('length of list after: ' + str(len(del_list_1)))

#run delete fields based on the delete list above, then print fields to verify
arcpy.AddMessage("Cleaning table 1...")
for item in del_list_1:
    #arcpy.AddMessage(item.name)
    item1 = item.name
    del_1 = arcpy.management.DeleteField(c1, item1)

#export excel file
arcpy.AddMessage("Exporting table 1...")
#arcpy.AddMessage(outTable + "\\" + name_f1)
#arcpy.AddMessage(c1)
arcpy.conversion.TableToExcel(c1, outTable + "\\" + name_f1, "NAME", "CODE")

################################################################################
################################################################################
####second table export
if name_f2 != "":
    #Create a copy, list fields to check
    li2 = fields_2.split(";")
    arcpy.AddMessage("Creating table 2...")
    c2 = arcpy.conversion.FeatureClassToFeatureClass(master, inter + "\\intermediate", "master_copy_2")
    c2f = arcpy.ListFields(c2)
    print(c2f)
    #arcpy.AddMessage('length of first list: ' + str(len(c2f)))

    #iterate through the list of fields. If it is NOT included in fields to keep parameter, add to a delete list
    del_list_2 = []
    print('length of list raw: ' + str(len(del_list_2)))
    #arcpy.AddMessage('length of list raw: ' + str(len(del_list_2)))

    for item in c2f:
        #arcpy.AddMessage("type = " + str(item.type))
        if item.type == 'OID' or item.type == 'Geometry':
            print(item.type)
        else:
            if item.name in li2:
                print("keep")
                #arcpy.AddMessage("1: " + str(item.name))
            else:
                del_list_2.append(item)
                #arcpy.AddMessage("2: " + str(item.name))

    print(del_list_2)
    print('length of list after: ' + str(len(del_list_2)))
    #arcpy.AddMessage('length of list after: ' + str(len(del_list_2)))

    #run delete fields based on the delete list above, then print fields to verify
    arcpy.AddMessage("Cleaning table 2...")
    for item in del_list_2:
        #arcpy.AddMessage(item.name)
        item2 = item.name
        del_2 = arcpy.management.DeleteField(c2, item2)

    #export excel file
    arcpy.AddMessage("Exporting table 2...")
    #arcpy.AddMessage(outTable + "\\" + name_f2)
    #arcpy.AddMessage(c2)
    arcpy.conversion.TableToExcel(c2, outTable + "\\" + name_f2, "NAME", "CODE")

################################################################################
################################################################################
####third table export
if name_f3 != "":
    #Create a copy, list fields to check
    li3 = fields_3.split(";")
    arcpy.AddMessage("Creating table 3...")
    c3 = arcpy.conversion.FeatureClassToFeatureClass(master, inter + "\\intermediate", "master_copy_3")
    c3f = arcpy.ListFields(c3)
    print(c3f)
    #arcpy.AddMessage('length of first list: ' + str(len(c3f)))

    #iterate through the list of fields. If it is NOT included in fields to keep parameter, add to a delete list
    del_list_3 = []
    print('length of list raw: ' + str(len(del_list_3)))
    #arcpy.AddMessage('length of list raw: ' + str(len(del_list_2)))

    for item in c3f:
        #arcpy.AddMessage("type = " + str(item.type))
        if item.type == 'OID' or item.type == 'Geometry':
            print(item.type)
        else:
            if item.name in li3:
                print("keep")
                #arcpy.AddMessage("1: " + str(item.name))
            else:
                del_list_3.append(item)
                #arcpy.AddMessage("2: " + str(item.name))

    print(del_list_3)
    print('length of list after: ' + str(len(del_list_3)))
    #arcpy.AddMessage('length of list after: ' + str(len(del_list_3)))

    #run delete fields based on the delete list above, then print fields to verify
    arcpy.AddMessage("Cleaning table 3...")
    for item in del_list_3:
        #arcpy.AddMessage(item.name)
        item3 = item.name
        del_3 = arcpy.management.DeleteField(c3, item3)

    #export excel file
    arcpy.AddMessage("Exporting table 3...")
    #arcpy.AddMessage(outTable + "\\" + name_f3)
    #arcpy.AddMessage(c3)
    arcpy.conversion.TableToExcel(c3, outTable + "\\" + name_f3, "NAME", "CODE")

################################################################################
################################################################################
####fourth table export
if name_f4 != "":
    #Create a copy, list fields to check
    li4 = fields_4.split(";")
    arcpy.AddMessage("Creating table 4...")
    c4 = arcpy.conversion.FeatureClassToFeatureClass(master, inter + "\\intermediate", "master_copy_4")
    c4f = arcpy.ListFields(c4)
    print(c4f)
    #arcpy.AddMessage('length of first list: ' + str(len(c4f)))

    #iterate through the list of fields. If it is NOT included in fields to keep parameter, add to a delete list
    del_list_4 = []
    print('length of list raw: ' + str(len(del_list_4)))
    #arcpy.AddMessage('length of list raw: ' + str(len(del_list_4)))

    for item in c4f:
        #arcpy.AddMessage("type = " + str(item.type))
        if item.type == 'OID' or item.type == 'Geometry':
            print(item.type)
        else:
            if item.name in li4:
                print("keep")
                #arcpy.AddMessage("1: " + str(item.name))
            else:
                del_list_4.append(item)
                #arcpy.AddMessage("2: " + str(item.name))

    print(del_list_4)
    print('length of list after: ' + str(len(del_list_4)))
    #arcpy.AddMessage('length of list after: ' + str(len(del_list_4)))

    #run delete fields based on the delete list above, then print fields to verify
    arcpy.AddMessage("Cleaning table 4...")
    for item in del_list_4:
        #arcpy.AddMessage(item.name)
        item4 = item.name
        del_4 = arcpy.management.DeleteField(c4, item4)

    #export excel file
    arcpy.AddMessage("Exporting table 4...")
    #arcpy.AddMessage(outTable + "\\" + name_f4)
    #arcpy.AddMessage(c4)
    arcpy.conversion.TableToExcel(c4, outTable + "\\" + name_f4, "NAME", "CODE")

##################################################################################
#################################################################################
#delete intermediate data, if box if checked
if delinter == 'true':
    arcpy.AddMessage("Deleting intermediate data...")
    arcpy.Delete_management(c1)
    if name_f2 != "":
        arcpy.Delete_management(c2)
    if name_f3 != "":
        arcpy.Delete_management(c3)
    if name_f4 != "":
        arcpy.Delete_management(c4)
    os.rmdir(inter + "\\intermediate")

##################################################################################
