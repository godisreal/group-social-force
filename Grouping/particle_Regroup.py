# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@126.com


import numpy as np
#from tools import *
import random

class Agent(object):
    def __init__(self, x=1, y=1):
        # random initialize a agent
        
        self.posX = random.uniform(8,24)
        self.posY = random.uniform(8,18)
        self.pos = np.array([self.posX, self.posY])	
        #self.pos = np.array([10.0, 10.0])

        self.actualVX = random.uniform(0,1.6)
        self.actualVY = random.uniform(0,1.6)
        self.actualV = np.array([self.actualVX, self.actualVY])
        #self.actualV = np.array([0.0, 0.0])

        self.dest = np.array([60.0,10.0])
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])
        
        self.desiredSpeed = 0.0 #random.uniform(0.3,2.3) #1.8
        self.desiredV = self.desiredSpeed*self.direction
        
        self.acclTime = random.uniform(8,16) #10.0
        self.drivenAcc =(self.desiredV - self.actualV)/self.acclTime
              
        self.mass = 60 #random.uniform(40,90) #60.0
        self.radius = 1.6 #0.3
        self.interactionRange = 3
        self.p = 0.8
        
        self.bodyFactor = 120000
        self.slideFricFactor = 240000
        self.A = 2000
        self.B = 0.8 #random.uniform(0.8,1.6) #0.8 #0.08
        
        print('X and Y Position:', self.pos)
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


    def changeAttr(self, x=1, y=1, Vx=1, Vy=1):
        self.posX = x
        self.posY = y
        self.pos = np.array([self.posX, self.posY])
        self.actualVX = Vx
        self.actualVY = Vy
        self.actualV = np.array([self.actualVX, self.actualVY])


    def showAttr(self):
        #print('test')
        print('X and Y Position:', self.pos)
        print('self.direction:', self.direction)
	print('self.velocity:', self.actualV)
        

    def peopleInteraction(self, other, Dfactor=1, Afactor=1, Bfactor=1):
        rij = self.radius + other.radius
        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = Afactor*self.A*np.exp((rij*Dfactor-dij)/(self.B*Bfactor))*nij*(rij*Dfactor-dij)/20000
        + self.bodyFactor*g(rij-dij)*nij/10000
        #tij = np.array([-nij[1],nij[0]])
        #deltaVij = (self.actualV - other.actualV)*tij
        #second = self.slideFricFactor*g(rij-dij)*deltaVij*tij
        return first #+ second


    def wallInteraction(self, wall):
        ri = self.radius
        diw,niw = distanceP2W(self.pos,wall)
        first = -self.A*np.exp((ri-diw)/self.B)*niw/100
        + self.bodyFactor*g(ri-diw)*niw/10000
        #tiw = np.array([-niw[1],niw[0]])
        #second = self.slideFricFactor*g(ri-diw)*(self.actualV*tiw)*tiw
        return first #- second


    def wallOnRoute(self, wall):
	self.pos
	self.actualV
	return true
		
		
    def peopleInterOpinion(self, other):
        # self.D = DMatrix(selfID, otherID)
        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        dij = np.linalg.norm(self.pos - other.pos)
        
	#nij = (self.pos - other.pos)/dij
        
        #if dij < self.interactionRange:
	#    self.dest = self.p*self.dest + (1-self.p)*other.dest


	otherDirection = np.array([0.0, 0.0])
	otherSpeed = 0.0
	num = 0
	otherV = np.array([0.0, 0.0])

        if dij < self.interactionRange:
	    #self.desiredV = self.p*self.desiredV + (1-self.p)*other.actualV
	    otherDirection = normalize(other.actualV)
	    otherSpeed = np.linalg.norm(other.actualV)
	    num = 1
	    otherV = other.actualV
	
        return otherDirection, otherSpeed, num, otherV
		

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm

def g(x):
    return np.max(x, 0.0)


# 计算点到线段的距离，并计算由点到与线段交点的单位向量
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

        
if __name__ == '__main__':
	Ped1 = Agent()
	Ped2 = Agent()
	f1 = Ped1.peopleInteraction(Ped2)
	f2 = Ped2.peopleInteraction(Ped1)
	g1 = Ped1.peopleInterOpinion(Ped2)[0]
	g2 = Ped2.peopleInterOpinion(Ped1)[2]
	print('----------Testing starts here--------')
	print('Other Opinion', g1)
	print('Other Opinion', g2)
	Ped1.showAttr()
	Ped1.showAttr()
	v = Ped1.adaptVel
	Ped1.changeAttr(1,1)
	Ped2.changeAttr(2,2)



	
