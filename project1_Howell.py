#Setup
###############################################################################
import arcpy

arcpy.env.overwriteOutput = 'TRUE'

workspace = arcpy.GetParameterAsText(0)
points = arcpy.GetParameterAsText(1)
wt_fld = arcpy.GetParameterAsText(2)
seed = arcpy.GetParameterAsText(3)
facil = arcpy.GetParameter(4)
near_method = arcpy.GetParameterAsText(5)
output = arcpy.GetParameterAsText(6)
metaiterations = arcpy.GetParameterAsText(7)
interdelete = arcpy.GetParameterAsText(8)
iterations = arcpy.GetParameter(9)
metanumb = arcpy.GetParameter(10)
thpoly = arcpy.GetParameterAsText(11)
#Outpath = r"H:\Classes\Fall_2019\GEOG_412\Project1.gdb"
arcpy.env.extent = points
################################################################################

#Warnings and Errors
#############################################################################
if seed != "" and facil != "":
    arcpy.AddError("Input seed OR number of facilities required")
    sys.exit()

elif seed != "" and metaiterations == "true":
    arcpy.AddError("Metaiteration not allowed with user input seeds")
    sys.exit()

#determine if input is projected or not, give appropriate warning
proj = arcpy.Describe(points).spatialReference.projectionCode
#proj2 = proj.
if proj == 0 and near_method == "PLANAR":
    arcpy.AddWarning("Planar measurement selected for unprojected coordinate system. Measurements are in degrees.")

if metanumb < 3 or metanumb > 5:
    arcpy.AddWarning("Number of meta-iterations is outside of recommended range of 3 to 5")

if metanumb > 5:
    arcpy.AddError("More than 5 meta iterations not supported")
    sys.exit()

if metanumb == 1:
    arcpy.AddError("Less than 2 meta iterations not supported")
    sys.exit()

if iterations < 5 or iterations > 10:
    arcpy.AddWarning("Number of iterations is outside of recommended range of 5 to 10")
###############################################################################


######calculate optimal locations#############################################
#dictionary to determine mean difference and list to delete intermediate data
meandiff = {}
deletefeatures = []

#copy the points layer and seed layer to a scratch file
points_copy = arcpy.CopyFeatures_management(points, workspace + "\\" + "points_copy")
deletefeatures.append(points_copy)
if seed != "":
    seed_copy = arcpy.CopyFeatures_management(seed, workspace + "\\" + "seed_copy")
    deletefeatures.append(seed_copy)



def metaanalysis(checkbox):
    if checkbox == 'false': #no metaiterations
        def optimal(path, pointlayer, weight, facility, number):
            #if no seed file is added, generate random facility
            facillist = []
            facillist.append(facility)
            for A in facillist:
                if facillist[0] == "":
                    arcpy.AddMessage("Generating random seed location")
                    global seedx
                    seedx = arcpy.CreateRandomPoints_management(workspace, "Random", points_copy, "", number_of_points_or_field = int(number))
                    deletefeatures.append(seedx)
                else:
                    arcpy.AddMessage("Using input seed")
                    seedx = seed_copy
            global iterlist
            iterlist = []
            for iter in range(iterations):
            ###near and mean center#########################################################
                if iter == 0:
                    arcpy.AddMessage("Performing iteration #" + str(iter + 1))
                    near = arcpy.Near_analysis(pointlayer, seedx, "", "", "", near_method)
                    mean = arcpy.MeanCenter_stats(pointlayer, path + "\\" + "meancenter" + str(iter + 1), weight, 'NEAR_FID', '')
                    arcpy.AddField_management(mean, "Iteration", 'TEXT')
                    arcpy.CalculateField_management(mean, 'ITERATION', str(iter + 1))
                    iterlist.append(mean)
                    table0 = arcpy.Statistics_analysis(pointlayer, "mean_" + str(iter), [['NEAR_DIST', 'Mean']])
                    with arcpy.da.SearchCursor(table0, ["MEAN_NEAR_DIST"]) as cursor:
                        for row in cursor:
                            value0 = row[0]
                    meandiff.update({iter + 1 : value0})
                    arcpy.Delete_management(table0)
                    deletefeatures.append(mean)
                    #arcpy.AddMessage("Average Difference for iteration " + str(iter + 1) + " is " + str(value0))
                elif iter >= 1:
                    arcpy.AddMessage("Performing iteration #" + str(iter + 1))
                    nearx = arcpy.Near_analysis(pointlayer, iterlist[-1], "", "", "", near_method)
                    meanx = arcpy.MeanCenter_stats(pointlayer, path + "\\" + "meancenter" + str(iter + 1), weight, 'NEAR_FID', '')
                    arcpy.AddField_management(meanx, "Iteration", 'TEXT')
                    arcpy.CalculateField_management(meanx, 'ITERATION', str(iter + 1))
                    iterlist.append(meanx)
                    table1 = arcpy.Statistics_analysis(pointlayer, "mean_" + str(iter), [['NEAR_DIST', 'Mean']])
                    with arcpy.da.SearchCursor(table1, ["MEAN_NEAR_DIST"]) as cursor:
                        for row in cursor:
                            value1 = row[0]
                    meandiff.update({iter + 1 : value1})
                    arcpy.Delete_management(table1)
                    deletefeatures.append(meanx)
                else:
                    arcpy.AddMessage("Error in first iteration")
            return iterlist
        OptimalLocations = optimal(workspace, points_copy, wt_fld, seed, facil)
    #merge results
        merge = arcpy.Merge_management(iterlist, str(workspace) + "\\" + "interm_loc")
        out = arcpy.CopyFeatures_management(iterlist[-1], output)
        #arcpy.AddMessage("Merge complete")
        arcpy.AddMessage("The mean distance is " + str(meandiff[iterations - 1]))
        if thpoly != "":
            arcpy.AddMessage("Generating Thiessen Polygons")
            tp = arcpy.CreateThiessenPolygons_analysis(out, thpoly)
