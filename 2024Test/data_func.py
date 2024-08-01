
#-----------------------------------------------------------------------
# Copyright (C) 2020, All rights reserved
#
# Peng Wang
#
#-----------------------------------------------------------------------
#=======================================================================
# 
# DESCRIPTION:
# This software is part of a python library to assist in developing and
# analyzing evacuation simulation results from Fire Dynamics Simulator with Evacuation (FDS+Evac).
# FDS+Evac is an open source software package developed by NIST. The source
# code is available at: https://github.com/firemodels/fds
#

# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@gmail.com

import sys, os
import pygame
import pygame.draw
import numpy as np
#from agent_model_obst3 import *
from agent_model import *
from obst import *
#from passage import *
from math_func import *
from math import *
#from config import *
import re
import random
import csv
#from ctypes import *
import struct
import time
try:
    import matplotlib.pyplot as plt
except:
    print("Warning: matplotlib cannot be imported.  Unable to plot figures!")
    if sys.version_info[0] == 2: 
        raw_input("Please check!")
    else:
        input("please check!")


def readDoorProb(FileName, doorIndex, showdata=True):
    findMESH=False
    doorProb=[]
    for line in open(FileName):
        if re.match('&DoorProb', line):
            findMESH=True
            row=[]
        if  findMESH:
            if re.search('prob=', line):
                dataTemp=line.split('prob=')
                #print('dataTemp:', dataTemp[1:])

                #for index in range(len(dataTemp[1:])):
                #    probDist=dataTemp[index+1].lstrip('[').strip('=').rstrip(']')
                probDist=dataTemp[1].lstrip('[').strip('=').rstrip(']')
                temp2 =  re.split(r'[\s\,]+', probDist)
                print(temp2)
                prob = float(temp2[doorIndex+1].lstrip('[').strip('=').rstrip(']'))
                row.append(prob)
                #print(row)

                    #xpoints = temp2[0]
                    #ypoints = temp2[1]
            '''
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            '''
            if re.search('WellDone!', line):
                findMESH = False
                #doorProb.append(dataTemp[1:])
                doorProb.append(row)
                # return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored

    print('doorProb', doorProb)
    (NRow, NColomn) = np.shape(doorProb)  
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(doorProb[i][j])
    print('matrix', matrix)
    if showdata:
        plt.plot(matrix)
        plt.grid()
        plt.show()
    return matrix


def readCSV_base(fileName):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    print(reader)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    dataNP = np.array(strData)
    #print (dataNP)
    #print ('np.shape(dataNP)', np.shape(dataNP))
    #print ('\n')

    #print(strData[1:,1:])
    csvFile.close()
    return dataNP


def getData(fileName, strNote):
    dataFeatures = readCSV_base(fileName)

    Num_Data = len(dataFeatures)
    
    IPedStart=0
    Find = False
    #print(dataFeatures)
    for i in range(Num_Data):
        if len(dataFeatures[i]):
            if dataFeatures[i][0]==strNote:
                IPedStart=i
                Find = True
    
    if Find is False:
        return [], 0, 0
        #IPedStart = None
        #IPedEnd = None
        #dataOK = None
        #return dataOK, IPedStart, IPedEnd
        #return [], 0, 0
    else:
        IPedEnd=IPedStart
        for j in range(IPedStart, Num_Data):
            if len(dataFeatures[j]):
                if dataFeatures[j][0]=='' or dataFeatures[j][0]==' ':
                    IPedEnd=j
                    break
            else: #len(dataFeatures[j])==0: Namely dataFeatures[j]==[]
                IPedEnd=j
                break
            if j==Num_Data-1:
                IPedEnd=Num_Data

        dataOK = dataFeatures[IPedStart : IPedEnd]
        return dataOK, IPedStart, IPedEnd

    #data_result = np.array(dataOK)
    #return data_result[1:, 1:]
    

# This function is not used in this program
def readCSV(fileName, mode='float'):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    #print(strData)
    #print('np.shape(strData)=', np.shape(strData))
    #print('\n')

    print('\n')
    print('#=======================#')
    print(fileName)
    dataNP = np.array(strData)
    print (dataNP)
    print('np.shape(dataNP)', np.shape(dataNP))
    print('\n')

    #print(strData[1:,1:])
    csvFile.close()	
    
    if mode=='string':
        print (dataNP[1:, 1:])
        return dataNP[1:, 1:]
	
    if mode=='float':
        
        #print dataNP[1:, 1:]
        (I, J) = np.shape(dataNP)
        #print "The size of tha above matrix:", [I, J]
        #print "The effective data size:", [I-1, J-1]
        matrix = np.zeros((I, J))
        #print matrix

        for i in range(1,I):
            for j in range(1,J):
                matrix[i,j] = float(dataNP[i,j])

    print (matrix[1:, 1:])
    return matrix[1:, 1:]
    

def arr1D_2D(data, debug=True):
    #data is in type of 1D array, but it is actually a 2D data format.  
    
    NRow = len(data)
    NColomn = len(data[1])
    matrix = np.zeros((NRow, NColomn), dtype='|S20')
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = data[i][j]
    if debug:
        print('Data in 2D array:\n', matrix)
        
    return matrix


def readFloatArray(tableFeatures, NRow, NColomn, debug=True):

    #tableFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Ped2Exit')
    matrix = np.zeros((NRow, NColomn))
    for i in range(NRow):
            for j in range(NColomn):
                matrix[i,j] = float(tableFeatures[i+1][j+1])
    if debug:
        print(tableFeatures, '\n')
        print('Data in Table:', '\n', matrix)
    return matrix


# The file to record the some output data of the simulation
# f = open("outData.txt", "w+")

