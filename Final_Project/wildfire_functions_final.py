"""
Authors: Nick Rachko, Owen Lamb, and David Smith
Date: 4/11/2013
Purpose: The purpose of this script is to create a series of functions for the
static and dynamic variables in a wildfire vulnerability index.  The static variables include
slope, population, median housing value, access, evacuation, land cover, and soil moisture.
The dynamic variable functions include barriers and aspect(wind).
"""

import arcpy
import numpy as np
import arcpy.sa as sa
arcpy.CheckOutExtension("Spatial")

def slopeIndexer(DEM):
    """ The purpose of this function to take a DEM, Calculate the slope, 
    and assign values based off steepness. The slope values
    are given a value 1-5 with a value of five being steeper, and thus more 
    prone to faster moving wildfires. The output is a Numpy Array.
    Input = Raster DEM
    Output = Numpy Array
    """
    slope = arcpy.sa.Slope(DEM)
    slopeArr = arcpy.RasterToNumPyArray(slope)
    slope1 = np.zeros(slopeArr.shape).astype(float)
    slope2 = np.zeros(slopeArr.shape).astype(float)
    slope3 = np.zeros(slopeArr.shape).astype(float)
    slope4 = np.zeros(slopeArr.shape).astype(float)
    slope5 = np.zeros(slopeArr.shape).astype(float)
    
    slope1 = np.where((slopeArr >= 0)&(slopeArr <= 5),1,0) 
    slope2 = np.where((slopeArr > 5)&(slopeArr <= 15),2,0) 
    slope3 = np.where((slopeArr > 15)&(slopeArr <= 30),3,0) 
    slope4 = np.where((slopeArr > 30)&(slopeArr <= 45),4,0)
    slope5 = np.where((slopeArr > 45),5,0)                      
    slopeCrit = slope1 + slope2 + slope3 + slope4 + slope5
    return slopeCrit
    
def housevalIndex(raster):
    """ The purpose of this function to take an input housing value raster, convert
    it into a numpy array, and assign values of 1-5 based on monetary value of an area. 
    The output is a Numpy Array.
    Input = Raster
    Output = Numpy Array
    """
    house = arcpy.RasterToNumPyArray(raster)
    vLC = np.zeros(house.shape).astype(float)
    lC = np.zeros(house.shape).astype(float)
    mC = np.zeros(house.shape).astype(float)
    hC = np.zeros(house.shape).astype(float)
    vHC = np.zeros(house.shape).astype(float)
    vLC = np.where((house>=0)&(house<=95100),1,0)
    lC =  np.where((house>95100)&(house<=128800),2,0)
    mC =  np.where((house>128800)&(house<=140100),3,0)
    hC =  np.where((house>140100)&(house<=157800),4,0)
    vHC =  np.where((house>157800),5,0)
    housevalCrit = vLC + lC + mC + hC + vHC
    return housevalCrit
    
def soilsIndexer(raster):
    """ The purpose of this function to take an input soil raster, convert
    it into a numpy array, and assign values of 1-5 based on the ability of a soil 
    to retain moisture after a rainfall event. The output is a Numpy Array.
    Input = Raster
    Output = Numpy Array
    """
    soils = arcpy.RasterToNumPyArray(raster)
    vLC = np.zeros(soils.shape).astype(float)
    lC = np.zeros(soils.shape).astype(float)
    mC = np.zeros(soils.shape).astype(float)
    hC = np.zeros(soils.shape).astype(float)
    vHC = np.zeros(soils.shape).astype(float)
    vLC = np.where((soils==3)|(soils==4)|(soils==6)|(soils==15)|(soils==8)|(soils==999),1,0)
    lC =  np.where((soils==0)|(soils==9)|(soils==13)|(soils==10),2,0)
    mC =  np.where((soils==5)|(soils==14)|(soils==4),3,0)
    hC =  np.where((soils==1),4,0)
    vHC =  np.where((soils==17)|(soils==12)|(soils==16)|(soils==7)|(soils==11),5,0)
    soilCrit = vLC + lC + mC + hC + vHC
    return soilCrit

