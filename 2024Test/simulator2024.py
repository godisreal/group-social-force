# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@126.com

import sys, os
import pygame
import pygame.draw
import numpy as np
from agent_model import *
from obst import *
from math_func import *
from math import *
#from config import *
import random
import csv
#from readCSV import *
from data_func import *


# Below are variables for users to set up pygame features
################################################################
SCREENSIZE = [800, 400]
RESOLUTION = 180
BACKGROUNDCOLOR = [255,255,255]
LINESICKNESS = 3
AGENTSIZE = 6
AGENTSICKNESS = 3
ZOOMFACTOR = 10
DT = 0.3
#WALLSFILE = "walls.csv"
#AGENTCOLOR = [0,0,255]

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
black = 0,0,0
purple = 160, 32, 240
magenta = 255, 0, 255


# Below are boolean variables for users to set up the simulation
################################################################
TIMECOUNT = True
THREECIRCLES = False    # Use 3 circles to draw agents
SHOWVELOCITY = True	# Show velocity and desired velocity of agents
SHOWINDEX = True        # Show index of agents
SHOWTIME = True         # Show a clock on the screen
SHOWINTELINE = True     # Draw a line between interacting agents
MODETRAJ = False        # Draw trajectory of agents' movement
COHESION = False        # Enable the cohesive social force
SELFREPULSION = True    # Enable self repulsion
WALLBLOCKHERDING = True
TPREMODE = 1        ### Instructinn: 1 -- DesiredV = 0  2 -- Motive Force =0: 
PAUSE = False
SHOWWALLDATA = True
debug = True

# The file to record the some output data of the simulation
f = open("out.txt", "w+")

ini = 1
marginTitle = 1
#FileName = "Agent_Data2024.csv"
FileName = "Agent_Data2024.csv"

#agentFeatures,IUpper, ILower = getData("agentData2018.csv", '&agent')

agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent')
Num_Agents=len(agentFeatures)-marginTitle
if Num_Agents <= 0:
    agentFeatures, lowerIndex, upperIndex = getData(FileName, '&agent')
    Num_Agents=len(agentFeatures)-marginTitle
if Num_Agents <= 0:
    agentFeatures, lowerIndex, upperIndex = getData(FileName, '&Agent')
    Num_Agents=len(agentFeatures)-marginTitle

f.write("Features of Agents\n"+str(agentFeatures)+"\n")
if debug: 
    print ('Number of Agents:', Num_Agents, '\n')
    print ("Features of Agents\n", agentFeatures, "\n")

agents = []
index = 0 
for agentFeature in agentFeatures[marginTitle:]:
    agent = Agent()
    agent.ID = index
    agent.name = str(agentFeature[ini-1])
    agent.pos = np.array([float(agentFeature[ini+0]), float(agentFeature[ini+1])])
    agent.actualV = np.array([float(agentFeature[ini+2]), float(agentFeature[ini+3])])
    agent.tau = float(agentFeature[ini+4])
    agent.tpre = float(agentFeature[ini+5])
    agent.p = float(agentFeature[ini+6])
    agent.pMode = agentFeature[ini+7]
    agent.aType = agentFeature[ini+8]
    agent.interactionRange = float(agentFeature[ini+9])
    #agent.moving_tau = float(agentFeature[ini+11])
    #agent.tpre_tau = float(agentFeature[ini+12])
    #agent.talk_tau = float(agentFeature[ini+13])
    #agent.talk_prob = float(agentFeature[ini+14])
    #agent.inComp = int(agentFeature[ini+15])
    agents.append(agent)
    index += 1


obstFeatures, lowerIndex, upperIndex = getData(FileName, '&Wall')
Num_Obsts=len(obstFeatures)-marginTitle
if Num_Obsts <= 0:
    obstFeatures, lowerIndex, upperIndex = getData(FileName, '&wall')
    Num_Obsts=len(obstFeatures)-marginTitle

