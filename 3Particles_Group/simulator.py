# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@126.com

import pygame
import pygame.draw
import numpy as np
from agent import *
from passage import *
from math_func import *
from math import *
#from config import *
import re
import random
import csv
from readCSV import *
from ctypes import *


# Color Info as below
red=255,0,0
green=0,255,0
blue=0,0,255
white=255,255,255
yellow=255,255,0
IndianRed=205,92,92
tan = 210,180,140
skyblue = 135,206,235
orange = 255,128,0
khaki = 240,230,140
#black = 0,0,0
purple = 160, 32, 240
magenta = 255, 0, 255
lightpink =255, 174, 185
lightblud =178, 223, 238
Cyan = 0, 255, 255
LightCyan = 224, 255, 255
lightgreen = 193, 255, 193


# Below are variables for users to set up pygame features
################################################################
SCREENSIZE = [800, 400]
RESOLUTION = 180
BACKGROUNDCOLOR = [255,255,255]
LINESICKNESS = 2
AGENTSIZE = 6
AGENTSICKNESS = 3
ZOOMFACTOR = 10
DT = 0.3
#WALLSFILE = "walls.csv"
#AGENTCOLOR = [0,0,255]

xSpace=10.0
ySpace=10.0

# Below are boolean variables for users to set up the simulation
################################################################
TIMECOUNT = True
THREECIRCLES = False    # Use 3 circles to draw agents
SHOWVELOCITY = True # Show velocity and desired velocity of agents
SHOWINDEX = True        # Show index of agents
SHOWTIME = True         # Show a clock on the screen
SHOWINTELINE = True     # Draw a line between interacting agents
MODETRAJ = False        # Draw trajectory of agents' movement
COHESION = True         # Enable the cohesive social force
SELFREPULSION = True    # Enable self repulsion
WALLBLOCKHERDING = True
TPREMODE = 3        ### Instructinn: 1 -- DesiredV = 0  2 -- Motive Force =0: 
PAUSE = False
SHOWWALLDATA = True
SHOWDOORDATA = True
SHOWEXITDATA = True
TESTFORCE = False
SHOWSTRESS = False
DRAWWALLFORCE = True
DRAWDOORFORCE = False
DRAWGROUPFORCE = True


# The file to record the some output data of the simulation
f = open("out.txt", "w+")

agentFeatures = readCSV("agentData2018.csv", 'string')
[Num_Agents, Num_Features] = np.shape(agentFeatures)
print('Number of Agents:', Num_Agents, '\n', file=f)
print("Features of Agents\n", agentFeatures, "\n", file=f)

agents = []
for agentFeature in agentFeatures:
    agent = Agent()
    agent.pos = np.array([float(agentFeature[0]), float(agentFeature[1])])
    agent.dest= np.array([float(agentFeature[2]), float(agentFeature[3])])
    agent.tau = float(agentFeature[4])
    agent.tpre = float(agentFeature[5])
    agent.p = float(agentFeature[6])
    agent.pMode = agentFeature[7]
    agent.aType = agentFeature[8]
    agent.interactionRange = float(agentFeature[9])
    agent.ID = int(agentFeature[10])
    agent.moving_tau = float(agentFeature[11])
    agent.tpre_tau = float(agentFeature[12])
    agent.talk_tau = float(agentFeature[13])
    agent.talk_prob = float(agentFeature[14])
    agent.inComp = int(agentFeature[15])
    agents.append(agent)

# initialize walls
#walls = []
#for line in open(WALLSFILE):
#    coords = line.split(',')
#    wall = []
#    wall.append(float(coords[0]))
#    wall.append(float(coords[1]))
#    wall.append(float(coords[2]))
#    wall.append(float(coords[3]))
#    walls.append(wall)

# initialize OBST
obstFeatures = readCSV("obstData2018.csv", "string")
walls = []
for obstFeature in obstFeatures:
    wall = obst()
    wall.params[0]= float(obstFeature[0])
    wall.params[1]= float(obstFeature[1])
    wall.params[2]= float(obstFeature[2])
    wall.params[3]= float(obstFeature[3])
    wall.mode = obstFeature[4]
    wall.oid = int(obstFeature[5])
    wall.arrow = int(obstFeature[6])
    wall.inComp = int(obstFeature[7])
    wall.pointer1 = np.array([float(obstFeature[8]), float(obstFeature[9])])
    wall.pointer2 = np.array([float(obstFeature[10]), float(obstFeature[11])])
    walls.append(wall)

#walls = [[3.33, 3.33, 23.97, 3.33], 
#[3.33, 3.33, 3.33, 30.31], 
#[3.33, 30.31, 23.97, 30.31]] 
#[23.31, 3.33, 33.31, 10.02], 
#[33.31, 16.92, 23.31, 23.31]]

#walls = [[3.33, 3.33, 29.97, 3.33], 
#[3.33, 3.33, 3.33, 33.31], 
#[3.33, 33.31, 29.97, 33.31],
#[23.31, 3.33, 33.31, 14.02], 
#[33.31, 20.92, 23.31, 33.31]]

