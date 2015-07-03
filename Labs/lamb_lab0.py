'''*********************************************
author: Owen Lamb
Date: 1/16/2013
Purpose: Introduction to python
*********************************************'''
#import arc license and set workspace
import arcpy
import math
from arcpy import env
env.workspace = r'D:\lab0\data'
env.overwriteOutput = 1

# Part 1
#For loop to populate an empty list
files = ['roads', 'cities', 'counties', 'states']
list1= []
for i in files:
    list1.append(i + 'txt')
    print list1

#While loop to raise pi to the nth power until the sum is greater that 10,000
theNumber = math.pi
i = 0
while theNumber**i <= 10000:
    print theNumber**i
    i+= 1
    
# Using the OS modue, create a list of names of files in the lab0 data folder
# Then, Using loopping and branching, create another list of only dbf files.
import os

#define path, a string to the file directory I am working in
path = r"D:\lab0\data"
files = os.listdir(path)
dbfs=[]
#Find .dbf files.
for i in files:
    if '.dbf' in i:
        dbfs.append(i)
        print dbfs
    
#Part II

#define variables
openSpace = 'boulderCountyOpen.shp'

#create list of shapefile names
cities = ['boulder','lafayette','louisville']
roads = ['highways', 'mjrroads', 'mnrroads']
features = cities + roads

#loop through cities list and clip open space to each municipality
for i in features:
    if i in cities:
        arcpy.Clip_analysis(openSpace,i+'.shp',i+'_Open.shp')
        print 'open space clipped to',i,'city limits'
    else:
        arcpy.Buffer_analysis(i+'.shp', i + '_Buffer50.shp' , '50 feet', 'FULL', 'ROUND', 'NONE','#')
        print i, 'buffered 50 feet'

 
print 'analysis complete'