def windIndexer(dem, directionlist):
    """ The purpose of this function to take a DEM and convert
    it into an aspect raster, and then into a numpy array based off the 8 cardinal directions.  
    Values of 1-5 will be assigned based on wildfire vulnerability. The output is a
    Numpy Array.
    Input = Raster
    Output = Numpy Array
    """
    asp = arcpy.sa.Aspect(dem)
    aspect = arcpy.RasterToNumPyArray(asp)    
    
    vLC= np.zeros_like(aspect)
    lC = np.zeros_like(aspect)
    mC = np.zeros_like(aspect)
    hC = np.zeros_like(aspect)
    vHC = np.zeros_like(aspect)

    if directionlist == 'N':
        vLC = np.where((aspect>=157.5)&(aspect<=202.5),1,0)         
        lC = np.where((aspect>=202.5)&(aspect<=247.5)|(aspect>=112.5)&(aspect<=157.5),2,0)
        mC = np.where((aspect>=67.5)&(aspect<=112.5)|(aspect>=247.5)&(aspect<=292.5),3,0)
        hC = np.where((aspect>=292.5)&(aspect<=337.5)|(aspect>=22.5)&(aspect<=67.5),4,0)
        vHC = np.where((aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360),5,0)                            
    if directionlist == 'S':
        vLC = np.where((aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360),1,0) 
        lC = np.where((aspect>=292.5)&(aspect<=337.5)|(aspect>=22.5)&(aspect<=67.5),2,0)
        mC = np.where((aspect>=67.5)&(aspect<=112.5)|(aspect>=247.5)&(aspect<=292.5),3,0)
        hC = np.where((aspect>=202.5)&(aspect<=247.5)|(aspect>=112.5)&(aspect<=157.5),4,0)
        vHC = np.where((aspect>=157.5)&(aspect<=202.5),5,0)                                                      
    if directionlist == 'W':
        vLC = np.where((aspect>=67.5)&(aspect<=112.5),1,0)
        lC = np.where((aspect>=22.5)&(aspect<=67.5)|(aspect>=112.5)&(aspect<=157.5),2,0)               
        mC = np.where((aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360)|(aspect>=157.5)&(aspect<=202.5),3,0)
        hC = np.where((aspect>=292.5)&(aspect<=337.5)|(aspect>=202.5)&(aspect<=247.5),4,0)                                   
        vHC = np.where((aspect>=247.5)&(aspect<=292.5),5,0)                                                 
    if directionlist == 'E':
        vLC = np.where((aspect>=247.5)&(aspect<=292.5),1,0)
        lC = np.where((aspect>=292.5)&(aspect<=337.5)|(aspect>=202.5)&(aspect<=247.5),2,0)
        mC = np.where((aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360)|(aspect>=157.5)&(aspect<=202.5) ,3,0)
        hC = np.where((aspect>=22.5)&(aspect<=67.5)|(aspect>=112.5)&(aspect<=157.5),4,0)
        vHC = np.where((aspect>=67.5)&(aspect<=112.5),5,0)
    if directionlist == 'NE':
        vLC = np.where((aspect>=202.5)&(aspect<=247.5),1,0)         
        lC = np.where((aspect>=247.5)&(aspect<=292.5)|(aspect>=157.5)&(aspect<=202.5),2,0)
        mC = np.where((aspect>=292.5)&(aspect<=337.5)|(aspect>=112.5)&(aspect<=157.5),3,0)
        hC = np.where((aspect>=67.5)&(aspect<=112.5)|(aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360),4,0)
        vHC = np.where((aspect>=22.5)&(aspect<=67.5),5,0)                            
    if directionlist == 'SE':
        vLC = np.where((aspect>=292.5)&(aspect<=337.5),1,0) 
        lC = np.where((aspect>=247.5)&(aspect<=292.5)|(aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360),2,0)
        mC = np.where((aspect>=202.5)&(aspect<=247.5)|(aspect>=22.5)&(aspect<=67.5),3,0)
        hC = np.where((aspect>=157.5)&(aspect<=202.5)|(aspect>=67.5)&(aspect<=112.5),4,0)
        vHC = np.where((aspect>=112.5)&(aspect<=157.5),5,0)                                                      
    if directionlist == 'NW':
        vLC = np.where((aspect>=112.5)&(aspect<=157.5),1,0)
        lC = np.where((aspect>=157.5)&(aspect<=202.5)|(aspect>=67.5)&(aspect<=112.5),2,0)               
        mC = np.where((aspect>=202.5)&(aspect<=247.5)|(aspect>=22.5)&(aspect<=67.5),3,0)
        hC = np.where((aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360)|(aspect>=67.5)&(aspect<=112.5),4,0)                                   
        vHC = np.where((aspect>=292.5)&(aspect<=337.5),5,0)                                                 
    if directionlist == 'SW':
        vLC = np.where((aspect>=22.5)&(aspect<=67.5),1,0)
        lC = np.where((aspect>=0)&(aspect<=22.5)|(aspect>=337.5)&(aspect<=360)|(aspect>=67.5)&(aspect<=112.5),2,0)
        mC = np.where((aspect>=292.5)&(aspect<=337.5)|(aspect>=112.5)&(aspect<=157.5),3,0)
        hC = np.where((aspect>=157.5)&(aspect<=202.5)|(aspect>=247.5)&(aspect<=292.5),4,0)
        vHC = np.where((aspect>=202.5)&(aspect<=247.5),5,0)
       
    aspCrit = vLC + lC + mC +hC + vHC
    return aspCrit
    
