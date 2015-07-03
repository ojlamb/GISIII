'''*************************************************************
Authors: Nick Rachko, Owen Lamb, and David Smith
Date: 4/11/2013
Purpose: The purpose of this script is to assess the vulnerability of a given
location to a wildfire event.  The script includes both static and dynamic variables
that can be adapted to fit any location and is designed to include a series of
output grids over a given period of time.  The static variables include slope,
population density, income level, streets, trails, landcover, and soils.  The 
dynamic variables include aspect(wind), barriers (hydrological and transportation based), 
precipitation, humidity, wind direction, wind speed, and temperature. The final 
output is a series of vulerability rasters where each cell is assigned a numeric value.  
*******************************************'''
#==============================================================================
# Modules neccesary: arcpy, spatial analyst, numpy, os, sys
#==============================================================================
print 'importing modules'
import numpy as np
import arcpy
from arcpy import env
from arcpy.sa import *
import os
import sys

print 'setting workspace'
env.workspace = r'C:\Users\Mintberry Crunch\Desktop\Final_Data'
env.overwriteOutput = 1

print 'setting snap raster environment'
arcpy.env.snapRaster = r'C:\Users\Mintberry Crunch\Desktop\Final_Data\citylim_rast'
arcpy.env.extent = r'C:\Users\Mintberry Crunch\Desktop\Final_Data\citylim_rast'

#==============================================================================
# Linking to our functions module "wildfire_functions_Final
#==============================================================================
print 'setting dynamic variables path' 
path = r'C:\Users\Mintberry Crunch\Desktop\Final_Data'
modPath = r'C:\Users\Mintberry Crunch\Desktop\Final_Data'
if modPath not in sys.path: sys.path.append(modPath)
from wildfire_functions_final import *

print 'checking out extensions'
arcpy.CheckOutExtension('Spatial')
#==============================================================================
# Defining variables 
#==============================================================================
print 'creating objects'
studyrast = 'citylim_rast'
studyShape = "BoulderCityLimits.shp"
mainroad = 'Mainrd.shp'
nlcd = "bouldernlcd.tif"
censpop = 'BoulderCountyCensusBlockGroups.shp'
medhval = 'medhousval.shp'
soils = 'soils_final.shp'
accessrast = 'accessrast'
evacrast = 'streetrast.tif'
dem = sa.Raster("boulderdem")
studyArr = arcpy.RasterToNumPyArray(studyrast)
#==============================================================================
# Pre-processing data: rasterizing, clipping etc.
#==============================================================================

print 'storing spatial reference information'
cellSize = dem.meanCellHeight
spref = dem.spatialReference
llpnt = dem.extent.lowerLeft

print 'converting features to raster'
popdenrast = arcpy.FeatureToRaster_conversion(censpop, 'POP10_SQMI', 'popdenrast', 30)     
incomerast = arcpy.FeatureToRaster_conversion(medhval, 'co_tdg_MED', 'incomerast', 30)
roadrast = arcpy.FeatureToRaster_conversion(mainroad, 'IsRoad', 'roadrast', 30)
soilrast = arcpy.FeatureToRaster_conversion(soils, 'texture', 'soilsrast', 30)

print 'clipping rasters to study area'
arcpy.Clip_management(evacrast, "", 'streetclip', studyrast, "", 'NONE')
arcpy.Clip_management(accessrast, "", 'trailclip', studyrast, "", 'NONE')
arcpy.Clip_management(popdenrast, "", 'popclip', studyrast, "", 'NONE')
arcpy.Clip_management(incomerast, "", 'medvalclip', studyrast, "", 'NONE')
arcpy.Clip_management(soilrast, "", 'soilclip', studyrast, "", 'NONE')
arcpy.Clip_management(roadrast, "", 'roadclip', studyrast, "", 'NONE')

#==============================================================================
# Calling static variable functions. 
#==============================================================================
print 'beginning analysis of static variables'
slopeArray = slopeIndexer(dem)
nlcdArray = nlcdIndexer(nlcd)
medvalArray = housevalIndex('medvalclip')
popdenArray = populationIndexer('popclip')
soilArray = soilsIndexer('soilclip')
accessArray = accessIndexer('trailclip', dem)
evacArray = evacIndexer('streetclip', dem)

print 'creating final vulnerability array of static variables'
staticArray = (medvalArray*2) + (popdenArray*2) + (evacArray*1.25) + (slopeArray*3) + (nlcdArray*2.5) + (soilArray*1) + (accessArray*1.25)
finalStatic = arcpy.NumPyArrayToRaster(staticArray.astype(float),llpnt,cellSize,cellSize)
arcpy.DefineProjection_management(finalStatic,spref)
finalStatic.save("staticrast")

print 'static variable analysis complete'

print 'beginning analysis of dynamic variables'
#==============================================================================
# Opening text files and extracting data containing information about precipitation
# wind speed, and wind direction for any given day in our study period
#==============================================================================
print 'importing dynamic variables into lists'
wind = 'winspd.txt'
winspdtxt = open(path + '/' + wind, 'r')
windy = winspdtxt.readline()
winspdtxt.close()
windlist = windy.split(',')

direction = 'windir.txt' 
windirtxt = open(path + '/'+ direction,'r')
winddir = windirtxt.readline()
windirtxt.close()
dirlist = winddir.split(',')

dayday = 'days.txt'
daystxt = open(path + '/' + dayday, 'r')
days = daystxt.readline()
daystxt.close()
dayslist = days.split(',')

ind = 'index.txt'
indextxt = open(path + '/' + ind, 'r')
index = indextxt.readline()
indextxt.close()
indexlist = index.split(',')

#==============================================================================
# Looping through list for each day, running dynamic functions, adding static
# arrays to dynamic array. Converting it to Raster. Clipping to study area. Saving.
#==============================================================================
studyArr = arcpy.RasterToNumPyArray(studyrast)
#vulnrast = "vulnrast"

for i in range(len(dayslist)):
    windval = windIndexer(dem,dirlist[i])
    barrier = barrierIndexer(studyrast, 'roadclip', dirlist[i])
    dynamArray = np.where((barrier==5),indexlist[i],0).astype(float)
    lowWind = float(indexlist[i])*.1
    medWind = float(indexlist[i])*.3
    highWind = float(indexlist[i])*.6
    if windlist[i]== "12":
        windspeed = np.where((barrier == 1),medWind,0)
    if windlist[i]=="15":
        windspeed = np.where((barrier == 1),highWind,0)
    else:
        windspeed = np.where((barrier == 1),lowWind,0)
    vulnArray = staticArray + dynamArray + windspeed + (windval*3)
    finalRast = arcpy.NumPyArrayToRaster(vulnArray.astype(int),llpnt,cellSize,cellSize)
    vulnrast = arcpy.Clip_management(finalRast,"",'vulnrast',studyShape,"",1)
    output = sa.Raster(vulnrast)
    arcpy.DefineProjection_management(output,spref)
    output.save('VulIndex_'+dayslist[i])

print 'analysis complete'  

