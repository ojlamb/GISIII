'''*********************************************
Author: Owen Lamb
Date: 2/19/2013
Purpose: Lab 3 Spatial Sampling Design
*********************************************'''
#Define function
def pointmaker(point,row):
    ''' The pupose of this function is to create a point feature class out of 
    a list of x coordinates, and y coordinates. The parameters are a point
    feature class, and a new row to put the point.'''
    point.X = myXCoords[i]
    point.Y = myYCoords[i]
    print 'Point properties (inside function): '
    print "x: ", point.X, "y: ", point.Y
    row.shape = point
    print "**********************"
    cursor.insertRow(row)


# import necessary modules for the analysis
print 'importing modules'
import arcpy
from arcpy import env
#Set workspace environment
print ' setting workspace'
env.workspace = r"D:\Lamb_lab3\lab3\data"
env.overwriteOutput = 1
arcpy.CheckOutExtension('Spatial')
#Decelare initial variables.
print 'declaring variables'
#Variable for interest area polygon
theme = 'interestAreas.shp'
#Variable to store the grid points for each interest polygon
points= ['grid1.shp','grid2.shp','grid3.shp']
#Variable to store the buffer polygons for each gridpoint
pointsBuff = ['gridbuff1.shp','gridbuff2.shp','gridbuff3.shp']
#Create variable to store square buffer list
squareBuff = ['squarebuff1.shp','squarebuff2.shp','squarebuff3.shp']
#Variable to store the clipped buffers- ie our interest areas
pointClip = ['gridclip1.shp','gridclip2.shp','gridclip3.shp']
squareClip = ['squareclip1.shp','squareclip2.shp','squareclip3.shp']
#Variable to store the 1992 agriculture raster.
agrast = ['agr1992','agr2001']
stats = ['g1agr1992.dbf','g2agr1992.dbf','g3agr1992.dbf','g1agr2001.dbf','g2agr2001.dbf','g3agr2001.dbf']

#Create a list of mesh size
print "Creating Lists"
#list containing mesh sizes
poly = [2000,3500, 4500]
#Create empty lists to store my coordinates
myXCoords = []
myYCoords = []

#Create search cursor in the theme shapefile
print "Creating Search Cursor"
SCur = arcpy.SearchCursor(theme)

#Iterate through a loop 3 times to get my extents of each polygon
for i in range(len(poly)):
    row = SCur.next()
    ext = row.shape.extent
    xm = ext.XMin
    xMa = ext.XMax
    ym = ext.YMin
    yMa = ext.YMax
    #Populate the lists myXCoords, myYCoords
    while ym < yMa:
        if xm < xMa:
            myXCoords.append(xm)
            myYCoords.append(ym)
            xm = xm + poly[i]
        else:
            ym = ym + poly[i]
            xm = ext.XMin
    arcpy.CreateFeatureclass_management(env.workspace, points[i], "point")
    cursor = arcpy.InsertCursor(points[i])     
    print"Creating Points"
    point = arcpy.Point()
    row = cursor.newRow()
   # Create a new feature class of points named "grid.shp"
    for i in range(0,len(myXCoords)):
        print 'Calling pointmaker function'
        pointmaker(point,row)
        #Alternative method without calling pointmaker function:
#            point.X = myXCoords[i]
#            point.Y = myYCoords[i]
#            row = cursor.newRow()
#            row.shape = point
#            cursor.insertRow(row)
#            print point.X,point.Y
    del cursor
    myXCoords = []
    myYCoords = []   
del SCur, row
#Program for User input to decide to buffer square or round.
userinput = raw_input("Type ROUND for Round buffer zones or SQUARE for square buffers zones around the sample points.")

for i in range(0,len(points)):
    if userinput == 'ROUND':
        print "Buffering 500 meters around each point"
        arcpy.Buffer_analysis(points[i],pointsBuff[i],"500 meters")
        print "Clipping the sample area (gridbuff.shp) to interestarea.shp"
        arcpy.Clip_analysis(pointsBuff[i],theme,pointClip[i])
    elif userinput == 'SQUARE':
        print "Buffering 500 meters around each point"
        arcpy.Buffer_analysis(points[i],pointsBuff[i],"500 meters")
        arcpy.FeatureEnvelopeToPolygon_management (pointsBuff[i], squareBuff[i], "MULTIPART")
        arcpy.Delete_management(pointsBuff[i])
        print "Clipping the sample area (gridbuff.shp) to interestarea.shp"
        arcpy.Clip_analysis(squareBuff[i],theme,squareClip[i])
        

print"Running Zonal Stats"
if userinput == 'ROUND':
    for i in range(0,len(agrast)):
        for j in range(0,len(pointClip)):
            for k in range(0,len(stats)):
                arcpy.sa.ZonalStatisticsAsTable(pointClip[j],'id',agrast[i],stats[k],'DATA','MEAN')
                sCur = arcpy.SearchCursor(stats[k])
                zrow = sCur.next()
                mean = zrow.getValue("MEAN")
            print 'The average intensity of agricultural land in',agrast[i],"for interest area",pointClip[j],"is", mean
if userinput == 'SQUARE':
    for i in range(0,len(agrast)):
        for j in range(0,len(squareClip)):
            for k in range(0,len(stats)):
                arcpy.sa.ZonalStatisticsAsTable(squareClip[j],'id',agrast[i],stats[k],1,'MEAN')
                sCur = arcpy.SearchCursor(stats[k])
                zrow = sCur.next()
                mean = zrow.getValue("MEAN")
            print 'The average intensity of agricultural land in',agrast[i],"for interest area",squareClip[j],"is", mean
print "fin"
    
    
    
    