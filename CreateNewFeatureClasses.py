#list all of the feature classes in the contents pane, create new FC for each
#drone flight to digitized polygon FC

#database to add the new FC to
arcpy.env.workspace = r'C:\\Users\\rhowell\\Documents\\ArcGIS\\Projects\\Archbold_2020_PostBurnFlights\\Archbold_2020_PostBurnFlights.gdb'
output = r'C:\\Users\\rhowell\\Documents\\ArcGIS\\Projects\\Archbold_2020_PostBurnFlights\\Archbold_2020_PostBurnFlights.gdb'
list = []
###########################################################################
############################################################################
#list all of the layers on the current project
p = arcpy.mp.ArcGISProject("CURRENT")
m = p.listMaps('Map')[0]
x = m.listLayers()

for item in x:
    list.append(item.name)

#make sure that every item does not start with a number or contain illegal characters
list2 = ['Orthos\\SW_Flatwoods_W_E_S_orthomosaic.tif', 'Orthos\\Railroad_Wildfire_orthomosaic.tif', 'Orthos\\NE_Scrub_orthomosaic.tif',
         'Orthos\\MC_WRP_C_1C_N_1W_orthomosaic.tif', 'Orthos\\Loop_Garden_orthomosaic.tif', 'Orthos\\ABS_5C_NurseryS_orthomosaic.tif', 'Orthos\\ABS_3E_orthomosaic.tif',
         'Orthos\\x60A_60C_orthomosaic.tif', 'Orthos\\x58A_58E_orthomosaic.tif', 'Orthos\\x54B_orthomosaic.tif', 'Orthos\\x4E_S_58B_58C_orthomosaic.tif', 'Orthos\\x4E_N_orthomosaic.tif']

#create domain
domain = 'Intensity_new'
arcpy.management.CreateDomain(output, domain, 'burn severity domain', 'TEXT', 'CODED')
domDict = {'0':'unburned', '1':'low severity', '2': 'medium severity', '3': 'high severity'}
for code in domDict:
    print(code)
    arcpy.AddCodedValueToDomain_management(output, domain, str(code), domDict[code])

#create feature class, create new severity field, and assign domain to field

for item in list2:
    name = item.split("\\")[1]
    name2 = name.split("_orthomosaic")[0]
    fc = arcpy.CreateFeatureclass_management(output, str(name2) + "_intensity", "POLYGON", spatial_reference=list2[0])
    field = arcpy.AddField_management(fc, "intensity", "TEXT")
    arcpy.AssignDomainToField_management(fc, 'intensity', domain, None)
    print(name2)

###set symbology of one new polygon layer (symbolized by intensity field) manually
#then run the following
#####note:duplicates will crash the tool
manual = 'DigitizedBurns\\x4E_N_intensity'#this is the layer that you created the symbology manually
list3 = ['DigitizedBurns\\SW_Flatwoods_W_E_S_intensity', 'DigitizedBurns\\Railroad_Wildfire_intensity', 'DigitizedBurns\\NE_Scrub_intensity',
         'DigitizedBurns\\MC_WRP_C_1C_N_1W_intensity', 'DigitizedBurns\\Loop_Garden_intensity', 'DigitizedBurns\\ABS_5C_NurseryS_intensity', 'DigitizedBurns\\ABS_3E_intensity',
         'DigitizedBurns\\x60A_60C_intensity', 'DigitizedBurns\\x58A_58E_intensity', 'DigitizedBurns\\x54B_intensity', 'DigitizedBurns\\x4E_S_58B_58C_intensity', 'DigitizedBurns\\x4E_N_intensity']
for item in list3:
    arcpy.management.ApplySymbologyFromLayer(item, manual, "VALUE_FIELD intensity intensity", "MAINTAIN")