if debug:
    print ('Number of Walls:', Num_Obsts, '\n')
    print ("Features of Walls\n", obstFeatures, "\n")

# initialize OBST
#obstFeatures = readCSV("obstData2018.csv", "string")
walls = []
index = 0
for obstFeature in obstFeatures[marginTitle:]:
    wall = obst()
    wall.name = str(obstFeature[ini-1])
    wall.params[0]= float(obstFeature[ini+0])
    wall.params[1]= float(obstFeature[ini+1])
    wall.params[2]= float(obstFeature[ini+2])
    wall.params[3]= float(obstFeature[ini+3])
    try:
        wall.arrow = int(obstFeature[ini+4])
    except:
        wall.arrow = int(0)
    try:
        wall.mode = str(obstFeature[ini+5])
    except:
        wall.mode = 'rect'
    wall.oid = int(index)
    index += 1
    try:
        wall.pointer1 = np.array([float(obstFeature[ini+6]), float(obstFeature[ini+7])])
        wall.pointer2 = np.array([float(obstFeature[ini+8]), float(obstFeature[ini+9])])
    except:
        wall.pointer1 = np.array([float('NaN'), float('NaN')]) #np.nan #
        wall.pointer2 = np.array([float('NaN'), float('NaN')]) #np.nan #
    walls.append(wall)
    print(wall.arrow)
    print(wall.mode)
    print(wall.pointer1, wall.pointer2)
    

#print(walls)
#input("Please check!")
'''
walls = []
index = 0
for obstFeature in obstFeatures[marginTitle:]:
    wall = obst()
    wall.name = str(obstFeature[ini])
    
    try:
        wall.mode = str(obstFeature[ini+6])
    except:
        wall.mode = 'rect'
    
    if wall.mode == 'line':
        wall.params[0]= float(obstFeature[ini+1])
        wall.params[1]= float(obstFeature[ini+2])
        wall.params[2]= float(obstFeature[ini+3])
        wall.params[3]= float(obstFeature[ini+4])
    
    elif wall.mode == 'rect':
        wall.params[0]= min(float(obstFeature[ini+1]),float(obstFeature[ini+3]))
        wall.params[1]= min(float(obstFeature[ini+2]),float(obstFeature[ini+4]))
        wall.params[2]= max(float(obstFeature[ini+1]),float(obstFeature[ini+3]))
        wall.params[3]= max(float(obstFeature[ini+2]),float(obstFeature[ini+4]))
    
    wall.oid = index
    index = index+1
    
    try:
        wall.arrow = int(obstFeature[ini+5])
    except:
        wall.arrow = int(0)
    
    try:
        wall.mode = str(obstFeature[ini+6])
    except:
        wall.mode = 'rect'
        
    try:
        wall.inComp = int(obstFeature[ini+7])
    except:
        wall.inComp = int(1)

    try:
        wall.pointer1 = np.array([float(obstFeature[8]), float(obstFeature[9])])
        wall.pointer2 = np.array([float(obstFeature[10]), float(obstFeature[11])])
    except:
        wall.pointer1 = np.nan #np.array([float('NaN'), float('NaN')])
        wall.pointer2 = np.nan #np.array([float('NaN'), float('NaN')])
    
    # Walls have no exit signs if arrow is 0
    #wall.exitSign = bool(wall.arrow)
    walls.append(wall)
'''

#doors = readCSV("Door_Data2018.csv", "float")
#agent2doors = readCSV("Agent2Door2018.csv", "float")


exitFeatures, lowerIndex, upperIndex = getData(FileName, '&Exit')
Num_Exits=len(exitFeatures)-marginTitle
if Num_Exits <= 0:
    exitFeatures, lowerIndex, upperIndex = getData(FileName, '&exit')
    Num_Exits=len(exitFeatures)-marginTitle
    
if debug: 
    print ('Number of Exits:', Num_Exits, '\n')
    print ("Features of Exits\n", exitFeatures, "\n")