#perform meta iteration if checked###############################################
    elif checkbox == 'true':
        global meandiffmeta1
        meandiffmeta1 = {}
        global meandiffmeta2
        meandiffmeta2 = {}
        global meandiffmeta3
        meandiffmeta3 = {}
        global meandiffmeta4
        meandiffmeta4 = {}
        global meandiffmeta5
        meandiffmeta5 = {}
        dictlist = [meandiffmeta1, meandiffmeta2, meandiffmeta3, meandiffmeta4, meandiffmeta5]
        global metamasterlist
        metamasterlist = []
        for metaan in range(metanumb):#deleted + 1
            arcpy.AddMessage("Performing Meta-Iteration " + str(metaan + 1))
            def optimalmeta(pathmeta, pointlayermeta, weightmeta, facilitymeta, numbermeta):
                    #if no seed file is added, generate random facilities
                facillistmeta = []
                facillistmeta.append(facilitymeta)
                for A in facillistmeta:
                    if facillistmeta[0] == "":
                        arcpy.AddMessage("Generating random seed location for Meta-iteration " + str(metaan + 1))
                        global seedxmeta
                        seedxmeta = arcpy.CreateRandomPoints_management(workspace, "Random_meta_" + str(metaan + 1), points_copy, "", int(numbermeta))
                        deletefeatures.append(seedxmeta)
                    else:
                        arcpy.AddMessage("Using input seed")
                        seedxmeta = seed_copy
                global iterlistmeta
                iterlistmeta = []
                for iter in range(iterations):
                    ###near and mean center#########################################################
                    if iter == 0:
                        arcpy.AddMessage("Performing iteration #" + str(iter + 1) + " for Meta-Iteration " + str(metaan + 1))
                        nearmeta = arcpy.Near_analysis(pointlayermeta, seedxmeta, "", "", "", near_method)
                        meanmeta = arcpy.MeanCenter_stats(pointlayermeta, pathmeta + "\\" + "meancenter_meta" + str(metaan + 1) + "_iteration_" + str(iter + 1), weightmeta, 'NEAR_FID', '')
                        arcpy.AddField_management(meanmeta, "Iteration", 'TEXT')
                        arcpy.AddField_management(meanmeta, "MetaIT", 'TEXT')
                        arcpy.CalculateField_management(meanmeta, 'ITERATION', str(iter + 1))
                        arcpy.CalculateField_management(meanmeta, 'METAIT', str(metaan + 1))
                        iterlistmeta.append(meanmeta)
                        metamasterlist.append(meanmeta)
                        table0meta = arcpy.Statistics_analysis(pointlayermeta, "mean_meta_" + str(iter), [['NEAR_DIST', 'Mean']])
                        with arcpy.da.SearchCursor(table0meta, ["MEAN_NEAR_DIST"]) as cursor:
                            for row in cursor:
                                value0meta = row[0]
                        metalist = dictlist[0]
                        metalist.update({iter + 1 : value0meta})
                        arcpy.Delete_management(table0meta)
                        deletefeatures.append(meanmeta)

                    elif iter >= 1:
                        arcpy.AddMessage("Performing iteration #" + str(iter + 1) + " for Meta-Iteration " + str(metaan + 1))
                        nearxmeta = arcpy.Near_analysis(pointlayermeta, iterlistmeta[-1], "", "", "", near_method)
                        meanxmeta = arcpy.MeanCenter_stats(pointlayermeta, pathmeta + "\\" + "meancenter_meta" + str(metaan + 1) + "_iteration_" + str(iter + 1), weightmeta, 'NEAR_FID', '')
                        arcpy.AddField_management(meanxmeta, "Iteration", 'TEXT')
                        arcpy.AddField_management(meanxmeta, "MetaIT", 'TEXT')
                        arcpy.CalculateField_management(meanxmeta, 'ITERATION', str(iter + 1))
                        arcpy.CalculateField_management(meanxmeta, 'METAIT', str(metaan + 1))
                        iterlistmeta.append(meanxmeta)
                        metamasterlist.append(meanxmeta)
                        table1meta = arcpy.Statistics_analysis(pointlayermeta, "mean_" + str(iter) + "_" + str(metaan + 1), [['NEAR_DIST', 'Mean']])
                        with arcpy.da.SearchCursor(table1meta, ["MEAN_NEAR_DIST"]) as cursor:
                            for row in cursor:
                                value1meta = row[0]
                        metalist = dictlist[metaan]
                        metalist.update({iter + 1 : value1meta})
                        arcpy.Delete_management(table1meta)
                        deletefeatures.append(meanxmeta)

                    else:
                        arcpy.AddMessage("Error in first iteration")


            OptimalLocations = optimalmeta(workspace, points_copy, wt_fld, seed, facil)
            merge = arcpy.Merge_management(metamasterlist, str(workspace) + "\\" + "interm_loc")

            ###compute optimal locations out of meta analysis
        arcpy.AddMessage("Determining lowest distance location meta analysis")

        mindict = {}

        for test in range(metanumb):
            mindict.update({test + 1: dictlist[test][iterations]})

        bestdict = min(mindict.keys(), key = (lambda k: mindict[k]))

        arcpy.AddMessage("The lowest average distance was achieved using meta-iteration "
          + str(bestdict) + " and the mean distance is " + str(int(mindict[bestdict])))
        if bestdict == 1:
            op = arcpy.CopyFeatures_management(metamasterlist[4], output)
        elif bestdict == 2:
            op = arcpy.CopyFeatures_management(metamasterlist[9], output)
        elif bestdict == 3:
            op = arcpy.CopyFeatures_management(metamasterlist[14], output)
        elif bestdict == 4:
            op = arcpy.CopyFeatures_management(metamasterlist[19], output)
        elif bestdict == 5:
            op = arcpy.CopyFeatures_management(metamasterlist[-1], output)
        else:
            arcpy.AddMessage("Something went wrong with the meta-iteration summary")

        if thpoly != "":
            arcpy.AddMessage("Generating Thiessen Polygons")
            tp = arcpy.CreateThiessenPolygons_analysis(op, thpoly)

    else:
        arcpy.AddMessage("Meta-analysis not checked")
    #delete intermediate data
    global interdel
    def interdel(delinter):
        if delinter == 'true' and metaiterations == 'true':
            arcpy.AddMessage("Deleting Intermediate Data")
            arcpy.Delete_management(merge)
            for delete in deletefeatures:
                arcpy.Delete_management(delete)
            for fcmeta in metamasterlist:
                arcpy.Delete_management(fcmeta)
            for fciter in iterlistmeta:
                arcpy.Delete_management(fcmeta)
        elif delinter == 'true' and metaiterations == 'false':
            arcpy.AddMessage("Deleting Intermediate Data")
            arcpy.Delete_management(seedx)
            arcpy.Delete_management(merge)
            for fciterlist in iterlist:
                arcpy.Delete_management(fciterlist)
        elif delinter == 'false':
            arcpy.AddMessage("Keeping intermediate data")
    interdel(interdelete)

metaanalysis(metaiterations)