def nlcdIndexer(raster):
    """ The purpose of this function to take an NLCD raster, convert it into a
    numpy array, and reclassify it into values of 1-5 based on wild-fire 
    vulnerability. The output is a Numpy Array.
    Input = Raster
    Output = Numpy Array
    """
    nlcd = arcpy.RasterToNumPyArray(raster)
    vLC= np.zeros_like(nlcd)
    lC = np.zeros_like(nlcd)
    mC = np.zeros_like(nlcd)
    hC = np.zeros_like(nlcd)
    vHC = np.zeros_like(nlcd)
    
    vLC = np.where((nlcd==11)|(nlcd==12)|(nlcd==31)|(nlcd==95)|(nlcd==90),1,0)
    lC =  np.where((nlcd==21)|(nlcd==22),2,0)
    mC = np.where((nlcd==23)|(nlcd==24)|(nlcd==81),3,0)
    hC = np.where((nlcd==41)|(nlcd==42)|(nlcd==43),4,0)
    vHC = np.where((nlcd==52)|(nlcd==71)|(nlcd==72),5,0)
    #
    nlcdcrit = vLC + lC + mC +hC + vHC
    return nlcdcrit

def accessIndexer(line1,dem):
    """ The purpose of this function to take a distance raster, convert it into a
    numpy array, and using the path distance tool, reclassify it into values of 1-5 based on wild-fire 
    vulnerability. The output is a Numpy Array.  Access is defined as streets, trails,
    and any user chosen avenues for accessing a wildfire.
    Input = Raster
    Output = Numpy Array
    """
    outPathDist = arcpy.sa.PathDistance(line1, in_surface_raster = dem)
    pathD = arcpy.RasterToNumPyArray(outPathDist)  
    
    vLC= np.zeros_like(pathD)
    lC = np.zeros_like(pathD)
    mC = np.zeros_like(pathD)
    hC = np.zeros_like(pathD)
    vHC = np.zeros_like(pathD)
    
    vLC = np.where((pathD <=100),1,0)
    lC = np.where((pathD >100)&(pathD <=500),2,0)
    mC = np.where((pathD >500)&(pathD <=1000),3,0)
    hC = np.where((pathD >1000)&(pathD <=1500),4,0)
    vHC = np.where((pathD >1500),5,0)
    
    accessCrit = vLC + lC + mC +hC + vHC    
    return accessCrit
    
def evacIndexer(lines, dem):
    """ The purpose of this function to take a distance raster, convert it into a
    numpy array, and using the path_distance tool, reclassify it into values of 
    1-5 based on wild-fire vulnerability. The output is a Numpy Array.
    Input = Raster
    Output = Numpy Array
    """
    outPathDist = arcpy.sa.PathDistance(lines, in_surface_raster = dem)
    pathD = arcpy.RasterToNumPyArray(outPathDist)
    
    vLC= np.zeros_like(pathD)
    lC = np.zeros_like(pathD)
    mC = np.zeros_like(pathD)
    hC = np.zeros_like(pathD)
    vHC = np.zeros_like(pathD)
    
    vLC = np.where((pathD <=50),1,0)
    lC = np.where((pathD >50)&(pathD <=250),2,0)
    mC = np.where((pathD >250)&(pathD <=500),3,0)
    hC = np.where((pathD >500)&(pathD <=1000),4,0)
    vHC = np.where((pathD >1000),5,0)
    
    evacCrit = vLC + lC + mC +hC + vHC    
    return evacCrit