exits = []
index = 0
for exitFeature in exitFeatures[marginTitle:]:
    exit = passage()
    exit.name = str(exitFeature[ini-1])
    exit.params[0]= min(float(exitFeature[ini+0]),float(exitFeature[ini+2]))
    exit.params[1]= min(float(exitFeature[ini+1]),float(exitFeature[ini+3]))
    exit.params[2]= max(float(exitFeature[ini+0]),float(exitFeature[ini+2]))
    exit.params[3]= max(float(exitFeature[ini+1]),float(exitFeature[ini+3]))
    try:
        exit.arrow = int(exitFeature[ini+4])
    except:
        exit.arrow = int(0)
    try:
        exit.mode = str(exitFeature[ini+5])
        exit.inComp = int(exitFeature[ini+6])
        #exit.exitSign = int(exitFeature[ini+8])
    except:
        exit.mode = 'rect'
        exit.inComp = int(1)
        #exit.exitSign = int(1)

    # Exits have  exit signs
    exit.exitSign = 1
    # Exits are all in rectangular shape in current progame
    if exit.mode != 'rect':
        exit.mode = 'rect'
    exit.pos = (np.array([exit.params[0], exit.params[1]]) + np.array([exit.params[2], exit.params[3]]))*0.5
    exit.oid = index
    index = index+1
    exits.append(exit)
        

n_agents = len(agents)
n_walls = len(walls)
n_exits = len(exits)
print(n_agents, n_walls, n_exits)

f.write('Number of Agents:'+str(n_agents)+'\n')
f.write('Number of Walls:'+str(n_walls)+'\n')
f.write('Number of Exits:'+str(n_exits)+'\n')
        
tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&Ped2Exit')
if len(tableFeatures)<=0:
    tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&Agent2Exit')
if len(tableFeatures)<=0:
    tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&agent2exit')

if len(tableFeatures)>0:
    agent2exit = readFloatArray(tableFeatures,n_agents, n_exits)

    if np.shape(agent2exit)!= (n_agents, n_exits): #or np.shape(agent2exit)[1]!=
        print('\n!!! Error on input data: exits or agent2exit !!! \n')
        f.write('\n!!! Error on input data: exits or agent2exit !!! \n')
        #raw_input('Error on input data: exits or agent2exit!  Please check')
        inputDataCorrect = False
    else:
        f.write('\n Input data: exits or agent2exit: \n'+str(agent2exit)+'\n')
        print('\n!Agent2Exit!', agent2exit, '!!! \n')
        inputDataCorrect = True

tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&GroupD')
if len(tableFeatures)<=0:
    tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&groupD')
DFactor_Init = readFloatArray(tableFeatures, n_agents, n_agents)

tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&GroupA')
if len(tableFeatures)<=0:
    tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&groupA')
AFactor_Init = readFloatArray(tableFeatures, n_agents, n_agents)

tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&GroupB')
if len(tableFeatures)<=0:
    tableFeatures, LowerIndex, UpperIndex = getData(FileName, '&groupB')
BFactor_Init = readFloatArray(tableFeatures, n_agents, n_agents)


if np.shape(DFactor_Init)!= (n_agents, n_agents) or np.shape(AFactor_Init)!= (n_agents, n_agents) or np.shape(BFactor_Init)!= (n_agents, n_agents): #or np.shape(agent2exit)[1]!=
    print('\n!!! Error on input data:  DFactor_Init, AFactor_Init, BFactor_Init !!! \n')
    f.write('\n!!! Error on input data:  DFactor_Init, AFactor_Init, BFactor_Init !!! \n')
    #raw_input('Error on input data: exits or agent2exit!  Please check')
    inputDataCorrect = False
else:
    f.write('\n Input data: DFactor_Init: \n'+str(DFactor_Init)+'\n')
    f.write('\n Input data: AFactor_Init: \n'+str(AFactor_Init)+'\n')
    f.write('\n Input data: BFactor_Init: \n'+str(BFactor_Init)+'\n')
    print('\n!D!', DFactor_Init, '!!! \n')
    print('\n!A!', AFactor_Init, '!!! \n')
    print('\n!B!', BFactor_Init, '!!! \n')
    inputDataCorrect = True

