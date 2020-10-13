# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@126.com

import pygame
import pygame.draw
import numpy as np
#import pedestrian_0817
from pedestrian_0817 import *
#from particle_Regroup import *
#from tools import *
import random
import matplotlib.pyplot as plt


SCREENSIZE = [800, 400]
RESOLUTION = 180
AGENTSNUM = 3
BACKGROUNDCOLOR = [255,255,255]
AGENTCOLOR = [0,0,255]
LINECOLOR = [255,0,0]
AGENTSIZE = 9
AGENTSICKNESS = 2
WALLSFILE = "walls.csv"
ZOOMFACTOR = 6

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
#agentFeatures = []
#for line in open("pedTest.txt"):
#    coords = line.split(',')
#    agentFeature = []
#    agentFeature.append(float(coords[0]))
#    agentFeature.append(float(coords[1]))
#    agentFeature.append(float(coords[2]))
#    agentFeature.append(float(coords[3]))
#    agentFeatures.append(agentFeature)

#agents = []
#for agentFeature in agentFeatures:
#    agent = Pedestrian()
#    agent.pos = np.array([agentFeature[0], agentFeature[1]])
#    agent.dest = np.array([agentFeature[2], agentFeature[3]])
#    agents.append(agent)


walls = [[3.33, 3.33, 23.97, 3.33],
[3.33, 3.33, 3.33, 30.31],
[3.33, 30.31, 23.97, 30.31]]
#[23.31, 3.33, 33.31, 10.02],
#[33.31, 16.92, 23.31, 23.31]]

print(walls)


# Initialize Desired Interpersonal Distance, A Matrix and B Matrix