def populationIndexer(populationRas):
    """ The purpose of this function to take population data from a raster, convert to a 
    numpy array, and query the array to each index criteria for population classes.
    Cells are given a value 1-5 based on wild-fire vulnerability. Higher pop = higher vulnerability.
    The output is a Numpy Array.
    Input = Raster Population
    Output = Numpy Array
    """
    popArr = arcpy.RasterToNumPyArray(populationRas)
    popIndex = np.zeros(popArr.shape).astype(float)
    pop1 = np.zeros(popArr.shape).astype(float)
    pop2 = np.zeros(popArr.shape).astype(float)
    pop3 = np.zeros(popArr.shape).astype(float)
    pop4 = np.zeros(popArr.shape).astype(float)
    pop5 = np.zeros(popArr.shape).astype(float)
    pop1 = np.where((popArr>= 0)&(popArr <= 1603),1,0) 
    pop2 = np.where((popArr > 1604)&(popArr <= 3207),2,0) 
    pop3 = np.where((popArr > 3208)&(popArr <= 4810),3,0) 
    pop4 = np.where((popArr > 4811)&(popArr <= 6414),4,0)
    pop5 = np.where((popArr > 6415),5,0)                      
    popCrit = pop1 + pop2 + pop3 + pop4 + pop5
    return popCrit