if sys.version_info[0] == 2: 
    raw_input("Please check!")
else:
    input("please check!")
    

# Initialize Desired Interpersonal Distance --- Old stuffs
#DFactor_Init = readCSV("D_Data2018.csv", 'float')
#AFactor_Init = readCSV("A_Data2018.csv", 'float')
#BFactor_Init = readCSV("B_Data2018.csv", 'float')

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

f.write("Wall Matrix\n"+str(walls)+"\n")
f.write("D Matrix\n"+str(DFactor_Init)+"\n")
f.write("A Matrix\n"+str(AFactor_Init)+"\n")
f.write("B Matrix\n"+str(BFactor_Init)+"\n")

if np.shape(DFactor_Init)!= (Num_Agents, Num_Agents):
    print('\nError on input data: DFactor_Init\n')
    f.write('\nError on input data: DFactor_Init\n')
    
if np.shape(AFactor_Init)!= (Num_Agents, Num_Agents): 
    print('\nError on input data: AFactor_Init\n')
    f.write('\nError on input data: AFactor_Init\n')

if np.shape(BFactor_Init)!= (Num_Agents, Num_Agents): 
    print('\nError on input data: BFactor_Init\n')
    f.write('\nError on input data: BFactor_Init\n')
    
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

#agents[2].pos = np.array([60, 12])    
#agents[2].direction = normalize(agents[2].dest - agents[2].pos)
agents[2].desiredSpeed = 1.8 
#agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
#agents[2].B = 3.6
agents[2].p = 0.6 #0.1
agents[2].pMode = 'fixed'
agents[2].interactionRange = 6.0