def readAgents(FileName, debug=True, marginTitle=1, ini=1):

    #dataFeatures = readCSV_base(FileName)
    #[Num_Data, Num_Features] = np.shape(dataFeatures)   

    agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Ped')
    Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&agent')
        Num_Agents=len(agentFeatures)-marginTitle
    if Num_Agents <= 0:
        agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent')
        Num_Agents=len(agentFeatures)-marginTitle

    if debug: 
        print ('Number of Agents:', Num_Agents, '\n')
        print ("Features of Agents\n", agentFeatures, "\n")

    agents = []
    for agentFeature in agentFeatures[marginTitle:]:
        agent = person()
        agent.pos = np.array([float(agentFeature[ini+0]), float(agentFeature[ini+1])])
        agent.dest= np.array([float(agentFeature[ini+2]), float(agentFeature[ini+3])])
        agent.tau = float(agentFeature[ini+4])
        agent.tpre = float(agentFeature[ini+5])
        agent.p = float(agentFeature[ini+6])
        agent.pMode = agentFeature[ini+7]
        agent.aType = agentFeature[ini+8]
        agent.interactionRange = float(agentFeature[ini+9])
        agent.ID = int(agentFeature[ini+10])
        agent.moving_tau = float(agentFeature[ini+11])
        agent.tpre_tau = float(agentFeature[ini+12])
        agent.talk_tau = float(agentFeature[ini+13])
        agent.talk_prob = float(agentFeature[ini+14])
        agent.inComp = int(agentFeature[ini+15])
        agents.append(agent)
        
    return agents


# This function addAgent() is actually not that meaningful.  We just leave it here for future optional development.  
# Because many agent features cannot be added by using the graphic user interface.
# Such as group features and door selection features.
def addAgent(agents, x_pos, y_pos):
    num = len(agents)
    agent = person()
    agent.pos = np.array([float(x_pos), float(y_pos)])
    agent.ID = int(num)
    agent.inComp = int(1)

    # add agent into the list of agents
    agents.append(agent)
    

def readWalls(FileName, debug=True, marginTitle=1, ini=1):
    #obstFeatures = readCSV(FileName, "string")
    #[Num_Obsts, Num_Features] = np.shape(obstFeatures)

    obstFeatures, lowerIndex, upperIndex = getData(FileName, '&Wall')
    Num_Obsts=len(obstFeatures)-marginTitle
    if Num_Obsts <= 0:
        obstFeatures, lowerIndex, upperIndex = getData(FileName, '&wall')
        Num_Obsts=len(obstFeatures)-marginTitle

    if debug:
        print ('Number of Walls:', Num_Obsts, '\n')
        print ("Features of Walls\n", obstFeatures, "\n")
    
    walls = []
    for obstFeature in obstFeatures[marginTitle:]:
        wall = obst()
        wall.params[0]= float(obstFeature[ini+0])
        wall.params[1]= float(obstFeature[ini+1])
        wall.params[2]= float(obstFeature[ini+2])
        wall.params[3]= float(obstFeature[ini+3])
        wall.arrow = int(obstFeature[ini+4])
        wall.id = int(obstFeature[ini+5])
        wall.inComp = int(obstFeature[ini+6])
        wall.mode = obstFeature[ini+7]
        #wall.pointer1 = np.array([float(obstFeature[8]), float(obstFeature[9])])
        #wall.pointer2 = np.array([float(obstFeature[10]), float(obstFeature[11])])
        walls.append(wall)
        
    return walls


#This function addWall() is created for users to add wall in testGeom()
def addWall(walls, startPt, endPt, mode='line'):
    num = len(walls)
    wall = obst()
    
    if mode == 'line':
        wall.params[0]= float(startPt[0])
        wall.params[1]= float(startPt[1])
        wall.params[2]= float(endPt[0])
        wall.params[3]= float(endPt[1])
    if mode == 'rect':
        wall.params[0]= float(startPt[0])
        wall.params[1]= float(startPt[1])
        wall.params[2]= float(endPt[0])
        wall.params[3]= float(endPt[1])

    # The wall arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    wall.arrow = 0 #normalize(endPt - startPt)
    
    wall.mode = mode
    wall.id = int(num)
    wall.inComp = int(1)

    # Add wall into the list of walls
    walls.append(wall)


def readDoors(FileName, debug=True, marginTitle=1, ini=1):
    #doorFeatures = readCSV(FileName, "string")
    #[Num_Doors, Num_Features] = np.shape(doorFeatures)

    doorFeatures, lowerIndex, upperIndex = getData(FileName, '&Door')
    Num_Doors=len(doorFeatures)-marginTitle
    if Num_Doors <= 0:
        doorFeatures, lowerIndex, upperIndex = getData(FileName, '&door')
        Num_Doors=len(doorFeatures)-marginTitle

    if debug:
        print ('Number of Doors:', Num_Doors, '\n')
        print ('Features of Doors\n', doorFeatures, "\n")
    
    doors = []
    for doorFeature in doorFeatures[marginTitle:]:
        door = passage()
        door.params[0]= float(doorFeature[ini+0])
        door.params[1]= float(doorFeature[ini+1])
        door.params[2]= float(doorFeature[ini+2])
        door.params[3]= float(doorFeature[ini+3])
        door.arrow = int(doorFeature[ini+4])
        door.id = int(doorFeature[ini+5])
        door.inComp = int(doorFeature[ini+6])
        door.exitSign = int(doorFeature[ini+7])
        door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
        doors.append(door)
        
    return doors


#This function addDoor() is created for users to add door in testGeom()
def addDoor(doors, startPt, endPt, mode='rect'):
    num = len(doors)
    door = passage()
    
    if mode == 'rect':
        door.params[0]= float(startPt[0])
        door.params[1]= float(startPt[1])
        door.params[2]= float(endPt[0])
        door.params[3]= float(endPt[1])

    # The arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    door.arrow = 0 #normalize(endPt - startPt)
    
    #door.mode = mode   # Currently door has no attribute of "mode"

    door.id = int(num)
    door.inComp = int(1)
    door.exitSign = int(0) # Default: there is no exit sign 
    door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
    
    # Add door into the list of doors
    doors.append(door)
    

#[Num_Doors, Num_DoorFeatures] = np.shape(doorFeatures)
#if np.shape(agent2doors)[0]!= Num_Agents or np.shape(agent2doors)[1]!= Num_Doors:
#    print '\nError on input data: doors or agent2doors \n'
#    print >>f, '\nError on input data: doors or agent2doors \n'