def barrierIndexer(studyArea, roads, windDirection):
    """
    The purpose of this function is to simulate possible fire movement
    given wind direction and main roads as barriers.
    Inputs:
    studyArea = area in which the function operates. (Raster)
    roads = roads to serve as barriers (Raster)
    windDirection = abbreviation of cardinal directions. (String) ex. "NW"
    Output:
    outputArr = Numpy array of values 5's and 1's. (5's = in fires path)(1's = blocked by barrier)
    """
    #Create Numpy Arrays
    studyArr = arcpy.RasterToNumPyArray(studyArea)
    roadArr = arcpy.RasterToNumPyArray(roads)
    #Create boolean array of roads. 1 = road. 0 = not road.
    roadBool = np.zeros(studyArr.shape).astype(float)
    roadBool = np.where((roadArr== 1),1,0)
    #Create an empty grid for output.
    outputArr = np.zeros(studyArr.shape).astype(float)
    if windDirection == "NW":
        print "Running North West Wind Index"
        #Wind Coming From NorthWest
        #Create prohibit grid for flagged values
        prohibitNW = np.ones(studyArr.shape).astype(float)
        for row in range(2,studyArr.shape[0]-2):
            for col in range(2,studyArr.shape[1]-2):
                if roadBool[row-1][col-1]==1:
                    if roadBool[row][col]== 1:
                        prohibitNW[row][col]=0
                        prohibitNW[row+1][col+1] = 0
                        prohibitNW[row+1][col] = 0
                        prohibitNW[row][col+1] = 0
                    if roadBool[row][col]== 0:
                        prohibitNW[row][col]=0
                        prohibitNW[row+1][col+1] = 0
                        prohibitNW[row+1][col] = 0
                        prohibitNW[row][col+1] = 0
                if prohibitNW[row-1][col-1]== 0:
                    prohibitNW[row+1][col+1] = 0
                    prohibitNW[row+1][col] = 0
                    prohibitNW[row][col+1] = 0   
        outputArr = np.where((prohibitNW == 1),5,1)
    if windDirection == "N":           
        print "Running North Wind Index"
        #Wind Coming From the North   
        #Create prohibit grid for flagged values
        prohibitN = np.ones(studyArr.shape).astype(float)
        for col in range(2,studyArr.shape[1]-2):               
            for row in range(2,studyArr.shape[0]-2):
                if roadBool[row-1][col]==1|roadBool[row-1][col-1]==1|roadBool[row-1][col+1]==1:
                    if roadBool[row][col]== 1:
                        prohibitN[row][col]=0
                        prohibitN[row+1][col] = 0
                    if roadBool[row][col]== 0:
                        prohibitN[row][col]=0
                        prohibitN[row+1][col] = 0
                if prohibitN[row-1][col]== 0:
                    prohibitN[row][col]=0
                    prohibitN[row+1][col] = 0
        outputArr = np.where((prohibitN == 1),5,1)       
    if windDirection == "NE":
        print "Running NorthEast Wind Index"
        #Wind Coming From the NorthEast
        #Create prohibit grid for flagged values
        prohibitNE = np.ones(studyArr.shape).astype(float)         
        for row in range(2,studyArr.shape[0]-2):
            for col in range(2,studyArr.shape[1]-2):
                if roadBool[row-1][col+1]==1:
                    if roadBool[row][col]== 1:
                        prohibitNE[row][col]=0
                        prohibitNE[row+1][col-1] = 0
                        prohibitNE[row][col-1] = 0
                        prohibitNE[row+1][col] = 0
                    if roadBool[row][col]== 0:
                        prohibitNE[row][col]=0
                        prohibitNE[row+1][col-1] = 0
                        prohibitNE[row][col-1] = 0
                        prohibitNE[row+1][col] = 0
                if prohibitNE[row-1][col+1]== 0:
                    prohibitNE[row+1][col-1] = 0
                    prohibitNE[row][col-1] = 0
                    prohibitNE[row+1][col] = 0               
        outputArr = np.where((prohibitNE == 1),5,1)
    if windDirection == "W":
        print "Running West Wind Index"
        #Wind Coming From the West
        #Create prohibit grid for flagged values
        prohibitW = np.ones(studyArr.shape).astype(float)
        for col in range(2,studyArr.shape[1]-2):
            for row in range(2,studyArr.shape[0]-2):
                if roadBool[row][col-1]==1|roadBool[row-1][col-1]==1|roadBool[row+1][col-1]==1:
                    if roadBool[row][col]== 1:
                        prohibitW[row][col+1] = 0
                        prohibitW[row][col]=0
                    if roadBool[row][col]== 0:
                       prohibitW[row][col+1] = 0
                       prohibitW[row][col]=0
                if prohibitW[row][col-1]== 0:
                       prohibitW[row][col+1] = 0
                       prohibitW[row][col]=0
        outputArr = np.where((prohibitW == 1),5,1)              
    if windDirection == "SW":
        print "Running South West Wind Index"               
        #Wind Coming from South West
        #Create prohibit grid for flagged values
        prohibitSW = np.ones(studyArr.shape).astype(float)
        row = 1645
        col = 1
        while col <= 1214:
            row = 1645
            while row > 0:
                if roadBool[row+1][col-1]==1 or roadBool[row][col]== 1:
                    prohibitSW[row][col]=0
                    prohibitSW[row-1][col+1] = 0
                    prohibitSW[row][col+1] = 0
                    prohibitSW[row-1][col] = 0
                if prohibitSW[row+1][col-1]==0:
                     prohibitSW[row-1][col+1] = 0
                     prohibitSW[row][col+1] = 0
                     prohibitSW[row-1][col] = 0
                row -= 1
            col += 1
        outputArr = np.where((prohibitSW == 1),5,1)
    if windDirection == "SE":
        print "Running South East Wind Index"
        #Wind Coming from South East
        #Create prohibit grid for flagged values
        prohibitSE = np.ones(studyArr.shape).astype(float)
        row = 1645
        col = 1214
        while col >= 0:
            row = 1645
            while row >= 0:
                if roadBool[row+1][col+1]==1 or roadBool[row][col]== 1:
                    prohibitSE[row][col]=0
                    prohibitSE[row][col-1] = 0
                    prohibitSE[row-1][col] = 0
                    prohibitSE[row-1][col-1] = 0
                if prohibitSE[row+1][col+1]==0:
                    prohibitSE[row][col-1] = 0
                    prohibitSE[row-1][col] = 0
                    prohibitSE[row-1][col-1] = 0
                if prohibitSE[row+1][col+1]== 0:
                       prohibitSE[row-1][col-1] = 0
                       prohibitSE[row][col]=0
                row -= 1
            col -= 1
        outputArr = np.where((prohibitSE == 1),5,1) 
    if windDirection == "E":
        print "Running East Wind Index"          
        #Wind Blowing from the East
        #Create prohibit grid for flagged values
        prohibitE = np.ones(studyArr.shape).astype(float)        
        row = 0
        col = 1214
        while col >= 0:
            row = 0
            while row <= 1645:
                if roadBool[row][col+1]==1:
                    if roadBool[row][col]== 1 or roadBool[row][col]== 0:
                        prohibitE[row][col-1] = 0
                        prohibitE[row][col]=0
                if prohibitE[row][col+1]== 0:
                       prohibitE[row][col-1] = 0
                       prohibitE[row][col]=0
                row += 1
            col -= 1
        outputArr = np.where((prohibitE == 1),5,1)
    if windDirection == "S":
        print "Running South Wind Index"    
        #Wind Coming from the South
        #Create prohibit grid for flagged values
        prohibitS = np.ones(studyArr.shape).astype(float)
        row = 1645
        col = 1214
        while col >= 0:
            row = 1645
            while row >= 0:
                if roadBool[row+1][col+1]==1 or roadBool[row+1][col]==1 or roadBool[row+1][col-1]==1:
                    if roadBool[row][col]== 1:
                        prohibitS[row][col]=0
                        prohibitS[row-1][col] = 0
                    if roadBool[row][col]== 0:
                        prohibitS[row][col]=0
                        prohibitS[row-1][col] = 0
                if prohibitS[row+1][col]== 0:
                       prohibitS[row-1][col] = 0
                row -= 1
            col -= 1
        outputArr = np.where((prohibitS == 1),5,1)
    return outputArr