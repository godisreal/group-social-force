# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@126.com

import pygame
import pygame.draw
import numpy as np
from particle_Regroup import *
#from tools import *
#from config import *
import random


SCREENSIZE = [800, 400]
RESOLUTION = 180
AGENTSNUM = 6
BACKGROUNDCOLOR = [255,255,255]
AGENTCOLOR = [0,0,255]
LINECOLOR = [255,0,0]
AGENTSIZE = 9
AGENTSICKNESS = 3
#WALLSFILE = "walls.csv"
ZOOMFACTOR = 10

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Modified Social Force Model')
clock = pygame.time.Clock()

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
agentFeatures = []
for line in open("pedTest.txt"):
    coords = line.split(',')
    agentFeature = []
    agentFeature.append(float(coords[0]))
    agentFeature.append(float(coords[1]))
    agentFeature.append(float(coords[2]))
    agentFeature.append(float(coords[3]))
    agentFeatures.append(agentFeature)


agents = []
for agentFeature in agentFeatures:
    agent = Agent()
    agent.pos = np.array([agentFeature[0], agentFeature[1]])
    agent.dest = np.array([agentFeature[2], agentFeature[3]])
    agents.append(agent)


walls = [[3.33, 3.33, 23.97, 3.33], 
[3.33, 3.33, 3.33, 30.31], 
[3.33, 30.31, 23.97, 30.31]] 
#[23.31, 3.33, 33.31, 10.02], 
#[33.31, 16.92, 23.31, 23.31]]

print(walls)


# Initialize Desired Interpersonal Distance


#DFactor = np.array(
#[[0.0, 0.3, 0.9, 1.3], 
#[0.3, 0.0, 0.3, 2.3], 
#[0.6, 0.3, 0.0, 1.3],
#[1.3, 2.1, 0.9, 0.0]])


DFactor = np.array(
[[0.0, 0.3, 0.9, 1.3, 1.6, 1.0], 
[0.3, 0.0, 0.3, 1.6, 1.0, 1.2], 
[0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
[1.3, 0.6, 1.3, 0.0, 1.7, 1.1],
[1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
[1.0, 1.2, 0.3, 2.1, 1.8, 0.0]])

AFactor = np.array(
[[0.0, 0.3, 0.9, 1.3, 1.6, 1.0], 
[0.3, 0.0, 0.3, 1.6, 1.0, 1.2], 
[0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
[1.3, 1.6, 1.3, 0.0, 1.7, 1.1],
[1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
[1.0, 1.2, 1.2, 2.1, 1.8, 0.0]])

BFactor = np.array(
[[0.0, 0.3, 0.9, 2.3, 2.6, 1.0], 
[1.3, 0.0, 3.3, 1.6, 3.0, 1.2], 
[0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
[1.3, 18.6, 1.3, 0.0, 1.7, 1.1],
[1.6, 1.0, 1.3, 12.7, 0.0, 1.8],
[1.0, 1.2, 18.8, 2.1, 1.8, 0.0]])



# initialize agents
agents = []
for n in range(AGENTSNUM):
    agent = Agent()
    agents.append(agent)



agents[1].pos = np.array([60, 8])
agents[1].dest = np.array([20.0,10.0])        
#agents[1].direction = normalize(agents[1].dest - agents[1].pos)
agents[1].desiredSpeed = 1.8
#agents[1].desiredV = agents[1].desiredSpeed*agents[1].direction
agents[1].p = 0.9

agents[2].pos = np.array([60, 12])
agents[2].dest = np.array([20.0,18.0])        
#agents[2].direction = normalize(agents[2].dest - agents[2].pos)
agents[2].desiredSpeed = 1.8 
#agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
#agents[2].B = 3.6
agents[2].p = 0.9

agents[3].changeAttr(32, 22, 0, 0)
agents[3].p = 0.6

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
        # elif event.type == pygame.MOUSEBUTTONUP:

    screen.fill(BACKGROUNDCOLOR)

    # draw walls
    for wall in walls:
        startPos = np.array([wall[0],wall[1]])
        endPos = np.array([wall[2],wall[3]])
        startPx = startPos*10 
        endPx = endPos*10
        pygame.draw.line(screen, LINECOLOR,startPx,endPx)

    # draw agents
	#   pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(),
	#                      AGENTSIZE, AGENTSICKNESS)


    # 计算相互作用力
    for idai,ai in enumerate(agents):
        # 初始速度和位置
        #v0 = ai.actualV
        #r0 = ai.pos
        ai.direction = normalize(ai.dest - ai.pos)
        ai.desiredV = ai.desiredSpeed*ai.direction
        # 计算受力
        #adapt = ai.adaptVel()
        peopleInter = 0.0
        wallInter = 0.0
	otherMovingDir = np.array([0.0, 0.0])
	otherMovingSpeed = 0.0
	otherMovingNum = 0

        for idaj,aj in enumerate(agents):
             if idai == idaj:
                 continue
             peopleInter += ai.peopleInteraction(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])
             
             otherMovingDir += ai.peopleInterOpinion(aj)[0]
	     otherMovingSpeed += ai.peopleInterOpinion(aj)[1]
	     otherMovingNum += ai.peopleInterOpinion(aj)[2]

	     #ai.desiredV = ai.p*ai.desiredV + ai.peopleInterOpinion(aj)[0]
	     # The Above Method is Not Correct
        

	if otherMovingNum != 0:
	    ai.direction = ai.p*ai.direction + (1-ai.p)*otherMovingDir
	    ai.desiredSpeed = ai.p*ai.desiredSpeed + (1-ai.p)*otherMovingSpeed/otherMovingNum
	    ai.desiredV = ai.desiredSpeed*ai.direction

	#ai.desiredV = ai.p*ai.desiredV + (1-ai.p)*otherMovingDir

        adapt = ai.adaptVel()
	
	for wall in walls:
            wallInter += ai.wallInteraction(wall)

        #print('Forces from Walls:', wallInter)
        #print('Forces from people:', peopleInter)
        
        sumForce = adapt + peopleInter + wallInter
        # 计算加速度
        accl = sumForce/ai.mass
        # 计算速度
        ai.actualV = ai.actualV + accl*0.5 # consider dt = 0.5
        # 计算位移
        ai.pos = ai.pos + ai.actualV*0.5
        #print(ai.pos)
        #print(accl,ai.actualV,ai.pos)
        
    
    for agent in agents:
        scPos = [0, 0]
        scPos[0] = int(agent.pos[0]*10)
        scPos[1] = int(agent.pos[1]*10)
        
        endPosV = [0, 0]
        endPosV[0] = int(agent.pos[0]*10 + agent.actualV[0]*10)
        endPosV[1] = int(agent.pos[1]*10 + agent.actualV[1]*10)
        
        endPosDV = [0, 0]
        endPosDV[0] = int(agent.pos[0]*10 + agent.desiredV[0]*10)
        endPosDV[1] = int(agent.pos[1]*10 + agent.desiredV[1]*10)
        
        pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)
        pygame.draw.line(screen, AGENTCOLOR, scPos, endPosV, 2)
        pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)
        
        #print(scPos)

    pygame.display.flip()
    clock.tick(20)