def readExits(FileName, debug=True, marginTitle=1, ini=1):
    #exitFeatures = readCSV(FileName, "string")
    #[Num_Exits, Num_Features] = np.shape(exitFeatures)

    exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Exit')
    Num_Exits=len(exitFeatures)-marginTitle
    if Num_Exits <= 0:
        exitFeatures, lowerIndex, upperIndex = getData(FileName, '&exit')
        Num_Exits=len(exitFeatures)-marginTitle

    if debug: 
        print ('Number of Exits:', Num_Exits, '\n')
        print ("Features of Exits\n", exitFeatures, "\n")
    
    exits = []
    for exitFeature in exitFeatures[marginTitle:]:
        exit = passage()
        exit.params[0]= float(exitFeature[ini+0])
        exit.params[1]= float(exitFeature[ini+1])
        exit.params[2]= float(exitFeature[ini+2])
        exit.params[3]= float(exitFeature[ini+3])
        exit.arrow = int(exitFeature[ini+4])
        exit.id = int(exitFeature[ini+5])
        exit.inComp = int(exitFeature[ini+6])
        exit.exitSign = int(exitFeature[ini+7])
        exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
        exits.append(exit)
        
    return exits


#This function addDoor() is created for users to add door in testGeom()
def addExit(exits, startPt, endPt, mode='rect'):
    num = len(exits)
    exit = passage()
    
    if mode == 'rect':
        exit.params[0]= float(startPt[0])
        exit.params[1]= float(startPt[1])
        exit.params[2]= float(endPt[0])
        exit.params[3]= float(endPt[1])

    # The arrow is to be tested in simulation.  
    # The default value is no direction assigned, i.e., zero.  
    exit.arrow = 0 #normalize(endPt - startPt)
    
    #exit.mode = mode   # Currently passage class has no attribute of "mode"

    exit.id = int(num)
    exit.inComp = int(1)
    exit.exitSign = int(1) # Default there is an exit sign
    exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
    
    # Add exit into the list of exits
    exits.append(exit)

    

##############################################
# This function will be used to read CHID from FDS input file
def readCHID(FileName):

    findHEAD=False
    for line in open(FileName):
        if re.match('&HEAD', line):
            findHEAD=True
        if  findHEAD:
            if re.search('CHID', line):
                temp1=line.split('CHID')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                return keyInfo
            if re.search('/', line):
                findHEAD = False
    return None

# Find the first &MESH line in FDS input file and return the value
def readMesh(FileName):
    findMESH=False
    for line in open(FileName):
        if re.match('&MESH', line):
            findMESH=True
        if  findMESH:
            if re.search('IJK', line):
                temp1=line.split('IJK')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xpoints = temp2[0]
                ypoints = temp2[1]
            if re.search('XB', line):
                temp1=line.split('XB')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                xmax = temp2[1]-temp2[0]
                ymax = temp2[3]-temp2[2]
            if re.search('/', line):
                findMESH = False
                return xpoints, ypoints, xmax, ymax
                # Only find the first &MESH line
                # The second or other MESH lines are ignored
    return None



def readTEnd(FileName):
    
    findTIME=False
    for line in open(FileName):
        if re.match('&TIME', line):
            findTIME=True
        if  findTIME:
            if re.search('T_END', line):
                temp1=line.split('T_END')
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                return keyInfo   # Return a string
            if re.search('/', line):
                findTIME = False
            
    keyInfo=0.0    #If T_END is not found, then return 0.0
    return keyInfo
    #return None
    

# To be added
def readKeyOnce(FileName, Title, Key):
    findTitle=False
    for line in open(FileName):
        if re.match(Title, line):
            findTitle=True
        if  findTitle:
            if re.search(Key, line):
                temp1=line.split(Key)
                line1=temp1[1].strip().strip('=').strip()
                temp2 =  re.split(r'[\s\,]+', line1)
                keyInfo = temp2[0]
                findTitle=False
                return keyInfo
            #if re.match(Title, line)==False and re.match('&', line):
            if re.search('/', line):
                findTitle = False
    return None



### A illustration of OBST PATH and EXIT in RECTANGULAR SHAPE
##############################
### p1-----------------p4  ###
###  |                  |  ###
###  |                  |  ###
###  |                  |  ###
### p2-----------------p3  ###
##############################
            