DFactor_Init = np.array(
[[0.0, 1.3, 1.2, 1.3, 1.6, 1.0],
[1.8, 0.0, 1.3, 1.6, 1.0, 1.2],
[1.6, 1.3, 0.0, 1.3, 1.3, 1.3],
[1.3, 0.6, 1.3, 0.0, 1.7, 1.1],
[1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
[1.0, 1.2, 0.3, 2.1, 1.8, 0.0]])

AFactor_Init = np.array(
[[0.0, 11.3, 11.9, 1.3, 1.6, 1.0],
[1.3, 0.0, 0.3, 1.6, 1.0, 1.2],
[1.9, 0.3, 0.0, 1.3, 1.3, 1.3],
[1.3, 1.6, 1.3, 0.0, 1.7, 1.1],
[1.6, 1.0, 1.3, 1.7, 0.0, 1.8],
[1.0, 1.2, 1.2, 2.1, 1.8, 0.0]])

BFactor_Init = np.array(
[[0.0, 8.3, 12.9, 2.3, 2.6, 1.0],
[0.3, 0.0, 3.3, 1.6, 3.0, 1.2],
[0.9, 0.3, 0.0, 1.3, 1.3, 1.3],
[1.3, 18.6, 1.3, 0.0, 1.7, 1.1],
[1.6, 1.0, 1.3, 12.7, 0.0, 1.8],
[1.0, 1.2, 18.8, 2.1, 1.8, 0.0]])


DFactor = DFactor_Init
AFactor = AFactor_Init
BFactor = BFactor_Init

v0 = []
v1 = []
v2 = []

vd0 = []
vd1 = []
vd2 = []

range02 = []
d02 = []

# initialize agents
agents = []
for n in range(AGENTSNUM):
    agent = Pedestrian()
    agents.append(agent)


agents[0].changeAttr(32, 22, 0.2, 0.1)
agents[0].desiredSpeed = 0.6
agents[0].p = 0.3

agents[1].pos = np.array([60, 8])
agents[1].actualV = np.array([1.6,1.6])
agents[1].dest = np.array([20.0,10.0])
agents[1].desiredSpeed = 1.8
#agents[1].desiredV = agents[1].desiredSpeed*agents[1].direction
agents[1].p = 0.1

agents[2].pos = np.array([65, 18])
agents[2].actualV = np.array([1.6,1.6])
agents[2].dest = np.array([20.0,18.0])
#agents[2].desiredSpeed = 1.8
#agents[2].desiredV = agents[2].desiredSpeed*agents[2].direction
agents[2].p = 0.2


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
        startPx = startPos*ZOOMFACTOR
        endPx = endPos*ZOOMFACTOR
        pygame.draw.line(screen, LINECOLOR,startPx,endPx)


    for idai,ai in enumerate(agents):
        # 初始速度和位置
        ai.direction = normalize(ai.dest - ai.pos)
        ai.desiredV = ai.desiredSpeed*ai.direction
        # Compute forces on agents
        #adapt = ai.adaptVel()
        peopleInter = 0.0
        wallInter = 0.0
        otherMovingDir = np.array([0.0, 0.0])
        otherMovingSpeed = 0.0
        otherMovingNum = 0
        otherDest = 0

        for idaj,aj in enumerate(agents):
             if idai == idaj:
                 continue
             peopleInter += ai.peopleInteraction(aj, DFactor[idai, idaj], AFactor[idai, idaj], BFactor[idai, idaj])

             rij = ai.radius + aj.radius
             dij = np.linalg.norm(ai.pos - aj.pos)
             dij_dest = np.linalg.norm(ai.dest - aj.dest)
             vij_desiredV = np.linalg.norm(ai.desiredV - aj.desiredV)

             if dij < ai.B*BFactor[idai, idaj] + rij*DFactor[idai, idaj]:
                #ai.interactionRange:
                otherMovingDir += normalize(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
                otherMovingSpeed += np.linalg.norm(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
                otherMovingNum += 1

                #DFactor[idai, idaj] = ai.p*DFactor[idai, idaj]+(1-ai.p)*DFactor[idaj, idai]

                #AFactor[idai, idaj] = ai.p*AFactor[idai, idaj]+(1-ai.p)*AFactor[idaj, idai]

                #BFactor[idai, idaj] = ai.p*BFactor[idai, idaj]+(1-ai.p)*BFactor[idaj, idai]

                #ai.acclTime = ai.p*ai.acclTime + (1-ai.p)*aj.acclTime

                if vij_desiredV < 6:
                    temp = -1/DFactor[idai, idaj]

                else:
                    temp = 1/DFactor[idai, idaj]

                #otherDest += temp


        if otherMovingNum > 0:
            ai.direction = (1-ai.p)*ai.direction + ai.p*otherMovingDir
            ai.desiredSpeed = (1-ai.p)*ai.desiredSpeed + ai.p*otherMovingSpeed/otherMovingNum
            ai.desiredV = ai.desiredSpeed*ai.direction

        #ai.desiredV = ai.p*ai.desiredV + (1-ai.p)*otherMovingDir

        if idai == 0:
            v0.append(np.linalg.norm(ai.actualV))
            vd0.append(ai.desiredSpeed)
        if idai == 1:
            v1.append(np.linalg.norm(ai.actualV))
            vd1.append(ai.desiredSpeed)
        if idai == 2:
            v2.append(np.linalg.norm(ai.actualV))
            vd2.append(ai.desiredSpeed)

        if idai == 0 and idaj == 2:
            range02.append(ai.interactionRange)
            d02.append(dij)

        adapt = ai.adaptVel()

        for wall in walls:
            wallInter += ai.wallInteraction(wall)

        #print('Forces from Walls:', wallInter)
        #print('Forces from people:', peopleInter)

        sumForce = adapt + peopleInter + wallInter
        # Compute acceleration
        accl = sumForce/ai.mass
        # Compute velocity
        ai.actualV = ai.actualV + accl*0.2 # consider dt = 0.5

        #temp = ai.actualV + accl*0.5
        #if np.sqrt(np.dot(temp,temp)) < 2:
        #    ai.actualV = ai.actualV + accl*0.5 # consider dt = 0.5

        # Calculate position
        ai.pos = ai.pos + ai.actualV*0.2
        #print(ai.pos)
        #print(accl,ai.actualV,ai.pos)

        # Buffer or Memory Effect
        ai.actualV_old = ai.actualV
        ai.desiredV_old = ai.desiredV


    for agent in agents:
        scPos = [0, 0]
        scPos[0] = int(agent.pos[0]*ZOOMFACTOR)
        scPos[1] = int(agent.pos[1]*ZOOMFACTOR)

        endPosV = [0, 0]
        endPosV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.actualV[0]*ZOOMFACTOR)
        endPosV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.actualV[1]*ZOOMFACTOR)

        endPosDV = [0, 0]
        endPosDV[0] = int(agent.pos[0]*ZOOMFACTOR + agent.desiredV[0]*ZOOMFACTOR)
        endPosDV[1] = int(agent.pos[1]*ZOOMFACTOR + agent.desiredV[1]*ZOOMFACTOR)

        #AGENTSIZE = int(agent.radius)
        pygame.draw.circle(screen, AGENTCOLOR, scPos, AGENTSIZE, AGENTSICKNESS)
        pygame.draw.line(screen, AGENTCOLOR, scPos, endPosV, 2)
        pygame.draw.line(screen, [255,60,0], scPos, endPosDV, 2)

        #print(scPos)

    pygame.display.flip()
    clock.tick(20)

#print('v0:', vd0)
#print('v1:', vd1)
#print('v2:', vd2)

np.save("vd0.npy",vd0)
np.save("vd1.npy",vd1)
np.save("vd2.npy",vd2)

np.save("v0.npy",v0)
np.save("v1.npy",v1)
np.save("v2.npy",v2)

#plt.figure('data')
plt.plot(vd0)
plt.plot(vd1)
plt.plot(vd2)
#plt.plot(d02)

#plt.subplot(121, vd0)
#plt.subplot(121, vd1)
#plt.subplot(121, vd2)

#plt.subplot(122, v0)
#plt.subplot(122, v1)
#plt.subplot(122, v2)

plt.show()
