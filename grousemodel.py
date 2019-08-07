import arcpy

###define main point file to append to
full = arcpy.GetParameterAsText(0)
#define feature to be appended to full
appF = arcpy.GetParameterAsText(1)

#arcpy.CopyFeatures_management(appF, "E:\\School\\GPS\\Backup\\2019\\GPSpoints_2019_py.gdb\\" + appF)
#########################################################################
###assign name############################################################
assignName = {'174768' : 'F11S9m', '174769' : 'C7S9m', '174770' : 'C11S9f',
              '174771' : 'C12S9f', '174772' : 'C16S9f', '174773' : 'C10S9f', '174774' : 'C1S8f',
              '174775' : 'C8S9f', '174776' : 'C17S9f', '174777' : 'C9S9f',
              '174778' : 'R1S8f', '174779' : 'C13S9f', '174780' : 'C6S9f',
              '174781' : 'C14S9f', '174782' : 'F10S9f', '177219' : 'F9S9f',
              '177220' : 'C5S9f', '177221' : 'C4S9f', '177222' : 'F8S9f', '177223' : 'F7S9f'}
print("dictionary set")

#add name field
arcpy.AddField_management(appF, "NAME", "TEXT")
###loop through assignName and write into existing column
cursor = arcpy.da.UpdateCursor(appF, ["ID", "NAME"])
print("cursor set")

arcpy.AddMessage("Converting Name Field...")

for updateRow in cursor:
    if updateRow[0] in assignName:
        print("starting loop")
        updateRow[1] = assignName[updateRow[0]]
        print(str(updateRow[1]) + "completed")
        cursor.updateRow(updateRow)
        print("row updated")
    else:
        print("this did not work")

del cursor

###assign unique ID############################################################
assignID = {'174768' : 757, '174769' : 754, '174770' : 760, '174771' : 761, '174772' : 765, '174773' : 759, '174774' : 730,
            '174775' : 755, '174776' : 766, '174777' : 758, '174778' : 740, '174779' : 762,
            '174780' : 753, '174781' : 763, '174782' : 756, '177219' : 750, '177220' : 752,
            '177221' : 751, '177222' : 749, '177223' : 748}

print("assign ID set")

#create ID field
arcpy.AddField_management(appF, "UniqueID", "TEXT")
###create ID update cursor
cursorID = arcpy.da.UpdateCursor(appF, ["ID", "UniqueID"])
print("ID cursor set")

arcpy.AddMessage("Converting UniqueID Field...")
###loop and assign ID
for updateRowID in cursorID:
    if updateRowID[0] in assignID:
        updateRowID[1] = assignID[updateRowID[0]]
        cursorID.updateRow(updateRowID)
    else:
        print("ID this did not work")

del cursorID

##############################################################################
###convert time#########################################################
arcpy.AddField_management(appF, "Year", "TEXT")
arcpy.AddField_management(appF, "Hour1", "SHORT")
arcpy.AddField_management(appF, "Month", "SHORT")
arcpy.AddField_management(appF, "Date", "SHORT")
###steal string snips from text field for ENTRY_DATE
arcpy.AddMessage("Converting date fields...")
arcpy.CalculateField_management(appF, "Year", '!Entry_DATE![6:11]')
arcpy.CalculateField_management(appF, "Month", '!Entry_DATE![0:2]')
arcpy.CalculateField_management(appF, "Date", '!Entry_DATE![3:5]')
arcpy.CalculateField_management(appF, "Hour1", '!Entry_DATE![11:14]')

###calculate mountain time
##############just add this field manually
arcpy.AddMessage("Converting hour to mountain...")
arcpy.AddField_management(appF, 'Time_3', 'DOUBLE')
cursorH = arcpy.da.UpdateCursor(appF,['Time_3', 'Hour1'])
print("hour cursor set")
for hour in cursorH:
    hour[0] = int(hour[1]) -6
    cursorH.updateRow(hour)

del cursorH
print("time done")

#############################################################################

###use datetime for day of the year
from datetime import datetime

arcpy.AddField_management(appF, 'DayOfYear', 'SHORT')

cursorD = arcpy.da.UpdateCursor(appF,["Year", "Month", "Date", "DayOfYear"])
print("day cursor set")

arcpy.AddMessage("Converting Day of the Year Field...")
for updateRowD in cursorD:
    updateRowD[3] = datetime(int(updateRowD[0]), updateRowD[1], updateRowD[2]).timetuple().tm_yday
    cursorD.updateRow(updateRowD)