##############################################
# This function will be used to read OBST from FDS input file
def readOBST(FileName, Keyword='&OBST', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("OBSTout.txt", "w+")
    obstFeatures = []
    findOBST=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findOBST=True
        if  findOBST:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip().strip('=').strip()
                #line1=temp1[1].strip('= ')
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()
                coords = re.split(r'[\s\,]+', dataXYZ)
                print(coords)
                obstFeature = []
                obstFeature.append(float(coords[0]))
                obstFeature.append(float(coords[2]))
                obstFeature.append(float(coords[1]))
                obstFeature.append(float(coords[3]))
                obstFeature.append(float(coords[4]))
                obstFeature.append(float(coords[5].rstrip('/')))
                obstFeatures.append(obstFeature)
                findOBST=False

            if debug:
                print (line, '\n', obstFeature)
                #print >>fo, line
                #print >>fo, obstFeature

            #print >>fo, 'test\n'
            #print >>fo, 'OBST Features\n'
            #print >>fo, obstFeatures
    
    if outputFile!=None:
        with open(outputFile, mode='w+') as obst_test_file:
            csv_writer = csv.writer(obst_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/mode'])
            index_temp=0
            for obstFeature in obstFeatures:
                if obstFeature[4]<Zmin and obstFeature[5]<Zmin:
                    continue
                if obstFeature[4]>Zmax and obstFeature[5]>Zmax:
                    continue
                csv_writer.writerow(['--', str(obstFeature[0]), str(obstFeature[1]), str(obstFeature[2]), str(obstFeature[3]), '0', str(index_temp), '1', 'rect'])
                index_temp=index_temp+1
    
    walls = []
    index = 0
    for obstFeature in obstFeatures:
        if obstFeature[4]<Zmin and obstFeature[5]<Zmin:
            continue
        if obstFeature[4]>Zmax and obstFeature[5]>Zmax:
            continue
        wall = obst()
        wall.params[0]= float(obstFeature[0])
        wall.params[1]= float(obstFeature[1])
        wall.params[2]= float(obstFeature[2])
        wall.params[3]= float(obstFeature[3])
        wall.arrow = 0
        wall.id = index
        wall.inComp = 1
        wall.mode = 'rect'
        walls.append(wall)
        index = index+1
    return walls


#######################################################
# This function will be used to read HOLE or DOOR from FDS input file
def readPATH(FileName, Keyword='&HOLE', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("HOLEout.txt", "w+")
    holeFeatures = []
    
    findPATH=False
    findPATH_XB=False
    findPATH_IOR=False
    for line in open(FileName):
        if re.match(Keyword, line):
            findPATH=True
            findPATH_XB=True
            findPATH_IOR=True
            
        if findPATH:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip().strip('=').strip()
                #line1=temp1[1]
                #temp =  line1.split('=')
                #dataXYZ = temp[1].strip()    
                coords = re.split(r'[\s\,]+', dataXYZ)
                
        #if findPATH and findPATH_IOR:
        #    if re.search('IOR', line):
        #        temp1=line.split('IOR')
        #        dataXYZ=temp1[1].strip().strip('=').strip()
        #        result_IOR = re.split(r'[\s\,]+', dataXYZ)              
        #if findPATH and not findPATH_XB and not findPATH_IOR:            
                holeFeature = []
                holeFeature.append(float(coords[0]))
                holeFeature.append(float(coords[2]))
                holeFeature.append(float(coords[1]))
                holeFeature.append(float(coords[3]))
                holeFeature.append(float(coords[4]))
                holeFeature.append(float(coords[5].rstrip('/')))
                holeFeatures.append(holeFeature)
                findPATH=False

                if debug:
                    print (line, '\n', holeFeature)
                    #print >>fo, line
                    #print >>fo, holeFeature

                #print >>fo, 'test\n'
                #print >>fo, 'HOLE Features\n'
                #print >>fo, holeFeatures

    if outputFile!=None:
        with open(outputFile, mode='w+') as door_test_file:
            csv_writer = csv.writer(door_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
            index_temp=0
            for holeFeature in holeFeatures:
                if holeFeature[4]<Zmin and holeFeature[5]<Zmin:
                    continue
                if holeFeature[4]>Zmax and holeFeature[5]>Zmax:
                    continue
                csv_writer.writerow(['--', str(holeFeature[0]), str(holeFeature[1]), str(holeFeature[2]), str(holeFeature[3]), '0', str(index_temp), '1', '0'])
                index_temp=index_temp+1

    doors = []
    index = 0
    for holeFeature in holeFeatures:
        if holeFeature[4]<Zmin and holeFeature[5]<Zmin:
            continue
        if holeFeature[4]>Zmax and holeFeature[5]>Zmax:
            continue
        door = passage()
        door.params[0]= float(holeFeature[0])
        door.params[1]= float(holeFeature[1])
        door.params[2]= float(holeFeature[2])
        door.params[3]= float(holeFeature[3])
        door.arrow = 0
        door.id = index
        door.inComp = 1
        door.exitSign = 0
        door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
        doors.append(door)
        index = index+1
    return doors


##############################################
# This function will be used to read EXIT from FDS input file
def readEXIT(FileName, Keyword='&EXIT', Zmin=0.0, Zmax=3.0, outputFile=None, debug=True):
    #fo = open("EXITout.txt", "w+")
    exitFeatures = []
    findEXIT=False
    findEXIT_XB=False
    findEXIT_IOR=False
    
    for line in open(FileName):
        if re.match(Keyword, line):
            findEXIT=True
            findEXIT_XB=True
            findEXIT_IOR=True
            
        if findEXIT:
            if re.search('XB', line):
                temp1=line.split('XB')
                dataXYZ=temp1[1].strip().strip('=').strip()
                #line1=temp1[1]
                #temp =  line1.split('=')
                #dataXYZ = temp[1]
                #coords = dataXYZ.split(',')
                coords = re.split(r'[\s\,]+', dataXYZ)
                
        #if findEXIT and findEXIT_IOR:
        #    if re.search('IOR', line):
        #        temp1=line.split('IOR')
        #        dataXYZ=temp1[1].strip().strip('=').strip()
        #        result_IOR = re.split(r'[\s\,]+', dataXYZ)              
        #if findEXIT and not findEXIT_XB and not findEXIT_IOR:
                exitFeature = []
                exitFeature.append(float(coords[0]))
                exitFeature.append(float(coords[2]))
                exitFeature.append(float(coords[1]))
                exitFeature.append(float(coords[3]))
                exitFeature.append(float(coords[4]))
                exitFeature.append(float(coords[5].rstrip('/')))
                exitFeatures.append(exitFeature)
                findEXIT=False

                if debug:
                    print (line, '\n', exitFeature)
                    #print >>fo, line
                    #print >>fo, exitFeature

            
                #print >>fo, 'test\n'
                #print >>fo, 'EXIT Features\n'
                #print >>fo, exitFeatures

        #if re.search('/', line): ???  Not used
        #    findEXIT=False
        #    findEXIT_XB=False
        #    findEXIT_IOR=False

    exits = []
    index = 0
    for exitFeature in exitFeatures:
        if exitFeature[4]<Zmin and exitFeature[5]<Zmin:
            continue
        if exitFeature[4]>Zmax and exitFeature[5]>Zmax:
            continue
        exit = passage()
        exit.params[0]= float(exitFeature[0])
        exit.params[1]= float(exitFeature[1])
        exit.params[2]= float(exitFeature[2])
        exit.params[3]= float(exitFeature[3])
        exit.arrow = 0   #  This need to be improved
        exit.id = index
        exit.inComp = 1
        exit.exitSign = 0
        exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5

        # In FDS input file exit is a planary surface and agents go into the surface
        # In our simulaiton exit is a rectangular area and agent reach the area
        if exit.params[0]==exit.params[2]:
            exit.params[0]=exit.params[0]-0.3
            exit.params[2]=exit.params[2]+0.3
            exitFeature[0]=exitFeature[0]-0.3
            exitFeature[2]=exitFeature[2]+0.3
            
            
        if exit.params[1]==exit.params[3]:
            exit.params[1]=exit.params[1]-0.3
            exit.params[3]=exit.params[3]+0.3
            exitFeature[1]=exitFeature[1]-0.3
            exitFeature[3]=exitFeature[3]+0.3
            
        exits.append(exit)
        index = index+1


    if outputFile:
        with open(outputFile, mode='w+') as exit_test_file:
            csv_writer = csv.writer(exit_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(['--', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
            index_temp=0
            for exitFeature in exitFeatures:
                if exitFeature[4]<Zmin and exitFeature[5]<Zmin:
                    continue
                if exitFeature[4]>Zmax and exitFeature[5]>Zmax:
                    continue                
                csv_writer.writerow(['--', str(exitFeature[0]), str(exitFeature[1]), str(exitFeature[2]), str(exitFeature[3]), '0', str(index_temp), '1', '0'])
                index_temp=index_temp+1
                
    return exits


def updateDoorData(doors, outputFile, inputFile=None):
    with open(outputFile, mode='a+') as door_test_file:
        csv_writer = csv.writer(door_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([''])
        if inputFile is not None:
            csv_writer.writerow([inputFile])
        csv_writer.writerow(['DOOR/PATH data in TestGeom: '])
        csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
        csv_writer.writerow(['&Door', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
        index_temp=0
        for door in doors:
            csv_writer.writerow(['--', str(door.params[0]), str(door.params[1]), str(door.params[2]), str(door.params[3]), str(door.arrow), str(door.id), str(door.inComp), str(door.exitSign)])
            index_temp=index_temp+1

def updateExitData(doors, outputFile, inputFile=None):
    with open(outputFile, mode='a+') as exit_test_file:
        csv_writer = csv.writer(exit_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([''])
        if inputFile is not None:
            csv_writer.writerow([inputFile])
        csv_writer.writerow(['EXIT data in TestGeom: '])
        csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
        csv_writer.writerow(['&Exit', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/exitSign'])
        index_temp=0
        for door in doors:
            csv_writer.writerow(['--', str(door.params[0]), str(door.params[1]), str(door.params[2]), str(door.params[3]), str(door.arrow), str(door.id), str(door.inComp), str(door.exitSign)])
            index_temp=index_temp+1
            

def updateWallData(walls, outputFile, inputFile=None):
    with open(outputFile, mode='a+') as wall_test_file:
        csv_writer = csv.writer(wall_test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([''])
        if inputFile is not None:
            csv_writer.writerow([inputFile])
        csv_writer.writerow(['WALL/OBST data in TestGeom: '])
        csv_writer.writerow(['time:', time.strftime('%Y-%m-%d_%H_%M_%S')])
        csv_writer.writerow(['&Wall', '0/startX', '1/startY', '2/endX', '3/endY', '4/arrow', '5/id', '6/inComp', '7/mode'])
        index_temp=0
        for wall in walls:
            csv_writer.writerow(['--', str(wall.params[0]), str(wall.params[1]), str(wall.params[2]), str(wall.params[3]), str(wall.arrow), str(wall.id), str(wall.inComp), str(wall.mode)])
            index_temp=index_temp+1
            

# Not used after the flow solver is integrated into our program
# This function was originally developed to dump exit2door data in TestGeom
def updateExit2Doors(exit2doors, fileName):
    (I, J) = np.shape(exit2doors)
    #print "The size of exit2door:", [I, J]
    #dataNP = np.zeros((I+1, J+1))

    dataNP=[]
    for i in range(I+1):
        row=[]
        if i==0:
            row.append('&Exit2Door')
            for j in range(1, J+1):
                row.append('DoorID'+str(j-1))
        else:
            row.append('ExitID'+str(i-1))
            for j in range(1, J+1):
                row.append(exit2doors[i-1, j-1])
            
        dataNP.append(row)

    #dataNP[1:, 1:] = exit2doors
    np.savetxt(fileName, dataNP, delimiter=',', fmt='%s')   #'2darray.csv'


##############################################################
# The function writeFRec is modified from Topi's work
# python script: readFRec (by Topi on Google Forum)
# readFRec: Read fortran record, return payload as bytestring
##############################################################
#
def writeFRec(infile, fmt, data):
    len1 = np.size(data)
    if len1==0 or data is None:
        #len2=infile.read(4)
        #infile.write(0x00)
        temp = struct.pack('@I', 0)
        infile.write(temp)
    
        return None
    
    #if fmt=='s':
        #result  = struct.pack('@I', data.encode())
    #    infile.write(data.encode())
    # Not try data.encode().  Use standard format to write data
        
    fmt2 = str(len1)+fmt
    num  = len1 * struct.calcsize(fmt)
    
    # length of the data
    num2   = struct.pack('@I', num)
    infile.write(num2)
    
    # Modified on 2022 Apr2: Handle string type differently from int and float type
    if fmt=='s':
        result = struct.pack(fmt, data.encode())
        infile.write(result)
    
        # End symbol
        temp = struct.pack('@I', 0)
        infile.write(temp)
        return "write a string"

    # Write data
    for i in range(len1):
        result = struct.pack(fmt, data[i])
        infile.write(result)
    
    # End symbol
    temp = struct.pack('@I', 0)
    infile.write(temp)
    

    
#Read fortran record, return payload as bytestring
def readFRec(infile,fmt):
    len1   = infile.read(4)
    if not len1:
        return None
    len1   = struct.unpack('@I', len1)[0]

    if len1==0:
        len2=infile.read(4)
        return None
    num    = int(len1/struct.calcsize(fmt))
    fmt2   = str(num)+fmt
    if num>1:
        result = struct.unpack(fmt2,infile.read(len1))
    else:
        result = struct.unpack(fmt2,infile.read(len1))[0]
    len2   = struct.unpack('@I', infile.read(4))[0]
    if fmt == 's':
        result=result[0].rstrip()
    return result


def intiPrt(fileName, debug=True):
    
    n_part=1  # Number of PARTicle classes
    [n_quant,zero_int]=[6,0]  # Number of particle features
    
    #filename=open('test.bin', 'wb+')
    writeFRec(fileName, 'I', [1])      #! Integer 1 to check Endian-ness
    writeFRec(fileName, 'I', [653])    # FDS version number
    writeFRec(fileName, 'I', [n_part]) # Number of PARTicle classes
    for npc in range(n_part):
        writeFRec(fileName, 'I', [n_quant, zero_int])
        for nq in range(n_quant):
            if nq == 0:
                writeFRec(fileName,'s', "desired Vx") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
                #q_units.append(units)  
                #q_labels.append(smv_label)
            if nq ==1:
                writeFRec(fileName,'s', "desired Vy") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
                #q_units.append(units)  
                #q_labels.append(smv_label)
            if nq ==2:
                writeFRec(fileName,'s', "actual Vx") # smv_label
                writeFRec(fileName,'s', "m/s")        # units
            if nq ==3:
                writeFRec(fileName,'s', "actual Vy") # smv_label
                writeFRec(fileName,'s', "m/s") 
            if nq ==4:
                writeFRec(fileName,'s', "motive Fx") # smv_label
                writeFRec(fileName,'s', "N")        # units
            if nq ==5:
                writeFRec(fileName,'s', "motive Fy") # smv_label
                writeFRec(fileName,'s', "N")        # units
#            if nq ==6:
#                writeFRec(fileName,'s', "group Fx") # smv_label
#                writeFRec(fileName,'s', "N")        # units
#            if nq ==7:
#                writeFRec(fileName,'s', "group Fy") # smv_label
#                writeFRec(fileName,'s', "N")        # units            
                

#################################################
# This function is used to dump evac prt5 data file
# so that the simulation result can be visualized by smokeview
#################################################
def dump_evac(agents, fileName, T, debug=True):
    
    num = len(agents)
    
    x=[]
    y=[]
    z=[]
    ap1=[]
    ap2=[]
    ap3=[]
    ap4=[]
    
    tag=[]
    # n_quant = ?  Please revise in intiPrt()
    Q_desiredVx=[]
    Q_desiredVy=[]
    Q_actualVx=[]
    Q_actualVy=[]
    Q_motiveFx=[]
    Q_motiveFy=[]
    Q_groupFx=[]
    Q_groupFy=[]
    
    for agent in agents:
        if agent.inComp == 0:
            continue
        
        x.append(agent.pos[0])
        y.append(agent.pos[1])
        z.append(1.5)

        # 180* np.arctan2(agent.actualV[1], agent.actualV[0]) /pi
        #angle = vectorAng(agent.actualV)
        ap1.append(vectorAng(agent.actualV))        # velocity direction  Agent HR angle is [0,2PI)
        ap2.append(0.1)     # diameter
        ap3.append(0.05)    #torso diameter
        ap4.append(1.0)     # height
        
        tag.append(agent.ID)

        Q_desiredVx.append(agent.desiredV[0])
        Q_desiredVy.append(agent.desiredV[1])
        Q_actualVx.append(agent.actualV[0])
        Q_actualVy.append(agent.actualV[1])
        Q_motiveFx.append(agent.motiveF[0])
        Q_motiveFy.append(agent.motiveF[1])
        Q_groupFx.append(agent.groupF[0])
        Q_groupFy.append(agent.groupF[1])
        
        #self.groupF        
        #self.selfrepF
        
    NPLIM=np.size(tag)
    # ??? what happens if tag is an empty list
    # if tag is empty, do not write agent data to the binary file
    xyz=x+y+z+ap1+ap2+ap3+ap4
    # tag=tag  tag is already OK
    Q=Q_desiredVx+Q_desiredVy+Q_actualVx+Q_actualVy +Q_motiveFx+Q_motiveFy #+Q_groupFx+Q_groupFy

    writeFRec(fileName, 'f', [T])
    writeFRec(fileName, 'I', [NPLIM])
    if NPLIM>0:
        writeFRec(fileName, 'f', xyz)
        writeFRec(fileName, 'I', tag)
        writeFRec(fileName, 'f', Q)



# Show simulation by pygame
def compute_simu(simu):

    # The file to record the output data of simulation
    FN_Temp = simu.outDataName + ".txt"
    f = open(FN_Temp, "a+")
    #simu.outFileName=f

    f.write("Start and compute simulation here.")
    # f.write('FN_FDS=', simu.FN_FDS)
    # f.write('FN_EVAC=', simu.FN_EVAC #,'\n')

    if not simu.inputDataCorrect:
        print("Input data is not correct!  Please modify input data file!")
        return

    # Initialize prt file in draw_func.py
    if simu.dumpBin:
        #fbin = open(simu.fpath + '\\' + simu.outDataName +'.bin', 'wb+')
        fbin = open(simu.outDataName +'.bin', 'wb+')
        intiPrt(fbin)

    
    ##########################################
    ### Simulation starts here: Only Compute
    ##########################################

    simu.t_sim = 0.0
    simu.tt_OtherList = 0.0
    #t_pause=0.0
    running = True
    while running and simu.t_sim < simu.t_end:
        
        # Computation Step
        simu.simulation_step2022()
        #simu.t_sim = simu.t_sim + simu.DT  # Maybe it should be in step()
        pass
        
        print('Current simulation time:', simu.t_sim, '\n')
        f.write('Current simulation time:'+str(simu.t_sim)+'\n')
        
        # Dump agent binary data file
        if simu.dumpBin and simu.t_sim > simu.tt_DumpData:
            dump_evac(simu.agents, fbin, simu.t_sim)
            simu.tt_DumpData = simu.tt_DumpData + simu.DT_DumpData
        
    f.close()
    if simu.dumpBin:
        fbin.close()
        
"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                #pygame.display.quit()
                simu.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                #button = pygame.mouse.get_pressed()            
            # elif event.type == pygame.MOUSEBUTTONUP:
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    ZOOMFACTOR = ZOOMFACTOR +1
                elif event.key == pygame.K_PAGEDOWN:
                    ZOOMFACTOR = max(6.0, ZOOMFACTOR -1)
                elif event.key == pygame.K_t:
                    simu.MODETRAJ = not simu.MODETRAJ
                elif event.key == pygame.K_SPACE:
                    simu.PAUSE = not simu.PAUSE
                elif event.key == pygame.K_v:
                    simu.SHOWVELOCITY = not simu.SHOWVELOCITY
                elif event.key == pygame.K_i:
                    simu.SHOWINDEX = not simu.SHOWINDEX
                elif event.key == pygame.K_d:
                    simu.DRAWDOORFORCE = not simu.DRAWDOORFORCE
                elif event.key == pygame.K_r:
                    simu.DRAWSELFREPULSION = not simu.DRAWSELFREPULSION
                elif event.key == pygame.K_KP1:
                    simu.SHOWWALLDATA = not simu.SHOWWALLDATA
                elif event.key == pygame.K_KP2:
                    simu.SHOWDOORDATA = not simu.SHOWDOORDATA
                elif event.key == pygame.K_KP3:
                    simu.SHOWEXITDATA = not simu.SHOWEXITDATA
                elif event.key == pygame.K_s:
                    simu.SHOWSTRESS = not simu.SHOWSTRESS
                elif event.key == pygame.K_UP:
                    ySpace=ySpace-10
                elif event.key == pygame.K_DOWN:
                    ySpace=ySpace+10
                elif event.key == pygame.K_LEFT:
                    xSpace=xSpace-10
                elif event.key == pygame.K_RIGHT:
                    xSpace=xSpace+10

        if simu.MODETRAJ == False:
            screen.fill(white)

        tt = pygame.time.get_ticks()/1000-simu.t_pause
        if simu.PAUSE is True:
            t_now = pygame.time.get_ticks()/1000
            simu.t_pause = t_now-tt
            continue

111111111111111111111111111111111111111111
        #############################
        ######### Drawing Process ######
        xyShift = np.array([xSpace, ySpace])

        ####################
        # Showing Time
        ####################
        if simu.SHOWTIME:
            tt = pygame.time.get_ticks()/1000-simu.t_pause
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Physics Time:" + str(tt), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [470,370]) #[750,350]*ZOOMFACTOR)
            time_surface=myfont.render("Simulation Time:" + str(simu.t_sim), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [630,370]) #[750,350]*ZOOMFACTOR)

        drawWalls(screen, simu.walls, ZOOMFACTOR, simu.SHOWWALLDATA, xSpace, ySpace)
        drawDoors(screen, simu.doors, ZOOMFACTOR, simu.SHOWDOORDATA, xSpace, ySpace)
        drawExits(screen, simu.exits, ZOOMFACTOR, simu.SHOWEXITDATA, xSpace, ySpace)

        # pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(), agent.size, LINEWIDTH)
        
        ####################
        # Drawing the agents
        ####################
        #for agent in agents:
        
        for idai, agent in enumerate(simu.agents):
            
            if agent.inComp == 0:
                continue
            
            #scPos = np.array([0, 0])
            scPos = [0, 0]
            scPos[0] = int(agent.pos[0]*ZOOMFACTOR+xSpace)
            scPos[1] = int(agent.pos[1]*ZOOMFACTOR+ySpace)
            
            #temp = int(100*agent.ratioV)
            #AGENTCOLOR = [0,0,temp]
            color_para = [0, 0, 0]
            color_para[0] = int(255*min(1, agent.ratioV))
            pygame.draw.circle(screen, color_para, scPos, int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            #int(agent.radius*ZOOMFACTOR), LINEWIDTH)
            
            if simu.THREECIRCLES:
                leftS = [0, 0]
                leftShoulder = agent.shoulders()[0]
                leftS[0] = int(leftShoulder[0]*ZOOMFACTOR+xSpace)
                leftS[1] = int(leftShoulder[1]*ZOOMFACTOR+ySpace)
            
                rightS = [0, 0]
                rightShoulder = agent.shoulders()[1]	
                rightS[0] = int(rightShoulder[0]*ZOOMFACTOR+xSpace)
                rightS[1] = int(rightShoulder[1]*ZOOMFACTOR+ySpace)
                
                #print ('shoulders:', leftS, rightS)
                pygame.draw.circle(screen, color_para, leftS, agent.size/2, 3)
                pygame.draw.circle(screen, color_para, rightS, agent.size/2, 3)
            
            if simu.SHOWVELOCITY:
                #endPosV = [0, 0]
                #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
                #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
                endPosV = (agent.pos+agent.actualV)*ZOOMFACTOR+xyShift
            
                #endPosDV = [0, 0]
                #endPosDV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.desiredV[0]*ZOOMFACTOR+xSpace)
                #endPosDV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.desiredV[1]*ZOOMFACTOR+ySpace)
                endPosDV = (agent.pos+agent.desiredV)*ZOOMFACTOR+xyShift
            
                #stressShow = 0
                #stressShow = int(255*agent.ratioV)
                #pygame.draw.line(screen, blue, leftS, rightS, 3)
                pygame.draw.line(screen, blue, scPos, endPosV, 2)
                pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)

            if simu.DRAWWALLFORCE:
                #endPosV = [0, 0]
                #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
                #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
                endPosWF = (agent.pos+agent.wallrepF)*ZOOMFACTOR+xyShift
            
                #pygame.draw.line(screen, blue, scPos, endPosV, 2)
                pygame.draw.line(screen, [230,220,160], scPos, endPosWF, 2)
                #khaki = 240,230,140

            if simu.DRAWDOORFORCE:
                endPosDF = (agent.pos+agent.doorF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, green, scPos, endPosDF, 2)

            if simu.DRAWGROUPFORCE:
                endPosGF = (agent.pos+agent.groupF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosGF, 2)

            if simu.DRAWSELFREPULSION:
                endPosRF = (agent.pos+agent.selfrepF)*ZOOMFACTOR+xyShift
                pygame.draw.line(screen, lightpink, scPos, endPosRF, 2)
                
            
            for idaj, agentOther in enumerate(simu.agents):
                scPosOther = [0, 0]
                scPosOther[0] = int(agentOther.pos[0]*ZOOMFACTOR+xSpace)
                scPosOther[1] = int(agentOther.pos[1]*ZOOMFACTOR+ySpace)
                
                agentPer = agent.pos+0.8*normalize(agentOther.pos - agent.pos)
                scPosDir = [0, 0]
                scPosDir[0] = int(agentPer[0]*ZOOMFACTOR+xSpace)
                scPosDir[1] = int(agentPer[1]*ZOOMFACTOR+ySpace)
                
                #leftShoulder, rightShoulder = agent.shoulders()
                #leftS = [int(leftShoulder[0]*ZOOMFACTOR), int(leftShoulder[1]*ZOOMFACTOR)]
                #rightS = [int(rightShoulder[0]*ZOOMFACTOR), int(rightShoulder[1]*ZOOMFACTOR)]
                
                if person.comm[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, blue, scPos, scPosOther, 2)
                    #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                    #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                    #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)

                if person.talk[idai, idaj] == 1 and simu.SHOWINTELINE: 
                    pygame.draw.line(screen, red, scPos, scPosOther, 3)
                    pygame.draw.line(screen, green, scPos, scPosDir, 4)
            
            #print(scPos)
            
            if simu.SHOWINDEX:
                #tt = pygame.time.get_ticks()/1000-t_pause
                myfont=pygame.font.SysFont("arial",14)
                if simu.t_sim < agent.tpre:
                    text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
                else: 
                    text_surface=myfont.render(str(idai), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift)

            if simu.SHOWSTRESS:
                myfont=pygame.font.SysFont("arial",14)
                text_surface=myfont.render(str(agent.ratioV), True, (0,0,0), (255,255,255))
                screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift+[0,6])

        pygame.display.flip()
        clock.tick(20)

    simu.ZOOMFACTOR = ZOOMFACTOR
    simu.xSpace = xSpace
    simu.ySpace = ySpace
    pygame.display.quit()
"""



if __name__ == '__main__':

    test = readCSV_base(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    print(test)
    doorFeatures = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Door')
    
    #print (doorFeatures)
    print (np.shape(doorFeatures))

    pedFeatures = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Ped')
    #print (pedFeatures)
    print (np.shape(pedFeatures))

    agents = readAgents("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    walls = readWalls("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    doors = readDoors("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    exits = readExits("/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv")
    
    print ('Length of agents:', len(agents))
    print ('Length of walls:', len(walls))
    
    ped2ExitFeatures, LowerIndex, UpperIndex = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&Ped2Exit')
    #print (ped2ExitFeatures)
    matrix = np.zeros((len(agents), len(exits)))
    
    for i in range(len(agents)):
            for j in range(len(exits)):
                matrix[i,j] = float(ped2ExitFeatures[i+1][j+1])
    print ('matrix', matrix)

    #Exit2DoorFeatures, LowerIndex, UpperIndex = getData("newDataForm.csv", '&Exit2Door')
    #print (Exit2DoorFeatures)
    #matrix = np.zeros((len(exits), len(doors)))
    #for i in range(len(exits)):
    #        for j in range(len(doors)):
    #            matrix[i,j] = float(Exit2DoorFeatures[i+1][j+1])
    #print ('matrix', matrix)
    
        #for index in range(Num_Data):
        #if dataFeatures[0,index]=='&Ped':
        #    IPedStart=index
        #    while dataFeatures[0,index]!='':
        #        index=index+1
        #    IPedEnd=index

    #agentFeatures = dataFeatures[IPedStart : IPedEnd]
    #[Num_Agents, Num_Features] = np.shape(agentFeatures)

    #doors = readDoors("doorData2019.csv", True)
    #exits = readExits("doorData2018.csv", True)
    
    # Initialize Desired Interpersonal Distance
    #DFactor_Init = readCSV("D_Data2018.csv", 'float')
    #AFactor_Init = readCSV("A_Data2018.csv", 'float')
    #BFactor_Init = readCSV("B_Data2018.csv", 'float')

    tableFeatures, LowerIndex, UpperIndex = getData(r"/mnt/sda6/gitwork2022/CrowdEgress/examples/ped2023Jan_problem.csv", '&groupB')
    BFactor_Init = readFloatArray(tableFeatures, len(agents), len(agents))
    BFactor_Init

    # Input Data Check
    #[Num_D1, Num_D2]=np.shape(DFactor_Init)
    #[Num_A1, Num_A2]=np.shape(AFactor_Init)
    #[Num_B1, Num_B2]=np.shape(BFactor_Init)

    #print >>f, np.shape(DFactor_Init), [Num_Agents, Num_Agents], '\n'

    print('\n', 'Test Output: exit2door.csv')
    exit2door=np.array([[ 1.0,  1.0,  1.0], [ 1.0,  -1.0,  -2.0], [ 1.0,  1.0,  1.0]])
    #print(exit2door)
    updateExit2Doors(exit2door, 'test_exit2door.csv')
    
    readDoorProb(r'/mnt/sda6/gitwork2022/CrowdEgress/examples/3Doors/ped2023Jan_2023-05-16_02_11_26.txt')
    
    
""" Test struct to read and write binary data
    n_part=2
    [n_quant,zero_int]=[1,0]
    f=open('test.bin', 'wb+')
    writeFRec(f, 'I', [1])      #! Integer 1 to check Endian-ness
    writeFRec(f, 'I', [653])    # FDS version number
    writeFRec(f, 'I', [n_part]) # Number of PARTicle classes
    for npc in range(n_part):
        writeFRec(f, 'I', [n_quant, zero_int])
        for nq in range(n_quant):
            smv_label =writeFRec(f,'s', "test")
            units     =writeFRec(f,'s', "Newton")
            #q_units.append(units)  
            #q_labels.append(smv_label)
    x1=[1.0, 2.0, 3.0]
    writeFRec(f, 'f', x1)
    x2=[1,2,3]
    writeFRec(f, 'I', x2)
    x3="abcdefg"
    writeFRec(f, 's', x3)
    f.close()
    
    f=open('test.bin', 'rb')
    testEnd =readFRec(f, 'I')
    ver =readFRec(f, 'I')
    n_part =readFRec(f, 'I')
    y1 = readFRec(f, 'f')
    y2 = readFRec(f, 'I')
    y3 = readFRec(f, 's') 
    print testEnd
    print ver
    print n_part
    print y1
    print y2
    print y3
    
"""