#agents[0].changeAttr(32, 22, 0, 0)
agents[0].pMode = 'fixed'


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
            if event.key == pygame.K_UP:
                ZOOMFACTOR = ZOOMFACTOR +1
            elif event.key == pygame.K_DOWN:
                ZOOMFACTOR = max(0, ZOOMFACTOR -1)
            elif event.key == pygame.K_t:
                MODETRAJ = not MODETRAJ
            elif event.key == pygame.K_SPACE:
                PAUSE = not PAUSE
            elif event.key == pygame.K_v:
                SHOWVELOCITY = not SHOWVELOCITY
            elif event.key == pygame.K_i:
                SHOWINDEX = not SHOWINDEX

    if MODETRAJ == False:
        screen.fill(BACKGROUNDCOLOR)

    if PAUSE ==  True:
        t_now = pygame.time.get_ticks()/1000
        t_pause = t_now-tt
        continue

    # Compute the agents one by one in loop
    for idai,ai in enumerate(agents):
        
        # Whether ai is in computation
        if ai.inComp == 0:
            continue
	
        #Pre-evacuation Time Effect
        # Question:  Shall I put tt here or outside the loop of ai ???
        tt = pygame.time.get_ticks()/1000-t_pause
        if (tt < ai.tpre):
            ai.desiredSpeed = random.uniform(0.3,0.6)
        else: 
            ai.desiredSpeed = random.uniform(2.0,3.0)
	
        #ai.dest = ai.memory.peek()
	
        ai.direction = normalize(ai.dest - ai.pos)
        ai.desiredV = ai.desiredSpeed*ai.direction
        #ai.desiredV = 0.7*ai.desiredV + 0.3*ai.desiredV_old
        peopleInter = 0.0
        wallInter = 0.0
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
            #ai.p = 1 - ai.ratioV  	# Method-2
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
                    result, flag = ai.wallInBetween(aj, wall)
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
        
        print('idai:', idai)
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
                DFactor[idai, idaj]=1.0
                AFactor[idai, idaj]=600
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

        #########################
        # Calculate Wall Repulsion
        for wall in walls:
            wallInter += ai.wallForce(wall)

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
	

        #temp = 0.0
        #maxWallForce = 0.0
        #wallDirection = np.array([0.0, 0.0])
	
        #for idwall, wall in enumerate(walls):
        #temp = np.linalg.norm(ai.wallForce(wall))
        #    if temp > maxWallForce: 
        #	maxWallForce = temp
        #	wallDirection = np.array([wall[0],wall[1]]) - np.array([wall[2],wall[3]])
        #	closeWall = wall
	
        if (tt >= ai.tpre):
        #################################
        # Wall Effect Computed: 
        # Is There Any Wall Nearby On The Route?
        # If So, Adjust Desired Direction 

            # temp = 0.0
            closeWall = walls[0] #None #walls[0]
            closeWallDist = 30.0 # Define how close the wall is
            for wall in walls:
                diw = ai.wallOnRoute(wall, 1.0)
                if diw!=None and diw < closeWallDist:
                    closeWallDist = diw
                    closeWall = wall
		    
	
            diw = ai.wallOnRoute(closeWall)
            if diw!=None:
            #if closeWall!=None:
            #    diw = ai.wallOnRoute(closeWall)
                wallDirection = np.array([closeWall.params[0],closeWall.params[1]]) - np.array([closeWall.params[2],closeWall.params[3]])
                wallDirection = -normalize(wallDirection)
                if np.dot(wallDirection, ai.actualV) < 0.0 and wall.arrow==0:
                #0.3*ai.desiredV+0.7*ai.desiredV_old) < 0.0:
                    wallDirection = -wallDirection
                
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
        sumForce = motiveForce + peopleInter + wallInter + ai.diss*ai.actualV + selfRepulsion #+ ai.sumAdapt
        
        # Compute acceleration
        accl = sumForce/ai.mass
        
        # Compute velocity
        ai.actualV = ai.actualV + accl*DT # consider dt = 0.5
        
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
            f.write('Time to Reach the Goal:'+str(ai.timeOut))
        
        ###########################################
        ## Remove agent when agent reaches the destination    
        #if np.linalg.norm(ai.pos-ai.dest)<=1e-3:
         #   agents.remove(agents[idai])

    
    ####################
    # Drawing the walls
    ####################
    
    for wall in walls:
        startPos = np.array([wall.params[0],wall.params[1]])
        endPos = np.array([wall.params[2],wall.params[3]])
        startPx = startPos*ZOOMFACTOR
        endPx = endPos*ZOOMFACTOR
        pygame.draw.line(screen, red, startPx, endPx, LINESICKNESS)
        
        if isnan(wall.pointer1[0]) or isnan(wall.pointer1[1]):
            pass
            #input("Please check!")
        else:
            guidePos = np.array([wall.pointer1[0], wall.pointer1[1]])
            guidePx = [0, 0]
            guidePx[0] = int(guidePos[0])*ZOOMFACTOR 
            guidePx[1] = int(guidePos[1])*ZOOMFACTOR
            pygame.draw.circle(screen, red, guidePx, LINESICKNESS)

        if isnan(wall.pointer2[0]) or isnan(wall.pointer2[1]):
            pass
            #input("Please check!")
        else:
            guidePos = np.array([wall.pointer2[0], wall.pointer2[1]])
            guidePx = [0, 0]
            guidePx[0] = int(guidePos[0])*ZOOMFACTOR 
            guidePx[1] = int(guidePos[1])*ZOOMFACTOR
            pygame.draw.circle(screen, red, guidePx, LINESICKNESS)

        if SHOWWALLDATA:
            myfont=pygame.font.SysFont("arial",14)
            text_surface=myfont.render(str(startPos), True, (255,0,0), (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR)
            text_surface=myfont.render(str(endPos), True, (255,0,0), (255,255,255))
            screen.blit(text_surface, endPos*ZOOMFACTOR)
            
    
    ####################
    # Drawing the doors
    ####################
    
    for exit in exits:
        
        Pos = exit.pos #np.array([door[0], door[1]])
        Px = [0, 0]
        Px[0] = int(Pos[0]*ZOOMFACTOR)
        Px[1] = int(Pos[1]*ZOOMFACTOR)
        pygame.draw.circle(screen, purple, Px, LINESICKNESS)
        
        '''
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
            
        pygame.draw.rect(screen, orange, [x+ xSpace, y+ ySpace, w, h], 2)

        if SHOWDATA:

            myfont=pygame.font.SysFont("arial",10)
            text_surface=myfont.render(str(startPos), True, blue, (255,255,255))
            screen.blit(text_surface, startPos*ZOOMFACTOR + xyShift)

            #text_surface=myfont.render(str(endPos), True, blue, (255,255,255))
            #screen.blit(text_surface, endPos*ZOOMFACTOR + xyShift)

            myfont=pygame.font.SysFont("arial",13)
            text_surface=myfont.render('Exit:'+str(exit.oid)+'/'+str(exit.name)+'/'+str(exit.arrow), True, red, white)
            screen.blit(text_surface, exit.pos*ZOOMFACTOR + xyShift)
        '''

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
        scPos[0] = int(agent.pos[0]*ZOOMFACTOR)
        scPos[1] = int(agent.pos[1]*ZOOMFACTOR)
        
        #temp = int(100*agent.ratioV)
        #AGENTCOLOR = [0,0,temp]
        color_para = [0, 0, 0]
        color_para[0] = int(255*min(1, agent.ratioV))
        pygame.draw.circle(screen, color_para, scPos, AGENTSIZE, AGENTSICKNESS)
	#int(ai.radius*ZOOMFACTOR), AGENTSICKNESS)
        
        if THREECIRCLES:
            leftS = [0, 0]
            leftShoulder = agent.shoulders()[0]
            leftS[0] = int(leftShoulder[0]*ZOOMFACTOR)
            leftS[1] = int(leftShoulder[1]*ZOOMFACTOR)
        
            rightS = [0, 0]
            rightShoulder = agent.shoulders()[1]	
            rightS[0] = int(rightShoulder[0]*ZOOMFACTOR)
            rightS[1] = int(rightShoulder[1]*ZOOMFACTOR)
            
            #print 'shoulders:', leftS, rightS
            pygame.draw.circle(screen, color_para, leftS, AGENTSIZE/2, 3)
            pygame.draw.circle(screen, color_para, rightS, AGENTSIZE/2, 3)
        
        if SHOWVELOCITY:
            endPosV = [0, 0]
            endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR)
            endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR)
        
            endPosDV = [0, 0]
            endPosDV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.desiredV[0]*ZOOMFACTOR)
            endPosDV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.desiredV[1]*ZOOMFACTOR)
        
            #stressShow = 0
            #stressShow = int(255*agent.ratioV)
            #pygame.draw.line(screen, blue, leftS, rightS, 3)
            pygame.draw.line(screen, blue, scPos, endPosV, 2)
            pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)
	    
	
        for idaj, agentOther in enumerate(agents):
            scPosOther = [0, 0]
            scPosOther[0] = int(agentOther.pos[0]*ZOOMFACTOR)
            scPosOther[1] = int(agentOther.pos[1]*ZOOMFACTOR)
            
            agentPer = agent.pos+0.8*normalize(agentOther.pos - agent.pos)
            scPosDir = [int(agentPer[0]*ZOOMFACTOR), int(agentPer[1]*ZOOMFACTOR)]
            
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
            #tt = pygame.time.get_ticks()/1000-t_pause
            myfont=pygame.font.SysFont("arial",14)
            if tt < agent.tpre:
                text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
            else: 
                text_surface=myfont.render(str(idai), True, (0,0,0), (255,255,255))
            screen.blit(text_surface, agent.pos*ZOOMFACTOR)
	    
        if SHOWTIME:
            #tt = pygame.time.get_ticks()/1000-t_pause
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Time:" + str(tt), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [730,370]) #[750,350]*ZOOMFACTOR)

    pygame.display.flip()
    clock.tick(20)

f.close()

