# -*-coding:utf-8-*-
# Author: WP and SS

import pygame
import pygame.draw
import numpy as np
from agent_WP_Random import *
from tools import *
#from config import *
#import random


SCREENSIZE = [800, 400]
RESOLUTION = 180
AGENTSNUM = 8
BACKGROUNDCOLOR = [255,255,255]
AGENTCOLOR = [0,0,255]
LINECOLOR = [255,0,0]
AGENTSIZE = 9
AGENTSICKNESS = 3
#WALLSFILE = "walls.csv"

pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption('Social Force Model - Single-Room Egress')
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


walls = [[3.33, 3.33, 29.97, 3.33], 
[3.33, 3.33, 3.33, 33.31], 
[3.33, 33.31, 29.97, 33.31],
[23.31, 3.33, 33.31, 14.02], 
[33.31, 20.92, 23.31, 33.31]]

print(walls)


# initialize agents
agents = []
for n in range(AGENTSNUM):
    agent = Agent()
    agents.append(agent)


#agents[1].pos = np.array([80, 12])
#agents[1].dest = np.array([20.0,10.0])        
#agents[1].direction = normalize(agents[1].dest - agents[1].pos)
#agents[1].desiredSpeed = 1.8
#agents[1].desiredV = agents[1].desiredSpeed*agents[1].direction

#agents[2].pos = np.array([80, 16])
#agents[2].dest = np.array([20.0,18.0])        
#agents[2].direction = normalize(agents[2].dest - agents[2].pos)
#agents[2].desiredSpeed = 1.2 
#agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
#agents[2].B = 3.6


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
        startPx = startPos*10 #worldCoord2ScreenCoord(startPos,SCREENSIZE,RESOLUTION)
        endPx = endPos*10 #worldCoord2ScreenCoord(endPos,SCREENSIZE,RESOLUTION)
        pygame.draw.line(screen, LINECOLOR,startPx,endPx)

    # draw agents
	#   pygame.draw.circle(screen, AGENTCOLOR, (np.array(SCREENSIZE)/2).tolist(),
	#                      AGENTSIZE, AGENTSICKNESS)


    # Interaction Force
    for idai,ai in enumerate(agents):
        # 初始速度和位置
        ai.direction = normalize(ai.dest - ai.pos)
        ai.desiredV = ai.desiredSpeed*ai.direction
        # 计算受力
        adapt = ai.adaptVel()
        peopleInter = 0.0
        wallInter = 0.0

        for idaj,aj in enumerate(agents):
             if idai == idaj:
                 continue
             peopleInter += ai.peopleInteraction(aj)

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
	
	if (ai.pos[0] >= 35.0) & (ai.Goal == 0):
	    print('test')
	    ai.Goal = 1
	    ai.timeOut = pygame.time.get_ticks()
	    #ai.timeOut = clock.get_time()/1000.0
	    print('Time to Reach the Goal:', ai.timeOut)
        
    

    for agent in agents:
	
        #scPos = agent.pos*10 #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
        scPos = [0, 0]
        scPos[0] = int(agent.pos[0]*10) #worldCoord2ScreenCoord(agent.pos, SCREENSIZE, RESOLUTION)
        scPos[1] = int(agent.pos[1]*10)
        
        endPos = [0, 0]
        endPos[0] = int(agent.pos[0]*10 + agent.actualV[0]*10)
        endPos[1] = int(agent.pos[1]*10 + agent.actualV[1]*10)

        endPosDV = [0, 0]
        endPosDV[0] = int(agent.pos[0]*10 + agent.desiredV[0]*10)
        endPosDV[1] = int(agent.pos[1]*10 + agent.desiredV[1]*10)

        
        pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)
        pygame.draw.line(screen, AGENTCOLOR, scPos, endPos, 2)
	pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)
        
        #print(scPos)

    pygame.display.flip()
    clock.tick(20)
    #clock.get_time
