"""********************************************************
Created on Wed Jan 23 17:44:48 2013
Lab 1: Temporal analysis with vector data.
Author: Owen Lamb
*******************************************************"""
#Import Modules
import arcpy
from arcpy import env
#set workspace
env.workspace = r"D:\lamb_lab1\data"
env.overwriteOutput = 1

#create your list of year values
dates = range(1972,1979)
print 'Creating iterable of years'

#buffer soil sample feature class
soilSample = 'soil_sample' 
soilBuffer = soilSample + '_Buffer500.shp'
arcpy.Buffer_analysis(soilSample + '.shp',soilBuffer , '500 Meters')
print 'Buffering soil layer'

#create search cursor for soil_sample.shp
soilCur = arcpy.SearchCursor(soilSample+ '.shp')
soilRow = soilCur.next()
print 'Opening search cursor on soil layer'

#loop through each year of analysis
#fill in the blank:
for year in dates:
     #dynamically declare variables that you will need
     polygonTheme = 'forestArea_' + str(year)+ '.shp' 
     pointTheme = soilSample +'.shp'
     polyClip ='forestClip_'+str(year)+'.shp'
     print "Declaring variables needed for year",year
     #add a field "data_year" to the forest table
     arcpy.AddField_management(polygonTheme, 'data_year','SHORT')
     print "Adding year field to",polygonTheme
     #calculate the field "data_year"
     arcpy.CalculateField_management(polygonTheme,'data_year', year)
     print "Calculating year field of",polygonTheme
     #clip the forest polygon to the buffered soil sample point
     arcpy.Clip_analysis(polygonTheme, soilBuffer, polyClip)
     print "Clipping:",polygonTheme,"to buffered point"
     #add needed fields to the result of the clip operation
     arcpy.AddField_management(polyClip,'for_Area','DOUBLE')
     print "Adding fields to",polyClip
     #get area from the clipped forest polygon theme
     #populate the for_area field with the area retrieved
     areaCur = arcpy.SearchCursor(polyClip)
     aRow = areaCur.next()
     area = aRow.shape.area
     arcpy.CalculateField_management(polyClip, 'for_Area', area, 'VB')
     print "Getting the forest area for the year",year
     print "Calculating the 'for_area' field of",polyClip
     #get the soil result for the corresponding year
     arcpy.AddField_management(polyClip,'soil_smp','DOUBLE')
     soilVal = soilRow.getValue('year'+ str(year))
     print "Getting soil result from",pointTheme
     #populate the "soil_smp" field in the clipped theme
     arcpy.CalculateField_management(polyClip, 'soil_smp', soilVal)
     print "Calculating 'soil_smp' field of",polyClip
     #print values of forest area and soil sample
     print "The forest area in",year,"was",area,"and the soil \
     measurement was",soilVal
     del aRow, areaCur, area
     #this prototype provides you with intuitive names for all of these variables
     #if you use different variable names, you will need to change the print
     #statements.