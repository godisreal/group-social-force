# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@126.com

import pygame
import pygame.draw
import numpy as np
from agent_model import *
from math_func import *
from math import *
#from config import *
import random
import csv
from readCSV import *
#from stack import *

SCREENSIZE = [800, 400]
RESOLUTION = 180
BACKGROUNDCOLOR = [255,255,255]
AGENTCOLOR = [0,0,255]
LINECOLOR = [255,0,0]
LINESICKNESS = 4
AGENTSIZE = 6
AGENTSICKNESS = 3
#WALLSFILE = "walls.csv"
#AGENTSNUM = 8
ZOOMFACTOR = 10
DT = 0.3
TIMECOUNT = True
THREECIRCLES = False  	# Use 3 circles to draw agents
SHOWVELOCITY = False	# Show velocity and desired velocity of agents
SHOWINDEX = True
SHOWTIME = True
COHESION = False		# Enable the cohesive social force
SELFREPULSION = True	# Enable self repulsion
WALLBLOCKHERDING = True
TPREMODE = 2        ### Instructinn: 1 -- Motive Force =0: 2 -- DesiredV = 0

f = open("out.txt", "w+")

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


#initialize agents
#agentFeatures = []
#for line in open("pedTest.txt"):
#    coords = line.split(',')
#    agentFeature = []
#    agentFeature.append(float(coords[0]))
#    agentFeature.append(float(coords[1]))
#    agentFeature.append(float(coords[2]))
#    agentFeature.append(float(coords[3]))
#    agentFeatures.append(agentFeature)


agentFeatures = readCSV("Agent_Data2018.csv")
[Num_Agents, Num_Features] = np.shape(agentFeatures)
print >> f, 'Number of Agents:', Num_Agents, '\n'
print >> f, "Features of Agents\n", agentFeatures, "\n"


agents = []
for agentFeature in agentFeatures:
    agent = Agent()
    agent.pos = np.array([agentFeature[0], agentFeature[1]])
    agent.dest = np.array([agentFeature[2], agentFeature[3]])
    agent.acclTime = agentFeature[4]
    agent.tpre = agentFeature[5]
    agent.p = agentFeature[6]
    agent.mass = agentFeature[7]
    agents.append(agent)

walls = readCSV("Wall_Data2018.csv")
doors = readCSV("Door_Data2018.csv")

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


# Initialize Desired Interpersonal Distance

DFactor_Init = readCSV("D_Data2018.csv")
AFactor_Init = readCSV("A_Data2018.csv")
BFactor_Init = readCSV("B_Data2018.csv")

#print walls
#print DFactor_Init
#print AFactor_Init
#print BFactor_Init

print >> f, "Wall Matrix\n", walls, "\n"
print >> f, "D Matrix\n", DFactor_Init, "\n"
print >> f, "A Matrix\n", AFactor_Init, "\n"
print >> f, "B Matrix\n", BFactor_Init, "\n"

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
    print '\nError on input data: DFactor_Init\n'
    print >>f, '\nError on input data: DFactor_Init\n'
    
if np.shape(AFactor_Init)!= (Num_Agents, Num_Agents): 
    print '\nError on input data: AFactor_Init\n'
    print >>f, '\nError on input data: AFactor_Init\n'

if np.shape(BFactor_Init)!= (Num_Agents, Num_Agents): 
    print '\nError on input data: BFactor_Init\n'
    print >>f, '\nError on input data: BFactor_Init\n'
    

DFactor = DFactor_Init
AFactor = AFactor_Init
BFactor = BFactor_Init

comm = np.zeros((Num_Agents, Num_Agents))

# initialize agents
#agents = []
#for n in range(Num_Agents):
#    agent = Agent()
#    agents.append(agent)


#agents[1].pos = np.array([60, 8])
#agents[1].dest = np.array([20.0,10.0])        
#agents[1].direction = normalize(agents[1].dest - agents[1].pos)
agents[1].desiredSpeed = 1.8
#agents[1].desiredV = agents[1].desiredSpeed*agents[1].direction
agents[1].p = 0.2

#agents[2].pos = np.array([60, 12])
#agents[2].dest = np.array([20.0,18.0])        
#agents[2].direction = normalize(agents[2].dest - agents[2].pos)
agents[2].desiredSpeed = 1.8 
#agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
#agents[2].B = 3.6
agents[2].p = 0.1
agents[2].pMode = 'fixed'

#agents[0].changeAttr(32, 22, 0, 0)
agents[0].pMode = 'fixed'


pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Modified Social Force Model')
clock = pygame.time.Clock()

