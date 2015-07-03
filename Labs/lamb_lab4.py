# -*- coding: utf-8 -*-
"""
@author: Owen Lamb
Assignment 4
Watershed Characterization: 2d and 3d shape measures.
Created on Wed Feb 20 17:17:23 2013
"""
#==============================================================================
# Import Modules and Set Workspace.
#==============================================================================
print "Importing Modules"
import arcpy, math
from arcpy import env
from arcpy.sa import*
arcpy.CheckOutExtension("Spatial")
env.workspace = r"D:\lamb_lab4\data"
env.overwriteOutput = 1
import lamb_lab4_module

#==============================================================================
# Declare Variables
#==============================================================================
print "Declaring Variables"
thadem = "demlab4"
shed = "watersheds_3D.shp"
dem = Raster('demlab4')
zonalOput = 'surface_area.dbf'

#==============================================================================
# Part I
#==============================================================================
#==============================================================================
# Calling Functions
#==============================================================================
print "Calling Functions"
twoDparim = lamb_lab4_module.twodParim(shed)
twoDarea = lamb_lab4_module.twodArea(shed)
circRatio = lamb_lab4_module.circRatio(shed)
threeDparim = lamb_lab4_module.threedParim(shed)
threeDarea = lamb_lab4_module.threedArea(shed, dem, zonalOput)
threeDcirc = lamb_lab4_module.threeDcirc(shed,dem)

#==============================================================================
# Comparing Circularity Ratios
#==============================================================================
print "Adding Fields to watersheds shape file"
arcpy.AddField_management(shed,'circ2D',"FLOAT")
arcpy.AddField_management(shed,'circ3D',"FLOAT")
upCur = arcpy.UpdateCursor(shed)
numpoly = int(arcpy.GetCount_management(shed).getOutput(0))
print "Comparing 2D and 3D Circularity Ratios"
for i in range(numpoly):
    rows = upCur.next()
    rows.circ2D = circRatio[i]
    rows.circ3D = threeDcirc[i]
    upCur.updateRow(rows)
    print "The 2D Circularity Ratio for polygon",i+1,"is",circRatio[i]
    print "The 3D Circularity Ratio for polygon",i+1,"is",threeDcirc[i]
    print " "
del upCur, rows
print "Fields Circ_Ra_2d and Circ_Ra_3d updated and compared"



#==============================================================================
# part II
#==============================================================================
# Call relief ratio function
relief = lamb_lab4_module.reliefRatio(shed)       
print "Add those ratios to the attribute table!"
arcpy.AddField_management(shed,"Relief_Ra","FLOAT")
upCur = arcpy.UpdateCursor(shed)
for i in range(numpoly):
    rows = upCur.next()
    rows.Relief_Ra= relief[i]
    upCur.updateRow(rows)
    print "The 2D Circularity Ratio for polygon",i+1,"is",relief[i]

print "fin"



