doorFeatures = readCSV("doorData2018.csv", "string")
doors = []
for doorFeature in doorFeatures:
    door = passage()
    door.params[0]= float(doorFeature[0])
    door.params[1]= float(doorFeature[1])
    door.params[2]= float(doorFeature[2])
    door.params[3]= float(doorFeature[3])
    door.arrow = int(doorFeature[4])
    door.id = int(doorFeature[5])
    door.inComp = int(doorFeature[6])
    door.exitSign = int(doorFeature[7])
    door.pos = (np.array([door.params[0], door.params[1]]) + np.array([door.params[2], door.params[3]]))*0.5
    doors.append(door)

agent2doors = readCSV("Agent2Door2018.csv", "float")

[Num_Doors, Num_DoorFeatures] = np.shape(doorFeatures)
if np.shape(agent2doors)[0]!= Num_Agents or np.shape(agent2doors)[1]!= Num_Doors:
    print('\nError on input data: doors or agent2doors \n')
    print('\nError on input data: doors or agent2doors \n', file=f)

#print 'num_agents-----+++++++!!!!!!!!', np.shape(agent2doors)[0]
#print 'num_doors------++++++!!!!!!!!!', np.shape(agent2doors)[1]
#print '\n'

exitFeatures = readCSV("exitData2018.csv", "string")
exits = []
for exitFeature in exitFeatures:
    exit = outlet()
    exit.params[0]= float(exitFeature[0])
    exit.params[1]= float(exitFeature[1])
    exit.params[2]= float(exitFeature[2])
    exit.params[3]= float(exitFeature[3])
    exit.arrow = int(exitFeature[4])
    exit.id = int(exitFeature[5])
    exit.inComp = int(exitFeature[6])
    exit.exitSign = int(exitFeature[7])
    exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
    exits.append(exit)


# Initialize Desired Interpersonal Distance
DFactor_Init = readCSV("D_Data2018.csv", 'float')
AFactor_Init = readCSV("A_Data2018.csv", 'float')
BFactor_Init = readCSV("B_Data2018.csv", 'float')

#print walls
#print DFactor_Init
#print AFactor_Init
#print BFactor_Init

print("Wall Matrix\n", walls, "\n", file=f)
print("D Matrix\n", DFactor_Init, "\n", file=f)
print("A Matrix\n", AFactor_Init, "\n", file=f)
print("B Matrix\n", BFactor_Init, "\n", file=f)

#DFactor_Init = np.array(
#[[0.0, 0.3, 0.9, 1.3, 1.6, 1.0], 
#[0.3, 0.0, 0.3, 1.6, 1.0, 1.2], 
#[0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
#[1.3, 0.6, 1.3, 0.0, 1.7, 1.1],
#[1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
#[1.0, 1.2, 0.3, 2.1, 1.8, 0.0]])

#AFactor_Init = np.array(
#[[0.0, 0.3, 0.9, 1.3, 1.6, 1.0], 
#[0.3, 0.0, 0.3, 1.6, 1.0, 1.2], 
#[0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
#[1.3, 1.6, 1.3, 0.0, 1.7, 1.1],
#[1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
#[1.0, 1.2, 1.2, 2.1, 1.8, 0.0]])

#BFactor_Init = np.array(
#[[0.0, 0.3, 0.9, 2.3, 2.6, 1.0], 
#[1.3, 0.0, 3.3, 1.6, 3.0, 1.2], 
#[0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
#[1.3, 18.6, 1.3, 0.0, 1.7, 1.1],
#[1.6, 1.0, 1.3, 12.7, 0.0, 1.8],
#[1.0, 1.2, 18.8, 2.1, 1.8, 0.0]])

# Input Data Check
#[Num_D1, Num_D2]=np.shape(DFactor_Init)
#[Num_A1, Num_A2]=np.shape(AFactor_Init)
#[Num_B1, Num_B2]=np.shape(BFactor_Init)

#print >>f, np.shape(DFactor_Init), [Num_Agents, Num_Agents], '\n'

if np.shape(DFactor_Init)!= (Num_Agents, Num_Agents):
    print('\nError on input data: DFactor_Init\n')
    print('\nError on input data: DFactor_Init\n', file=f)
    
if np.shape(AFactor_Init)!= (Num_Agents, Num_Agents): 
    print('\nError on input data: AFactor_Init\n')
    print('\nError on input data: AFactor_Init\n', file=f)

if np.shape(BFactor_Init)!= (Num_Agents, Num_Agents): 
    print('\nError on input data: BFactor_Init\n')
    print('\nError on input data: BFactor_Init\n', file=f)
    
DFactor = DFactor_Init
AFactor = AFactor_Init
BFactor = BFactor_Init

comm = np.zeros((Num_Agents, Num_Agents))
talk = np.zeros((Num_Agents, Num_Agents))

#Users may easily change some attributes of agents before the simulation
#########################################

#agents[1].pos = np.array([60, 8])
#agents[1].dest = np.array([20.0,10.0])        
#agents[1].direction = normalize(agents[1].dest - agents[1].pos)
agents[1].desiredSpeed = 1.8
#agents[1].desiredV = agents[1].desiredSpeed*agents[1].direction
agents[1].p = 0.2
agents[1].dest = doors[1].pos

#agents[2].pos = np.array([60, 12])    
#agents[2].direction = normalize(agents[2].dest - agents[2].pos)
agents[2].desiredSpeed = 1.8 
#agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
#agents[2].B = 3.6
agents[2].p = 0.6 #0.1
agents[2].pMode = 'fixed'
agents[2].interactionRange = 6.0
agents[2].dest = doors[1].pos