del cursorD

###############################################################################

#assign lek of capture
arcpy.AddMessage("Assigning Lek...")
arcpy.AddField_management(appF, "Lek_temp", "TEXT")
arcpy.AddField_management(appF, "Lek_cap", "TEXT")

cursorL = arcpy.da.UpdateCursor(appF,['Lek_temp', 'NAME'])

for lek in cursorL:
    lek[0] = (lek[1])[0]
    cursorL.updateRow(lek)

del cursorL

leks = {'C' : 'COOP', 'F' : 'Fruitland', 'R' : 'Road Hollow', 'W' : 'Wildcat'}

cursorLek = arcpy.da.UpdateCursor(appF,['Lek_temp', 'Lek_cap'])

for lek_capture in cursorLek:
    if lek_capture[0] in leks:
        lek_capture[1] = leks[lek_capture[0]]
        cursorLek.updateRow(lek_capture)

del cursorLek

arcpy.DeleteField_management(appF, 'Lek_temp')

##############################################################################

#assign year of capture
arcpy.AddMessage("Assigning Capture Year...")
bird_2018 = ['728', '729', '730', '731', '732', '733', '734', '735', '736', '737',
             '738', '739', '740', '741', '742', '743', '744', '745', '746', '747']
bird_2019 = ['748', '749', '750', '751', '752', '753', '754', '755', '756', '757',
             '758', '759', '760', '761', '762', '763', '764', '765', '766']

arcpy.AddField_management(appF, "Year_cap", "TEXT")

cursorYear = arcpy.da.UpdateCursor(appF,['Year_cap', 'UniqueID'])

for cap_year in cursorYear:
    if cap_year[1] in bird_2018:
        cap_year[0] = '2018'
        cursorYear.updateRow(cap_year)
    elif cap_year[1] in bird_2019:
        cap_year[0] = '2019'
        cursorYear.updateRow(cap_year)
    else:
        cap_year[0] = '9999'
        cursorYear.updateRow(cap_year)

del cursorYear

###################################################################################

#assign sex
arcpy.AddMessage("Assigning Sex...")
bird_male = ['736', '738', '743', '744', '745', '746', '754', '757']
bird_female = ['728', '729', '730', '731', '732', '733', '734', '735',
             '737', '739', '740', '741', '742', '747', '748', '749', '750',
             '751', '752', '753', '755', '756', '758', '759', '760', '761',
             '762', '763', '764', '765', '766']

arcpy.AddField_management(appF, "SEX", "TEXT")

cursorSex = arcpy.da.UpdateCursor(appF,['SEX', 'UniqueID'])

for sex in cursorSex:
    if sex[1] in bird_male:
        sex[0] = 'MALE'
        cursorSex.updateRow(sex)
    elif sex[1] in bird_female:
        sex[0] = 'FEMALE'
        cursorSex.updateRow(sex)
    else:
        sex[0] = 'UNKNOWN'
        cursorSex.updateRow(sex)

del cursorSex

################################################################################

#append features
arcpy.AddMessage("Appending Features...")
point_append = arcpy.Append_management (appF, full, 'NO_TEST')
arcpy.AddMessage("Deleting Identical...")
delete_identical = arcpy.DeleteIdentical_management(full, ["ID", "ENTRY_DATE", "LAT", "LON"])
arcpy.AddMessage("Complete")
#################################################
#################################################
#EVERYTHING ABOVE THIS WORKS#####################
#################################################




#This works individually, just have to save edits between each step
#saving for just in case later
#arcpy.AddField_management(appF, "ed", "DATE")
#arcpy.CalculateField_management(appF, "ed", "!ENTRY_DATE!")
###convert year
#print("converting year")
#arcpy.ConvertTimeField_management(appF, 'ed', 'yyyy', 'Year', 'LONG', 'yyyy')
#print("year done")
###convert month
#print("converting month")
#arcpy.ConvertTimeField_management(appF, 'ed', 'MM', 'Month', 'LONG', 'MM')
#print("month done")
###convert date
#print("converting date")
#arcpy.ConvertTimeField_management(appF, 'ed', 'dd', 'Date', 'LONG', 'dd')
#print("date done")
###convert hour
#print("converting hour")
#arcpy.ConvertTimeField_management(appF, 'ed', 'HH', 'Hour1', 'LONG', 'HH')
#print("hour done")
###convert hour to mountain time
#print("GMT to mountain")
