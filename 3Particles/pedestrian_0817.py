# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@126.com

import numpy as np
import random

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm

def g(x):
    if x>=0:
        return x
    else:
        return 0

def vectorAngleCos(x,y):
    if (len(x) != len(y)):
        print('error input,x and y is not in the same dimension')
        return
    angleCos = np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
    angle = np.arccos(angleCos)
    return angle


# 计算点到线段的距离，并计算由点到与线段交点的单位向量
# Calculate the distance from a point to a line segment
# Calculate the unit vector directing from the point to the line segment
def distanceP2W(point, wall):
    p0 = np.array([wall[0],wall[1]])
    p1 = np.array([wall[2],wall[3]])
    d = p1-p0
    ymp0 = point-p0
    ymp1 = point-p1
    t = np.dot(d,ymp0)/np.dot(d,d)
    if t <= 0.0:
        dist = np.sqrt(np.dot(ymp0,ymp0))
        cross = p0 + t*d
    elif t >= 1.0:
        #ymp1 = point-p1
        dist = np.sqrt(np.dot(ymp1,ymp1))
        cross = p0 + t*d
    else:
        cross = p0 + t*d
        dist = np.linalg.norm(cross-point)
    npw = normalize(cross-point)
    return dist,npw


class Pedestrian(object):
    def __init__(self, x=1, y=1):
        # random initialize a agent

        self.posX = random.uniform(8,24)
        self.posY = random.uniform(8,18)
        self.pos = np.array([self.posX, self.posY])

        self.actualVX = 0.0 #random.uniform(0,1.6)
        self.actualVY = 0.0 #random.uniform(0,1.6)
        self.actualV = np.array([self.actualVX, self.actualVY])
        #self.actualV = np.array([0.0, 0.0])

        self.dest = np.array([60.0,10.0])
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])

        self.desiredSpeed = 0.0 #random.uniform(0.3,2.3) #1.8
        self.desiredV = self.desiredSpeed*self.direction

        self.acclTime = 2 #random.uniform(8,16) #10.0
        self.drivenAcc =(self.desiredV - self.actualV)/self.acclTime

        self.mass = 60 #random.uniform(40,90) #60.0
        self.radius = 0.35
        self.interactionRange = 1.2
        self.p = 0.1

        self.wallrepF= np.array([0.0,0.0])
        self.groupF= np.array([0.0,0.0])
        self.selfrepF= np.array([0.0,0.0])

        self.bodyFactor = 120000
        self.slideFricFactor = 240000
        self.A = 2
        self.B = 0.6 #random.uniform(0.8,1.6) #0.8 #0.08

        self.desiredV_old = np.array([0.0, 0.0])
        self.actualV_old = np.array([0.0, 0.0])

        self.Goal = 0
        self.timeOut = 0.0

        print('X and Y Position:', self.pos)
        print('Actual Velocity:', self.actualV)
        print('self.direction:', self.direction)



    # def step(self):
    #     # 初始速度和位置
    #     v0 = self.actualV
    #     r0 = self.pos
    #     self.direction = normalize(self.dest - self.pos)
    #     # 计算受力
    #     adapt = self.adaptVel()
    #     peopleInter = self.peopleInteraction()
    #     wallInter = self.wallInteraction()
    #     sumForce = adapt + peopleInter + wallInter
    #     # 计算加速度
    #     accl = sumForce/self.mass
    #     # 计算速度
    #     self.actualV = v0 + accl # consider dt = 1
    #     # 计算位移
    #     self.pos = r0 + v0 + 0.5*accl
    #     print(accl,self.actualV,self.pos)



    def adaptVel(self):
        deltaV = self.desiredV - self.actualV
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)
        return deltaV*self.mass/self.acclTime


    def selfRepulsion(self, Dfactor=1, Afactor=1, Bfactor=1):
        first = -self.direction*Afactor*self.A*np.exp((self.radius*Dfactor)/(self.B*Bfactor))*(self.radius*Dfactor)
        return first


    def changeAttr(self, x=1, y=1, Vx=1, Vy=1):
        self.posX = x
        self.posY = y
        self.pos = np.array([self.posX, self.posY])
        self.actualVX = Vx
        self.actualVY = Vy
        self.actualV = np.array([self.actualVX, self.actualVY])


    def showAttr(self):
        print('X and Y Position:', self.pos)
        print('The destination', self.dest)



    def peopleInteraction(self, other, Dfactor=1, Afactor=1, Bfactor=1):
        rij = self.radius + other.radius
        # rij = desiredDistance(selfID, otherID)
        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = Afactor*self.A*np.exp((rij*Dfactor-dij)/(self.B*Bfactor))*nij*(rij*Dfactor-dij)
        + self.bodyFactor*g(rij-dij)*nij
        #tij = np.array([-nij[1],nij[0]])
        #deltaVij = (self.actualV - other.actualV)*tij
        #second = self.slideFricFactor*g(rij-dij)*deltaVij*tij
        return first #+ second


    def wallInteraction(self, wall):
        ri = self.radius
        diw,niw = distanceP2W(self.pos,wall)
        first = -self.A*np.exp((ri-diw)/self.B)*niw*2000
        + self.bodyFactor*g(ri-diw)*niw
        #tiw = np.array([-niw[1],niw[0]])
        #second = self.slideFricFactor*g(ri-diw)*(self.actualV*tiw)*tiw
        return first #- second

    def wallOnRoute(self, wall):
        self.pos
        self.actualV
        return true


    def peopleInterOpinion(self, other, Dfactor=1, Afactor=1, Bfactor=1):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        #nij = (self.pos - other.pos)/dij

        #if dij < self.interactionRange:
        #    self.dest = self.p*self.dest + (1-self.p)*other.dest

        otherDirection = np.array([0.0, 0.0])
        otherSpeed = 0.0
        num = 0
        otherV = np.array([0.0, 0.0])

        #if dij < self.B*Bfactor + rij*Dfactor:
        if dij < self.interactionRange:
            #self.desiredV = self.p*self.desiredV + (1-self.p)*other.actualV
            otherDirection = normalize(other.actualV)
            otherSpeed = np.linalg.norm(other.actualV)
            num = 1
            otherV = other.actualV

        return otherDirection, otherSpeed, num, otherV



if __name__ == '__main__':
        Ped1 = Pedestrian()
        Ped2 = Pedestrian()
        f1 = Ped1.peopleInteraction(Ped2)
        f2 = Ped2.peopleInteraction(Ped1)
        g1 = Ped1.peopleInterOpinion(Ped2)[0]
        g2 = Ped2.peopleInterOpinion(Ped1)[2]
        print('Other Opinion', g1)
        print('Other Opinion', g2)
        Ped1.showAttr()
        v = Ped1.adaptVel
        Ped1.changeAttr(1,1)
        Ped2.changeAttr(2,2)
