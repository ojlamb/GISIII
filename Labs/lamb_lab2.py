'''*********************************************
Author: Owen Lamb
Date: 1/30/2013
Purpose: Lab 2 Feature Creation and Editing
*********************************************'''
# import necessary modules for the analysis
import arcpy
from arcpy import env
env.workspace = r"D:\lamb_lab2\data"
env.overwriteOutput = 1

print "Declaring variables."
#Declare variables, i.e. existing and new ones you will need
print "*******Part I*********"
print "Reading the textfile."
#Read in the text file information line by line
theme = '14erRoute.shp'
textFile = 'coords.txt'
text = open(env.workspace + '/' + textFile, 'r')
xCoords= text.readline().strip()
yCoords= text.readline().strip()
text.close()
print "Creating the lists of x and y coordinates."
#Create a list of x's and a list of y's from the string objects
xList = xCoords.split(',')
yList = yCoords.split(',')
print "Creating a polyline feature class."
#The feature class will be 'empty' at this point
arcpy.CreateFeatureclass_management(env.workspace, theme, 'POLYLINE')

print "Creating a point object and an array object."     
#The point object will be used to create each of the vertices of the array 
point = arcpy.Point()
array = arcpy.Array()
print "Opening an insert-cursor to create and access a new row."    
#Create an insert cursor on the empty feature class
routeCur = arcpy.InsertCursor(theme)
routeRow = routeCur.newRow()
for i in range(len(xList)):
    point.X = xList[i]
    point.Y = yList[i]
    array.add(point) 

print "Populating geometry with array"
#Populate the shape field of the feature class with the array object
routeRow.shape = array  
routeCur.insertRow(routeRow)
del routeCur, routeRow
     

print "*******Part II********"
print "Conducting 3D analysis"
arcpy.CheckOutExtension('3D')
dem ='dem_lab2'
threeD = 'inter3d.shp'
#Get the Z value of each point from the DEM and then get 2D and 3D lengths
arcpy.InterpolateShape_3d(dem, theme, threeD)
print "Creating 3D shape"
#use 2D polyline and DEM to create 3D polyline

print "Adding fields."
#Add fields (numPnts, 2Dlength and 3Dlength) to 3D feature class
arcpy.AddField_management(threeD,'numPnts', 'LONG')
arcpy.AddField_management(threeD,'Length2d', 'FLOAT')
arcpy.AddField_management(threeD,'Length3d', 'FLOAT')


print "updating fields"
#use cursor to populate numPnts, 2D and 3D length fields
updCur3 = arcpy.UpdateCursor(threeD)
updRow3 = updCur3.next()
updCur2 = arcpy.UpdateCursor(theme)
updRow2 = updCur2.next()


#get number of 2D points Points
numPs = updRow2.shape.pointCount
updRow3.setValue('numPnts',numPs)

# get 2d length
len2d = updRow2.shape.length
updRow3.setValue('Length2d',len2d)
  
#get 3d Length
len3d = updRow3.shape.length3D
updRow3.setValue('Length3d',len3d)
    
#Update the attribute table row
updCur3.updateRow(updRow3)
  
    

del updCur2, updCur3,updRow2, updRow3    
   

    
print "The 2D length is:"
print len2d
print "The 3D length is:"
print len3d
print "The difference is:"
print len3d - len2d
#print out planar and surface lengths and the difference

print "analysis complete hoooray!"