red=255,0,0
green=0,255,0
blue=0,0,255
white=255,255,255
yellow=255,255,0
IndianRed=205,92,92

#myfont=pygame.font.SysFont("arial",16)
#text_surface=myfont.render("No2",True, (0,0,0), (255,255,255))
#screen.blit(text_surface, (16,20))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
        # elif event.type == pygame.MOUSEBUTTONUP:

    screen.fill(BACKGROUNDCOLOR)


    # Compute the agents
    for idai,ai in enumerate(agents):
	
        #Pre-evacuation Time Effect
        tt = pygame.time.get_ticks()/1000
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
        otherMovingDir = np.array([0.0, 0.0])
        otherMovingSpeed = 0.0
        otherMovingNum = 0
	
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
	    
	    
        #############################################
        # Compute interaction of agents
        # Group force and herding effect

        for idaj,aj in enumerate(agents):
	    
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
                    if flag == True:
                        no_wall_ij = False
	     
            see_ij = True
            if np.dot(ai.actualV, aj.pos-ai.pos)<0.2:
                see_ij = False
	     
            #############################################
            # Turn on or off cohesive social force
            # Also known as group force
            if COHESION and no_wall_ij: #and see_ij:
                peopleInter += ai.cohesiveForce(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])*anisoF
	     
	     
            #############################################
            # Traditional Social Force and Physical Force
            if no_wall_ij and see_ij:
                peopleInter += ai.agentForce(aj)*anisoF
	     
	     	         
            #################################
            # Herding Effect Starts Here
            # Also Known As Opinion Dynamics
            #################################
            if dij < ai.B_CF*BFactor[idai, idaj] + rij*DFactor[idai, idaj] and no_wall_ij and see_ij:
            #if dij < ai.interactionRange and no_wall_ij:
                otherMovingDir += normalize(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
                otherMovingSpeed += np.linalg.norm(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
                otherMovingNum += 1
                comm[idai, idaj] = 1
		
                #DFactor[idai, idaj] = (1-ai.p)*DFactor[idai, idaj]+ai.p*DFactor[idaj, idai]
                #AFactor[idai, idaj] = (1-ai.p)*AFactor[idai, idaj]+ai.p*AFactor[idaj, idai]
                #BFactor[idai, idaj] = (1-ai.p)*BFactor[idai, idaj]+ai.p*BFactor[idaj, idai]
                #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*aj.desiredV		
            else: 
                comm[idai, idaj] = 0
	     

        #################################
        # Herding Effect Computed
        if otherMovingNum != 0:
            ai.direction = (1-ai.p)*ai.direction + ai.p*otherMovingDir
            ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + ai.p*otherMovingSpeed/otherMovingNum
            ai.desiredV = ai.desiredSpeed*ai.direction

            #ai.desiredV = (1-ai.p)*ai.desiredV + ai.p*otherMovingDir


        #############################################
        # Turn on or off self-repulsion
        # Also known as sub-consciousness effect in crowd dynamics
        if SELFREPULSION and (otherMovingNum != 0):
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
	
        #########################
        # Calculate Motive Forces
        # Consider TPRE features
	
        tt = pygame.time.get_ticks()/1000
        if (tt < ai.tpre and TPREMODE == 1):
            ai.desiredV = ai.direction*0.0
            ai.desiredSpeed = 0.0
            #ai.dest = ai.pos
            motiveForce = ai.adaptVel()
	
        #ai.sumAdapt += motiveForce*0.2  #PID: Integration Test Here
        
        #tt = pygame.time.get_ticks()/1000
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
            closeWall = walls[0]
            closeWallDist = 30.0
            wallDirection = np.array([closeWall[0], closeWall[1]]) - np.array([closeWall[2], closeWall[3]])
            for idwall, wall in enumerate(walls):
                result, flag, diw = ai.wallOnRoute(wall, 1.0)
                if flag: 
                    if diw < closeWallDist:
                        closeWallDist = diw
                        closeWall = wall
                        wallDirection = np.array([wall[0],wall[1]]) - np.array([wall[2],wall[3]])
		    
	
            result, flag, diw = ai.wallOnRoute(closeWall)
            if flag:
                if np.dot(wallDirection, ai.actualV) < 0.0:
                #0.3*ai.desiredV+0.7*ai.desiredV_old) < 0.0:
                    wallDirection = -wallDirection
                    #ai.memory.append(np.array([wall[2],wall[3]]))
                #else:  
                    #ai.memory.append(np.array([wall[0],wall[1]]))
            
                ai.direction = ai.direction + wallDirection/np.linalg.norm(wallDirection)*20/diw
                ai.desiredV = ai.desiredSpeed*ai.direction
	    
	#if np.linalg.norm(ai.pos-ai.memory[-1])<=1e-1:
	#ai.memory.pop()
            motiveForce = ai.adaptVel()	

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
        if TIMECOUNT and (ai.pos[0] >= 35.0) and (ai.Goal == 0):
            print('test')
            ai.Goal = 1
            ai.timeOut = pygame.time.get_ticks()
            #ai.timeOut = clock.get_time()/1000.0
            print 'Time to Reach the Goal:', ai.timeOut
            print >> f, 'Time to Reach the Goal:', ai.timeOut

    
    ####################
    # Drawing the walls
    ####################
    
    for wall in walls:
        startPos = np.array([wall[0],wall[1]])
        endPos = np.array([wall[2],wall[3]])
        startPx = startPos*ZOOMFACTOR
        endPx = endPos*ZOOMFACTOR
        pygame.draw.line(screen, LINECOLOR, startPx, endPx, LINESICKNESS)
	
    
    ####################
    # Drawing the doors
    ####################
    
    for door in doors:
        Pos = np.array([door[0], door[1]])
        Px = [0, 0]
        Px[0] = int(Pos[0]*ZOOMFACTOR)
        Px[1] = int(Pos[1]*ZOOMFACTOR)
        pygame.draw.circle(screen, LINECOLOR, Px, LINESICKNESS)

    # draw agents
    #   pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(),
    #                      AGENTSIZE, AGENTSICKNESS)
    
    ####################
    # Drawing the agents
    ####################
    #for agent in agents:
    
    for idai, agent in enumerate(agents):
        #scPos = np.array([0, 0])
        scPos = [0, 0]
        scPos[0] = int(agent.pos[0]*ZOOMFACTOR)
        scPos[1] = int(agent.pos[1]*ZOOMFACTOR)
        
        #temp = int(100*agent.ratioV)
        #AGENTCOLOR = [0,0,temp]
        color_para = [0, 0, 0]
        color_para[0] = int(255*min(1, agent.ratioV))
        pygame.draw.circle(screen, color_para, scPos, AGENTSIZE, AGENTSICKNESS)
        
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
            #pygame.draw.line(screen, AGENTCOLOR, leftS, rightS, 3)
            pygame.draw.line(screen, AGENTCOLOR, scPos, endPosV, 2)
            pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)
	    
	
        for idaj, agentOther in enumerate(agents):
            scPosOther = [0, 0]
            scPosOther[0] = int(agentOther.pos[0]*ZOOMFACTOR)
            scPosOther[1] = int(agentOther.pos[1]*ZOOMFACTOR)
            
            agentPer = agent.pos+0.8*normalize(agentOther.pos - agent.pos)
            scPosDir = [int(agentPer[0]*ZOOMFACTOR), int(agentPer[1]*ZOOMFACTOR)]
            
            leftShoulder, rightShoulder = agent.shoulders()
            leftS = [int(leftShoulder[0]*ZOOMFACTOR), int(leftShoulder[1]*ZOOMFACTOR)]
            rightS = [int(rightShoulder[0]*ZOOMFACTOR), int(rightShoulder[1]*ZOOMFACTOR)]
            
            if comm[idai, idaj] == 1: 
                pygame.draw.line(screen, AGENTCOLOR, scPos, scPosOther, 2)
                #pygame.draw.circle(screen, blue, scPosDir, 2, 2)
                #pygame.draw.line(screen, blue, scPosDir, rightS, 2)
                #pygame.draw.line(screen, blue, scPosDir, leftS, 2)
                pygame.draw.line(screen, green, scPos, scPosDir, 4)
        
        #print(scPos)
	
        if SHOWINDEX:
            tt = pygame.time.get_ticks()/1000
            myfont=pygame.font.SysFont("arial",14)
            if tt < agent.tpre:
                text_surface=myfont.render(str(idai), True, (255,0,0), (255,255,255))
            else: 
                text_surface=myfont.render(str(idai), True, (0,0,0), (255,255,255))
            screen.blit(text_surface, agent.pos*ZOOMFACTOR)
	    
        if SHOWTIME:
            tt = pygame.time.get_ticks()/1000
            myfont=pygame.font.SysFont("arial",14)
            time_surface=myfont.render("Time:" + str(tt), True, (0,0,0), (255,255,255))
            screen.blit(time_surface, [730,370]) #[750,350]*ZOOMFACTOR)

    pygame.display.flip()
    clock.tick(20)

f.close()

