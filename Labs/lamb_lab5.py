# -*- coding: utf-8 -*-
"""
Created on Wed Mar 06 18:21:23 2013
GIS Programming: Assignment 5
Raster covolution with Numpy
@author: Owen Lamb
"""
#==============================================================================
# import modules
#==============================================================================
from time import clock
start = clock()
print "Import Modules"
import arcpy
from arcpy import env
import arcpy.sa as sa
import numpy as np

#Set workspace environment
print 'Setting Workspace'
env.workspace = r"D:\Lamb_lab5\data"
env.overwriteOutput = 1
arcpy.CheckOutExtension('Spatial')

#==============================================================================
# Define Function
#==============================================================================
print"Defining Function"
def focalMean(numpyarr):
    """
    The purpose of this function is to input a numpy array to get the average of all 
    cells in a neighborhood. The function uses a focal window neighborhood of 11X9 ( 330m by 270m)
    to get the avereage of each cell and assign it to the center cell. Output is a grid, each cell representing 
    the average of its the focal window.
    """
    perGrid = np.zeros(numpyarr.shape).astype(float)
    for i in range (4,np.size(numpyarr,1)-5):
        for j in range (5,np.size(numpyarr,0)-6):
            sum = 0.0
            #Loop through moving window
            for ii in range(i-4,i+5):
                for jj in range(j-5,j+6):
                    sum = sum + numpyarr[jj,ii]
            perGrid[j][i] = float(sum/99.0)*100.0 
    return perGrid
    
    
#==============================================================================
# Declaring input data
#==============================================================================
print "Defining Input Dem and Nlcd"
dem = 'dem_lab5' 
landCover = 'nlcd06_lab5' 

#==============================================================================
# create raster objects
#==============================================================================
print "Creating Raster Objects"
demRas = sa.Raster(dem)
coverRas = sa.Raster(landCover)

#Get raster information
demHeight = demRas.height
demWidth = demRas.height
nlcdHeight = coverRas.height
nlcdWidth = coverRas.height
llpnt = demRas.extent.lowerLeft
demSize = demRas.meanCellHeight
nlcdSize = demRas.meanCellHeight
assert(abs(demRas.meanCellHeight-demRas.meanCellWidth)<0.00001),'Cell size \.astype(float)significantly different'
assert(abs(coverRas.meanCellHeight-coverRas.meanCellWidth)<0.00001)

#convert raster objects to numpy arrays
demArr = arcpy.RasterToNumPyArray(demRas)
nlcdArr = arcpy.RasterToNumPyArray(coverRas)

#Get suitability indexes for each land cover criteria.
print "Running Analysis for Green Area"
nlcdGreen = np.where((nlcdArr == 41)|(nlcdArr==42)|(nlcdArr==43)|(nlcdArr==52),1,0)
greenPer = focalMean(nlcdGreen)
greenSuit = np.zeros(nlcdGreen.shape).astype(float)
greenSuit = np.where((greenPer > 30.0),1,0).astype(float)

print "Running Analysis for Agricultural Area"
nlcdAgr = np.where((nlcdArr == 81)|(nlcdArr==82),1,0)
agrPer = focalMean(nlcdAgr)
agrSuit = np.zeros(nlcdAgr.shape).astype(float)
agrSuit = np.where((agrPer < 5.0),1,0).astype(float)  

print "Running Analysis for Water Area"
nlcdWet = np.where((nlcdArr == 11),1,0)
wetPer = focalMean(nlcdWet)
wetSuit = np.zeros(nlcdWet.shape).astype(float)
wetSuit = np.where((wetPer > 5.0)&(wetPer < 20.0),1,0).astype(float) 

print "Running Analysis for Low Development Area"
nlcdDev = np.where((nlcdArr == 21)|(nlcdArr==22),1,0)
devPer = focalMean(nlcdDev)
devSuit = np.where((devPer < 20.0),1,0).astype(float)     

print "Running Analysis for Slope"
demSlope = sa.Slope(demRas)
slopeArr = arcpy.RasterToNumPyArray(demSlope).astype(float)
slopePer = focalMean(slopeArr)/100
slopeSuit = np.where((slopePer < 8.0),1,0).astype(float)

print "Calculating Suitability Index"
allSuit = np.zeros(nlcdArr.shape).astype(float)
allSuit = greenSuit + agrSuit + wetSuit + devSuit + slopeSuit

print "Adding up All suitable sites"
count = 0
for i in range (np.size(allSuit,1)):
    for j in range (np.size(allSuit,0)):
        if allSuit[j][i] == 5.0:
            count = count + 1
print "Number of suitable locations:",count


print "Converting Numpy Array to Arcpy Raster"
suitRaster = arcpy.NumPyArrayToRaster(allSuit,llpnt,demSize,demSize)
arcpy.DefineProjection_management(suitRaster,demRas.spatialReference)
print "Saving the Suitability Raster"
suitRaster.save('suitOut')
print 'elapsed time: ',round(clock()-start,2),' seconds'

#Slicing Approach
#for row in ..
#    for col ...:
#        win =  ma[row -5:row+6],col-4:col+5]
#        win = win*mask
#        win.sum()

#Circular Window 15*15
#radius = ((.5+winRows)/2)**2+(0.5+winCol)/2)**2)**0.
#Vectorize operations
#Create Boolean Mask
#if winShape =='rectangular':
#    dim = int(dimList[0]/2),int(dimList[1]/2)]
#    mask = np.ones((dim[0]))
#


#Win shift method
#cut out a raster array minus the edge effect
#Loop through and just slide the window across the raster and just add it up.
#Scipi function ndimage.convolve