#agents[0].changeAttr(32, 22, 0, 0)
agents[0].pMode = 'fixed'

# Assign destinations of agents
agents[0].dest = exits[1].pos
agents[1].dest = exits[1].pos
agents[2].dest = exits[1].pos
agents[3].dest = exits[0].pos
agents[4].dest = exits[0].pos
agents[5].dest = exits[2].pos
agents[6].dest = exits[2].pos

##########################################
### Simulation starts here with Pygame
##########################################

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Modified Social Force Model')
clock = pygame.time.Clock()
#screen.fill(BACKGROUNDCOLOR)

#myfont=pygame.font.SysFont("arial",16)
#text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
#screen.blit(text_surface, (16,20))

t_pause=0.0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
        # elif event.type == pygame.MOUSEBUTTONUP:
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                ZOOMFACTOR = ZOOMFACTOR +1
            elif event.key == pygame.K_PAGEDOWN:
                ZOOMFACTOR = max(0, ZOOMFACTOR -1)
            elif event.key == pygame.K_t:
                MODETRAJ = not MODETRAJ
            elif event.key == pygame.K_SPACE:
                PAUSE = not PAUSE
            elif event.key == pygame.K_v:
                SHOWVELOCITY = not SHOWVELOCITY
            elif event.key == pygame.K_i:
                SHOWINDEX = not SHOWINDEX
            elif event.key == pygame.K_KP1:
                SHOWWALLDATA = not SHOWWALLDATA
            elif event.key == pygame.K_KP2:
                SHOWDOORDATA = not SHOWDOORDATA
            elif event.key == pygame.K_KP3:
                SHOWEXITDATA = not SHOWEXITDATA
            elif event.key == pygame.K_UP:
                ySpace=ySpace-10
            elif event.key == pygame.K_DOWN:
                ySpace=ySpace+10
            elif event.key == pygame.K_LEFT:
                xSpace=xSpace-10
            elif event.key == pygame.K_RIGHT:
                xSpace=xSpace+10

    if MODETRAJ == False:
        screen.fill(BACKGROUNDCOLOR)

    if PAUSE is True:
        t_now = pygame.time.get_ticks()/1000
        t_pause = t_now-tt
        continue

    # Compute the agents one by one in loop
    for idai,ai in enumerate(agents):
        
        # Whether ai is in computation
        if ai.inComp == 0:
            continue
    
    #Pre-evacuation Time Effect
        tt = pygame.time.get_ticks()/1000 - t_pause
        if (tt < ai.tpre):
            ai.desiredSpeed = random.uniform(0.3,1.6)
        else: 
            ai.desiredSpeed = random.uniform(2.0,3.0)
    
        #ai.dest = ai.memory.peek()
    
        ai.direction = normalize(ai.dest - ai.pos)
        ai.desiredV = ai.desiredSpeed*ai.direction
        #ai.desiredV = 0.7*ai.desiredV + 0.3*ai.desiredV_old
        peopleInter = 0.0
        wallInter = np.array([0.0, 0.0])
        doorInter = np.array([0.0, 0.0])
        otherDir = np.array([0.0, 0.0])
        otherSpeed = 0.0
        #otherMovingNum = 0
    
        ai.actualSpeed = np.linalg.norm(ai.actualV)
        ai.desiredSpeed = np.linalg.norm(ai.desiredV)
    
        #print >> f, "desired speed of agent i:", ai.desiredSpeed, "/n"
        #print >> f, "actual speed of agent i:", ai.actualSpeed, "/n"
    
        if ai.desiredSpeed != 0: 
            ai.ratioV = ai.actualSpeed/ai.desiredSpeed
        else: 
            ai.ratioV = 1
    
        ######################
        # Wall force adjusted
        # Stress indicator is used (Or known as ratioV)
        ai.stressLevel = 1 - ai.ratioV
        ai.test = 0.0 #??
        #ai.diw_desired = max(0.2, ai.ratioV)*0.6
        #ai.A_WF = 700*max(0.3, ai.ratioV)
        #ai.B_WF = 1.6*max(min(0.6, ai.ratioV),0.2)
    
        ai.diw_desired = max(0.5, ai.ratioV)*0.6
        #ai.A_WF = 30*max(0.5, ai.ratioV)
        ai.B_WF = 2.2*max(min(0.5, ai.ratioV),0.2) 
    
    
        ######################
        # Herding indicator adjusted
        # There are two method:
        # 1. White Noise Method
        # 2. Stress Level Method (Or known as ratioV: Helbing's Equation)
        #if ai.p == 0.0:
        if ai.pMode == 'random':
            ai.p = random.uniform(-0.3, 0.6)  # Method-1
            #ai.p = random.uniform(-0.3, 0.6*ai.stressLevel)
            #ai.p = 1 - ai.ratioV   # Method-2
        elif ai.pMode =='increase':
            pass
        elif ai.pMode =='decrease':
            pass
        
        ai.others=[]
        
        #############################################
        # Compute interaction of agents
        # Group force and herding effect
        # Find the agents who draw ai's attention

        for idaj,aj in enumerate(agents):
            
            if aj.inComp == 0:
                comm[idai, idaj] = 0
                talk[idai, idaj] = 0
                continue
        
            rij = ai.radius + aj.radius
            dij = np.linalg.norm(ai.pos - aj.pos)
         
            #Difference of current destinations
            dij_dest = np.linalg.norm(ai.dest - aj.dest)
         
            #Difference of desired velocities
            vij_desiredV = np.linalg.norm(ai.desiredV - aj.desiredV)
         
            #Difference of actual velocities
            vij_actualV = np.linalg.norm(ai.actualV - aj.actualV)
         
            phiij = vectorAngleCos(ai.actualV , (aj.pos - ai.pos))
            anisoF = ai.lamb + (1-ai.lamb)*(1+cos(phiij))*0.5
         
            #print >> f, "anisotropic factor", anisoF, "/n"
         
            if idai == idaj:
                continue
            
            #####################################################
            # Check whether there is a wall between agent i and j
            no_wall_ij = True
            if WALLBLOCKHERDING: 
                for idwall, wall in enumerate(walls):
                    if wall.inComp ==0:
                        continue
                    #result, flag = ai.iswallInBetween(aj, wall)
                    result, flag = wall.wallInBetween(ai.pos, aj.pos)
                    if result != None:
                        no_wall_ij = False
                        
                        
            see_i2j = True
            if np.dot(ai.actualV, aj.pos-ai.pos)<0.2:
                see_i2j = False
            if np.linalg.norm(ai.actualV)<0.2:
                temp=random.uniform(-180, 180)
                if temp < 70 and temp > -70:
                    see_i2j =True
         
            #############################################
            # Turn on or off group social force
            # Also known as cohesive social force
            #if COHESION and no_wall_ij and see_i2j:
            #    peopleInter += ai.cohesiveForce(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])*anisoF
                
         
            #############################################
            # Traditional Social Force and Physical Force
            if no_wall_ij: #and see_i2j:
                peopleInter += ai.agentForce(aj)*anisoF
         
                     
            talk[idai, idaj] = 0
            ###################################################
            # Interactive Opinion Dynamics Starts here
            # Including Herding Effect, Group Effect and Talking Behavior
            # There are several persons around you.  Which draws your attention?  
            ###################################################
            if dij < ai.B_CF*BFactor[idai, idaj] + rij*DFactor[idai, idaj] and no_wall_ij and see_i2j:
            #if dij < ai.interactionRange and no_wall_ij and see_i2j:
                comm[idai, idaj] = 1
                ai.others.append(aj)
        
                #DFactor[idai, idaj] = (1-ai.p)*DFactor[idai, idaj]+ai.p*DFactor[idaj, idai]
                #AFactor[idai, idaj] = (1-ai.p)*AFactor[idai, idaj]+ai.p*AFactor[idaj, idai]
                #BFactor[idai, idaj] = (1-ai.p)*BFactor[idai, idaj]+ai.p*BFactor[idaj, idai]
                #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*aj.desiredV      
            else: 
                comm[idai, idaj] = 0

            # Loop of idaj,aj ends here
            ###########################
        
        print('=== ai id ===::', idai)
        print('ai.others len:', len(ai.others))
        
        if len(ai.others)!=0: #and tt>ai.tpre:
            otherDir, otherSpeed = ai.opinionDynamics()
            ai.direction = (1-ai.p)*ai.direction + ai.p*otherDir
            ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + ai.p*otherSpeed
            ai.desiredV = ai.desiredSpeed*ai.direction
            
        
        for aj in ai.others:

            idaj=aj.ID
            print('others ID', idaj)
            #############################################
            # Turn on or off group social force
            # Also known as cohesive social force
                    
            dij = np.linalg.norm(ai.pos - aj.pos)
         
            #Difference of current destinations
            dij_dest = np.linalg.norm(ai.dest - aj.dest)
         
            #Difference of desired velocities
            vij_desiredV = np.linalg.norm(ai.desiredV - aj.desiredV)
         
            #Difference of actual velocities
            vij_actualV = np.linalg.norm(ai.actualV - aj.actualV)
            
            if dij<ai.interactionRange: #and 0.6<random.uniform(0.0,1.0):
            #ai.talk_prob<random.uniform(0.0,1.0):
                DFactor[idai, idaj]=3.0
                AFactor[idai, idaj]=60
                BFactor[idai, idaj]=30
                ai.tau = ai.talk_tau
                talk[idai, idaj]=1
            else:
                DFactor[idai, idaj]=DFactor_Init[idai, idaj]
                AFactor[idai, idaj]=AFactor_Init[idai, idaj]
                BFactor[idai, idaj]=BFactor_Init[idai, idaj]
                ai.tau = ai.moving_tau
                talk[idai, idaj]=0

            if COHESION:
                peopleInter += ai.cohesiveForce(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])*anisoF

            #if tt > aj.tpre: 
            #    ai.tpre = (1-ai.p)*ai.tpre + ai.p*aj.tpre
            if dij < ai.interactionRange:
                ai.tpre = 0.5*ai.tpre + 0.5*aj.tpre

        #ai.others=list(set(ai.others))
        #################################
        # Herding Effect Computed
        #if otherMovingNum != 0:
            #ai.direction = (1-ai.p)*ai.direction + ai.p*otherMovingDir
            #ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + #ai.p*otherMovingSpeed/otherMovingNum
            #ai.desiredV = ai.desiredSpeed*ai.direction

            #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*otherMovingDir


        ########################################################
        # Turn on or off self-repulsion by boolean variable SELFREPULSION
        # Also known as sub-consciousness effect in crowd dynamics
        ########################################################
        if SELFREPULSION and (len(ai.others) != 0):
            selfRepulsion = ai.selfRepulsion(DFactor[idai, idai], AFactor[idai, idai], BFactor[idai, idai])#*ai.direction
            #peopleInter += selfRepulsion
        else: 
            selfRepulsion = 0.0


        outsideDoor = True
        for door in doors:
            if door.inComp ==0:
                continue
            #doorInter += ai.doorForce(door)
            if door.insideDoor(ai.pos):
                wallInter = np.array([0.0, 0.0])
                outsideDoor = False
                #doorInter = ai.doorForce(door)
                #break

        #########################
        # Calculate Wall Repulsion
        if outsideDoor:
            for wall in walls:
                if wall.inComp ==0:
                    continue
                wallInter += ai.wallForce(wall)
                #wallInter += wall.wallForce(ai)

        #print('Forces from Walls:', wallInter)
        #print('Forces from people:', peopleInter)
    
        #############################################
        # Calculate Motive Forces
        # Consider TPRE features
        #############################################   
        #tt = pygame.time.get_ticks()/1000-t_pause
        if (tt < ai.tpre and TPREMODE == 1):
            ai.desiredV = ai.direction*0.0
            ai.desiredSpeed = 0.0
            #ai.dest = ai.pos
            ai.tau = random.uniform(2.0,10.0) #ai.tpre_tau
            motiveForce = ai.adaptVel()
    
        #ai.sumAdapt += motiveForce*0.2  #PID: Integration Test Here
        
        #tt = pygame.time.get_ticks()/1000-t_pause
        if (tt < ai.tpre and TPREMODE == 2):
            motiveForce = np.array([0.0, 0.0])

        if (tt < ai.tpre and TPREMODE == 3):
            pass
            if outsideDoor:
                doorInter = np.array([0.0, 0.0])
                
            goSomeone = ai.moveToAgent()
            if goSomeone != None:
                gsid = goSomeone.ID
                ai.diretion = normalize(goSomeone.pos - ai.pos)
                ai.desiredSpeed = random.uniform(0.6,1.6)
                ai.desiredV = ai.diretion*ai.desiredSpeed
                ai.tau = random.uniform(0.6,1.6) #ai.tpre_tau
                motiveForce = ai.adaptVel()
                print ('&&& In Tpre Stage:')
                print(('goSomeone:', goSomeone.ID))
            else:
                ai.desiredV = ai.direction*0.0
                ai.desiredSpeed = 0.0
                ai.tau = random.uniform(2.0,10.0) #ai.tpre_tau
                motiveForce = ai.adaptVel()
                print('&&& In Tpre Stage:')
                print('goSomeone is None.')
    

        #temp = 0.0
        #maxWallForce = 0.0
        #wallDirection = np.array([0.0, 0.0])
    
        #for idwall, wall in enumerate(walls):
        #temp = np.linalg.norm(ai.wallForce(wall))
        #    if temp > maxWallForce: 
        #   maxWallForce = temp
        #   wallDirection = np.array([wall[0],wall[1]]) - np.array([wall[2],wall[3]])
        #   closeWall = wall
    
        if (tt >= ai.tpre):
        #################################
        # Wall Effect Computed: 
        # Is There Any Wall Nearby On The Route?
        # If So, Adjust Desired Direction

            #####################################################
            # Check whether there is a wall between agent i and the destination
            no_wall_dest = True
            for idwall, wall in enumerate(walls):
                if wall.inComp ==0:
                    continue
                result, flag = wall.wallInBetween(ai.pos, ai.dest)
                if result != None:
                    no_wall_dest = False
                    break

            ai.targetDoors=[]
            # Start to search possible doors
            if not no_wall_dest:
                for iddoor, door in enumerate(doors):
                    if door.inComp ==0:
                        continue
                    if door.insideDoor(ai.pos):
                        ai.targetDoors.append(door)
                        continue
                    edge1, edge2 = door.doorEdge()
                    isVisableDoor=True
                    for wall in walls:
                        if wall.inComp ==0:
                            continue
                        result1, flag1 = wall.wallInBetween(ai.pos, edge1)
                        result2, flag2 = wall.wallInBetween(ai.pos, edge2)
                        result3, flag3 = wall.wallInBetween(ai.pos, door.pos)
                        if flag1 and flag2 and flag3:
                            isVisableDoor=False
                            break
                    if isVisableDoor:
                        ai.targetDoors.append(door)

            print('ai:', ai.ID, 'Length of targetDoors:', len(ai.targetDoors))

            goDoor = ai.selectDoor()
            #goDoor.computePos()
            if goDoor==None:
                print('goDoor is None.')
                doorInter = np.array([0.0, 0.0])
            else:
                print('go Door:', goDoor.id, goDoor.pos)
                doorInter = ai.doorForce(goDoor, 'edge', 0.3)
                
            #dir1=goDoor.direction()
            #dir2=goDoor.pos-ai.pos
            if goDoor!=None: #and np.dot(dir1, dir2)>=0:
                if not goDoor.insideDoor(ai.pos):
                    ai.direction = normalize(goDoor.pos-ai.pos)
                    ai.desiredV = ai.desiredSpeed*ai.direction
                else:
                    ai.direction = goDoor.direction()
                    ai.desiredV = ai.desiredSpeed*ai.direction

            # Interaction with enviroment
            # Search for wall on the route
            # temp = 0.0
            closeWall = walls[0] #None #walls[0]
            closeWallDist = 30.0 # Define how close the wall is
            for wall in walls:
                if wall.inComp ==0:
                    continue
                crossp, diw, arrow = ai.wallOnRoute(wall, 1.0)
                if diw!=None and diw < closeWallDist:
                    closeWallDist = diw
                    closeWall = wall
            
            crossp, diw, wallDirection = ai.wallOnRoute(closeWall, 1.0)
            if diw!=None and goDoor!=None and outsideDoor:
                if goDoor.insideDoor(crossp):
                    wallInter = wallInter - ai.wallForce(closeWall)

            if diw!=None and goDoor==None: # and not ai.targetDoors:
            #if closeWall!=None:
            #    diw = ai.wallOnRoute(closeWall)
                #wallDirection = np.array([closeWall.params[0],closeWall.params[1]]) - np.array([closeWall.params[2],closeWall.params[3]])
                #wallDirection = -normalize(wallDirection)
                #if wall.arrow==0 or ai.aType=='search': 
                if np.dot(wallDirection, ai.actualV) < 0.0 and wall.arrow==0:
                    #0.3*ai.desiredV+0.7*ai.desiredV_old) < 0.0:
                    wallDirection = -wallDirection

                #if (isnan(closeWall.pointer1[0]) or isnan(closeWall.pointer1[1])) and (isnan(closeWall.pointer2[0]) or isnan(closeWall.pointer2[1])) or ai.aType=='search': 
                if isnan(closeWall.pointer1[0]) or isnan(closeWall.pointer1[1]) or ai.aType=='search':
                    pass
                    if diw==None:
                        print('diw==None')
                        print('ai:', idai)
                        print('closeWall:', closeWall.oid)
                        print('################################')
            
                    ai.direction = ai.direction + wallDirection*20/diw
                    ai.direction = normalize(ai.direction)
                    ai.desiredV = ai.desiredSpeed*ai.direction
                    #ai.destmemory.append([wall[2],wall[3]]+0.1*wallDirection)
                #elif ai.destmemory[-1] is not [closeWall[5], closeWall[6]]:  
                    #ai.destmemory[-1][0]!=closeWall[5] or ai.destmemory[-1][1]!= closeWall[6]:
                    #ai.destmemory.append([wall[0],wall[1]]+0.1*wallDirection)
                    #ai.destmemory.append([closeWall[5], closeWall[6]])
                    #ai.direction = normalize(ai.destmemory[-1]-ai.pos)
                    #ai.desiredV = ai.desiredSpeed*ai.direction
                else:
                    temp1= np.linalg.norm([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                    temp2= np.linalg.norm([closeWall.pointer2[0], closeWall.pointer2[1]]-ai.pos)
                    for aj in ai.others:
                        temp1 = temp1+np.linalg.norm([closeWall.pointer1[0], closeWall.pointer1[1]]-aj.pos)
                        temp2 = temp2+np.linalg.norm([closeWall.pointer2[0], closeWall.pointer2[1]]-aj.pos)
                    if temp1<temp2:
                        ai.direction = normalize([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                    else:
                        ai.direction = normalize([closeWall.pointer2[0], closeWall.pointer2[1]]-ai.pos)
                    #ai.direction = normalize([closeWall.pointer1[0], closeWall.pointer1[1]]-ai.pos)
                    ai.desiredV = ai.desiredSpeed*ai.direction
            
                #ai.direction = ai.direction + wallDirection/np.linalg.norm(wallDirection)*20/diw
                #ai.desiredV = ai.desiredSpeed*ai.direction
        
            #if np.linalg.norm(ai.pos-ai.destmemory[-1])<=1e-3:
            #    ai.destmemory.pop()
            ai.tau=ai.moving_tau
            motiveForce = ai.adaptVel() 
            
            #print 'destmemeory', len(ai.destmemory)

        # Compute total force
        sumForce = motiveForce + peopleInter + wallInter + doorInter + ai.diss*ai.actualV + selfRepulsion #+ ai.sumAdapt

        # Compute acceleration
        accl = sumForce/ai.mass
        
        # Compute velocity
        ai.actualV = ai.actualV + accl*DT # consider dt = 0.5

        ai.wallrepF = wallInter
        ai.doorF = doorInter
        ai.groupF = peopleInter
        ai.selfrepF = selfRepulsion

        if TESTFORCE:
            print('@motiveForce:', np.linalg.norm(motiveForce), motiveForce)
            print('@peopleInter:', np.linalg.norm(peopleInter), peopleInter)
            print('@wallInter:', np.linalg.norm(wallInter), wallInter)
            print('@doorInter:', np.linalg.norm(doorInter), doorInter)
            print('@diss:', np.linalg.norm(ai.diss*ai.actualV), ai.diss*ai.actualV)
            print('@selfRepulsion:', np.linalg.norm(selfRepulsion), selfRepulsion)
        
        ###########################################
        # Solution to Overspeed: Agents will not move too fast
        ai.actualSpeed = np.linalg.norm(ai.actualV)
        if (ai.actualSpeed >= ai.maxSpeed):
            ai.actualV = ai.actualV*ai.maxSpeed/ai.actualSpeed
            #ai.actualV[0] = ai.actualV[0]*ai.maxSpeed/ai.actualSpeed
            #ai.actualV[1] = ai.actualV[1]*ai.maxSpeed/ai.actualSpeed
    
    
        # Calculate Positions
        ai.pos = ai.pos + ai.actualV*DT
        #print(ai.pos)
        #print(accl,ai.actualV,ai.pos)
    
        ai.desiredV_old = ai.desiredV
        ai.actualV_old = ai.actualV
    
        ###########################################
        ## Output time when agents reach the safety
        #if TIMECOUNT and (ai.pos[0] >= 35.0) and (ai.Goal == 0):
        if TIMECOUNT and (np.linalg.norm(ai.pos-ai.dest)<=0.2) and (ai.Goal == 0):
            print('test')
            ai.inComp = 0
            ai.Goal = 1
            ai.timeOut = pygame.time.get_ticks()
            #ai.timeOut = clock.get_time()/1000.0
            print('Time to Reach the Goal:', ai.timeOut)
            print('Time to Reach the Goal:', ai.timeOut, file=f)
        
        ###########################################
        ## Remove agent when agent reaches the destination    
        #if np.linalg.norm(ai.pos-ai.dest)<=1e-3:
         #   agents.remove(agents[idai])


    ##############################################################
    ######### Drawing Process ######
    xyShift = np.array([xSpace, ySpace])

    ####################
    # Showing Time
    ####################
    if SHOWTIME:
        tt = pygame.time.get_ticks()/1000-t_pause
        myfont=pygame.font.SysFont("arial",14)
        time_surface=myfont.render("Time:" + str(tt), True, (0,0,0), (255,255,255))
        screen.blit(time_surface, [730,370]) #[750,350]*ZOOMFACTOR)

    ####################
    # Drawing the walls
    ####################
    for wall in walls:
        
        if wall.inComp == 0:
            continue
        
        if wall.mode=='line':
            startPos = np.array([wall.params[0],wall.params[1]]) #+xyShift
            endPos = np.array([wall.params[2],wall.params[3]]) #+xyShift
            startPx = startPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            endPx = endPos*ZOOMFACTOR #+np.array([xSpace, ySpace])
            pygame.draw.line(screen, red, startPx+xyShift, endPx+xyShift, LINESICKNESS)
            
            if isnan(wall.pointer1[0]) or isnan(wall.pointer1[1]):
                pass
            else:
                guidePos = np.array([wall.pointer1[0], wall.pointer1[1]])
                #guidePx = [int(guidePos[0])*ZOOMFACTOR, int(guidePos[1])*ZOOMFACTOR]
                guidePx = [int(guidePos[0]*ZOOMFACTOR+xSpace), int(guidePos[1]*ZOOMFACTOR+ySpace)]
                #guidePx[0] = int(guidePos[0])*ZOOMFACTOR
                #guidePx[1] = int(guidePos[1])*ZOOMFACTOR
                pygame.draw.circle(screen, red, guidePx, 6, LINESICKNESS)
                #pygame.draw.circle(screen, red, guidePx+xyShift, 6, LINESICKNESS)
                            
            if isnan(wall.pointer2[0]) or isnan(wall.pointer2[1]):
                pass
            else:
                guidePos = np.array([wall.pointer2[0], wall.pointer2[1]])
                #guidePx = [int(guidePos[0])*ZOOMFACTOR, int(guidePos[1])*ZOOMFACTOR]
                guidePx = [int(guidePos[0]*ZOOMFACTOR+xSpace), int(guidePos[1]*ZOOMFACTOR+ySpace)]
                #guidePx[0] = int(guidePos[0])*ZOOMFACTOR
                #guidePx[1] = int(guidePos[1])*ZOOMFACTOR
                pygame.draw.circle(screen, red, guidePx, 6, LINESICKNESS)
                #pygame.draw.circle(screen, red, guidePx+xyShift, 6, LINESICKNESS)

            if SHOWWALLDATA:
                myfont=pygame.font.SysFont("arial",14)
                text_surface=myfont.render(str(startPos), True, (255,0,0), (255,255,255))
                screen.blit(text_surface, startPos*ZOOMFACTOR +xyShift)
                text_surface=myfont.render(str(endPos), True, (255,0,0), (255,255,255))
                screen.blit(text_surface, endPos*ZOOMFACTOR +xyShift)

        elif wall.mode=='rect':
            x= ZOOMFACTOR*wall.params[0]
            y= ZOOMFACTOR*wall.params[1]
            w= ZOOMFACTOR*(wall.params[2] - wall.params[0])
            h= ZOOMFACTOR*(wall.params[3] - wall.params[1])
            
            pygame.draw.rect(screen, red, [x+xSpace, y+ySpace, w, h], LINESICKNESS)

            if SHOWWALLDATA:
                pass
                startPos = np.array([wall.params[0],wall.params[1]])
                endPos = np.array([wall.params[2],wall.params[3]])

                myfont=pygame.font.SysFont("arial",10)

                #text_surface=myfont.render(str(startPos), True, red, (255,255,255))
                #screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

                #text_surface=myfont.render(str(endPos), True, red, (255,255,255))
                #screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)
    
    
    ####################
    # Drawing the doors
    ####################
    
    for door in doors:

        if door.inComp == 0:
            continue
        
        #startPos = np.array([door[0], door[1]])
        #endPos = np.array([door[2], door[3]])

        startPos = np.array([door.params[0],door.params[1]]) #+xyShift
        endPos = np.array([door.params[2],door.params[3]]) #+xyShift

        #Px = [0, 0]
        #Px[0] = int(Pos[0]*ZOOMFACTOR)
        #Px[1] = int(Pos[1]*ZOOMFACTOR)
        #pygame.draw.circle(screen, red, Px, LINESICKNESS)

        x= ZOOMFACTOR*door.params[0] 
        y= ZOOMFACTOR*door.params[1] 
        w= ZOOMFACTOR*(door.params[2] - door.params[0])
        h= ZOOMFACTOR*(door.params[3] - door.params[1])
            
        pygame.draw.rect(screen, green, [x+ xSpace, y+ ySpace, w, h], LINESICKNESS)

        if SHOWDOORDATA:
            
            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR+xyShift)

            text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            screen.blit(text_surface, endPos*ZOOMFACTOR+xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render(str(door.arrow), True, blue, (255,255,255))
            screen.blit(text_surface, door.pos*ZOOMFACTOR+xyShift)

    ####################
    # Drawing the exits
    ####################
    
    for exit in exits:

        if exit.inComp == 0:
            continue

        startPos = np.array([exit.params[0],exit.params[1]]) #+xyShift
        endPos = np.array([exit.params[2],exit.params[3]]) #+xyShift

        #Px = [0, 0]
        #Px[0] = int(Pos[0]*ZOOMFACTOR)
        #Px[1] = int(Pos[1]*ZOOMFACTOR)
        #pygame.draw.circle(screen, red, Px, LINESICKNESS)

        x= ZOOMFACTOR*exit.params[0]
        y= ZOOMFACTOR*exit.params[1]
        w= ZOOMFACTOR*(exit.params[2] - exit.params[0])
        h= ZOOMFACTOR*(exit.params[3] - exit.params[1])
            
        pygame.draw.rect(screen, orange, [x+ xSpace, y+ ySpace, w, h], LINESICKNESS)

        if SHOWEXITDATA:

            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR + xyShift)

            text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            screen.blit(text_surface, endPos*ZOOMFACTOR + xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render(str(exit.arrow), True, blue, (255,255,255))
            screen.blit(text_surface, exit.pos*ZOOMFACTOR + xyShift)

    #   pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(), AGENTSIZE, AGENTSICKNESS)
    
    ####################
    # Drawing the agents
    ####################
    #for agent in agents:
    
    for idai, agent in enumerate(agents):
        
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
        pygame.draw.circle(screen, color_para, scPos, AGENTSIZE, AGENTSICKNESS)
    #int(ai.radius*ZOOMFACTOR), AGENTSICKNESS)
        
        if THREECIRCLES:
            leftS = [0, 0]
            leftShoulder = agent.shoulders()[0]
            leftS[0] = int(leftShoulder[0]*ZOOMFACTOR+xSpace)
            leftS[1] = int(leftShoulder[1]*ZOOMFACTOR+ySpace)
        
            rightS = [0, 0]
            rightShoulder = agent.shoulders()[1]    
            rightS[0] = int(rightShoulder[0]*ZOOMFACTOR+xSpace)
            rightS[1] = int(rightShoulder[1]*ZOOMFACTOR+ySpace)
            
            #print 'shoulders:', leftS, rightS
            pygame.draw.circle(screen, color_para, leftS, AGENTSIZE/2, 3)
            pygame.draw.circle(screen, color_para, rightS, AGENTSIZE/2, 3)
        
        if SHOWVELOCITY:
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

        if DRAWWALLFORCE:
            #endPosV = [0, 0]
            #endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR+xSpace)
            #endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR+ySpace)
            endPosWF = (agent.pos+agent.wallrepF)*ZOOMFACTOR+xyShift
        
            #pygame.draw.line(screen, blue, scPos, endPosV, 2)
            pygame.draw.line(screen, [230,220,160], scPos, endPosWF, 2)
            #khaki = 240,230,140

        if DRAWDOORFORCE:
            endPosDF = (agent.pos+agent.doorF)*ZOOMFACTOR+xyShift
            pygame.draw.line(screen, green, scPos, endPosDF, 2)

        if DRAWGROUPFORCE:
            endPosGF = (agent.pos+agent.groupF)*ZOOMFACTOR+xyShift
            pygame.draw.line(screen, lightpink, scPos, endPosGF, 2)
            
        
        for idaj, agentOther in enumerate(agents):
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
            
            if comm[idai, idaj] == 1 and SHOWINTELINE: 
                pygame.draw.line(screen, blue, scPos, scPosOther, 2)
                #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                pygame.draw.line(screen, green, scPos, scPosDir, 4)

            if talk[idai, idaj] == 1 and SHOWINTELINE: 
                pygame.draw.line(screen, red, scPos, scPosOther, 3)
                pygame.draw.line(screen, green, scPos, scPosDir, 4)
        
        #print(scPos)
    
        if SHOWINDEX:
            tt = pygame.time.get_ticks()/1000-t_pause
            myfont=pygame.font.SysFont("arial",14)
            if tt < agent.tpre:
                text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
            else: 
                text_surface=myfont.render(str(idai), True, (0,0,0), (255,255,255))
            screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift)

        if SHOWSTRESS:
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render(str(agent.ratioV), True, (0,0,0), (255,255,255))
            screen.blit(text_surface, agent.pos*ZOOMFACTOR+xyShift+[0,6])

    pygame.display.flip()
    clock.tick(20)

f.close()

