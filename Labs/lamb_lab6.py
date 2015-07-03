# -*- coding: utf-8 -*-
"""
GIS Programming: Assignment 6
Ecosystem Recovey after Wildfire
Created on Wed Mar 20 17:44:13 2013

@author: Owen Lamb
"""
#==============================================================================
# Importing Modules
#==============================================================================
print "Importing Modules"
import os, sys
from osgeo import gdal
import scipy
import numpy as np
modPath = r"D:\lamb_lab6\lab6materials"
if modPath not in sys.path: sys.path.append(modPath)
from lab6functions import *

#==============================================================================
# Setting Workspace
#==============================================================================
print "Setting Workspace"
path = "D:\lamb_lab6\data"
dempath = path +'\\L5_bigElk\\'
os.chdir(path) 

##==============================================================================
## Define Functions
##==============================================================================
#def zoneStatsAsTable(zoneTable,valueTable):
#    """ The purpose of this function is to calculate zonal statistics
#    Mean, Standard Deviation, Min, and Max, of a valueGrid based on 
#    the corresponding zone. Inputs are two numpy arrays."""
#    zone, zoneG = readRaster(zoneTable)
#    value, valueG = readRaster(valueTable)
#    
#    
#
#    
#    

#==============================================================================
# Declaring variables
#==============================================================================
print "Declaring Variables"
demName = 'bigElkDem.tif'
burnArea = 'fire.shp'
studyArea = 'studyArea.shp'
files = os.listdir(path+'\l5_bigElk')
landsat = 'L5034032'
fireClip = 'Clipped_fire.tif'

#==============================================================================
# Parsing through the lists
#==============================================================================
print "Managing Files"
band3tifs = []
band4tifs = []
for i in range(0,len(files)):
    if '2001' in files[i]:
        continue
    if files[i].endswith('B3.tif'):
        band3tifs.append(files[i])
    elif files[i].endswith('B4.tif'):
        band4tifs.append(files[i])
    elif files[i].endswith('.tif'):
        allTifs.append(files[i])

#==============================================================================
# Part 1
#==============================================================================
clipOut = 'clipDem.tif'
#Clip Dem to Study Area:
demClip,demGT,demG = clipRaster(demName,studyArea)
#Write out Clipped Dem:
writeNumpyArray(demClip,clipOut,demGT,demG.GetProjection())
#Calculate slope and aspect of the dem:
print"Calculating slope and aspect"
demSlope = 'demSlope.tif'
demAspect ='demAsp.tif'
slopeAspect(clipOut,demSlope,demAspect, driver = 'GTiff')
#Read Rasters
demSlp,demSlpG  = readRaster(demSlope)
demAsp, demAspG = readRaster(demAspect)
#Reclass Slop and Aspect Rasters
print"Reclassifying Slope and Aspect Rasters"
slope,histo = reclassByHisto(demSlp,10)
aspect = reclassAspect(demAsp)
#Write Out Rasters
writeNumpyArray(slope,'clip_'+demSlope, demSlpG.GetGeoTransform(),demSlpG.GetProjection())
writeNumpyArray(aspect,'clip_'+demAspect, demAspG.GetGeoTransform(),demAspG.GetProjection())
#Rasterize fire.shp and clip it to the study area:
rasterizePoly(burnArea,'fireRas',pixelSize=30,fld='ID',dvr='GTiff')
burnClip,burnclipGT,burnG = clipRaster('fireRas',studyArea)
writeNumpyArray(burnClip,fireClip, burnclipGT,burnG.GetProjection())
fire, fireG = readRaster(fireClip) 
print "Burn Area Rasterized and Clipped to Study Area"
#Parse Through images and clip them to the study area:
clip3List = []
clip4List = []
for i in range(len(band3tifs)):
	#Clip images to study area:
    clipOut3 ='clipped_'+band3tifs[i]
    clipOut4 ='clipped_'+band4tifs[i]
    b3Clip,b3GT,b3G = clipRaster(dempath + band3tifs[i],studyArea)
    b4Clip,b4GT,b4G = clipRaster(dempath + band4tifs[i],studyArea)
    writeNumpyArray(b3Clip,clipOut3, b3GT,b3G.GetProjection())
    writeNumpyArray(b4Clip,clipOut4, b4GT,b4G.GetProjection())
    clip3List.append(clipOut3)
    clip4List.append(clipOut4)
print "Band Images Clipped to Study Area"
#Calculate NDVI for all years:
time = range(2002,2012)
rrList=[]
year = 2
print"Calculate NDVI with Band 3 and Band 4 2002-2011"
for i in range(len(clip3List)):
    band3, band3G = readRaster(clip3List[i])
    band4, band4G = readRaster(clip4List[i])
    ndvi = (band4-band3)/(band4+band3)
    greenNdvi = np.ma.masked_where(fire == 1,ndvi)
    burnNdvi = np.ma.masked_where(fire == 2,ndvi)
    greenMean = np.mean(greenNdvi)
    recoverRatio = burnNdvi/greenMean
    rrList.append(recoverRatio) 
    meanRecover = np.mean(recoverRatio)
    print "Mean Recovery Ratio for year Two Thousand",year, meanRecover
    year = year+1
print "Calculating the Slope"
#Iterate through each pixel in each raster to calculate the polyfit slope   
slopeList = np.zeros(recoverRatio.shape).astype(float)
stack = np.dstack(rrList)
for i in range(len(stack)):
    for j in range(len(stack[0])):
        stackList = []
        for k in range(len(rrList)):
            stackList.append(stack[i][j][k])
        slope, yint = scipy.polyfit(time,stackList,1)
        slopeList[i][j] = slope     
#Find the mean slope of the recover ratio   
slopeMasked = np.ma.masked_where(fire == 2,slopeList) 
print "The Mean Slope of the Recovery Ratio Is", np.mean(slopeMasked)
#
####==============================================================================
#### Part 2
####==============================================================================
##Run Zonal Stats
#zoneGrid = 'clip_demSlope.tif'
#zoneGrid, zoneG = readRaster(zoneGrid)
#valueGrid = slopeList
#zones = np.unique(zoneGrid)
#sizeTable = len(zones)
#iterator= range(len(zones))
#stats = np.zeros((sizeTable,5))
#
#for i in iterator:
#    check = zones[i]
#    stats[0][i]= check
#    zonal = np.ma.masked_where(zoneGrid == check, valueGrid)
#    stats[1][i]= np.ma.mean(zonal)
#    stats[2][i]= np.ma.min(zonal)
#    stats[3][i]= np.ma.max(zonal)
#    stats[4][i]= np.ma.std(zonal)
#
#print stats











    
