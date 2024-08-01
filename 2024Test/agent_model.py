# -*-coding:utf-8-*-
# Author: WP and SS
# Email: wp2204@gmail.com


import numpy as np
from math_func import *
from math import *
import random
#from stack import *

class Agent(object):
    def __init__(self, x=1, y=1):
        # random initialize a agent
        
        #self.memory = np.array([0.0, 0.0], [0.0, 0.0], [0.0, 0.0])
        #self.sumAdapt = np.array([0.0, 0.0])
        self.ID = 0 #Name or index of agents
        self.inComp = 1
        self.aType = 'MoveToDest'  #{'MoveToDest' 'Follow' 'Talk' 'Search'}

        self.tpre = random.uniform(6.0,22.0)
        self.maxSpeed = random.uniform(1.0,2.0)
        self.diss = random.uniform(-1.0,0.0)
        
        self.posX_init = random.uniform(8,24)
        self.posY_init = random.uniform(8,18)
        self.pos = np.array([self.posX_init, self.posY_init])	
        #self.pos = np.array([10.0, 10.0])

        self.actualVX_init = random.uniform(0,1.6)
        self.actualVY_init = random.uniform(0,1.6)
        self.actualV = np.array([self.actualVX_init, self.actualVY_init])
        self.actualSpeed = np.linalg.norm(self.actualV) #np.array([0.0, 0.0])

        self.dest = np.array([60.0,10.0])
        self.direction = normalize(self.dest - self.pos)
        #self.direction = np.array([0.0, 0.0])

        self.knowndoor = []
        self.others = []
        self.destmemory = []
        self.destmemory.append(self.dest)
        
        self.desiredSpeed = 2.0 #random.uniform(0.3,2.3) #1.8
        self.desiredV = self.desiredSpeed*self.direction
        self.desiredSpeedMode = 'random' #{'random' 'fixed' 'increase' 'decrease'}
        
        self.tau = random.uniform(8,16) #10.0
        self.drivenAcc =(self.desiredV - self.actualV)/self.tau
              
        self.mass = 60 #random.uniform(40,90) #60.0
        self.radius = 0.35 #1.6 #0.3

        self.interactionRange = 3.0 #Distance for communication (talking)
        self.p = 0.2
        self.pMode = 'random' #{'random' 'fixed' 'increase' 'decrease'}
        
        self.bodyFactorA = 12.0
        self.slideFricFactorA = 240000

        # Cohesive Force
        self.A_CF = 1 #30/20000 #2
        self.B_CF = 1 #random.uniform(0.8,1.6) #0.8 #0.08

        # Social Force
        self.A_SF = 200 #2
        self.B_SF = 0.8 #random.uniform(0.8,1.6) #0.8 #0.08

        # Wall Force
        self.A_WF = 60 #200 #60 #2
        self.B_WF = 3.2 #0.2 #0.8 #3.2 #2.2 #random.uniform(0.8,1.6) #0.08
        
        self.bodyFactorW = 12.0
        self.slideFricFactorW = 240000

        self.Goal = 0
        self.timeOut = 0.0

        self.desiredV_old = np.array([0.0, 0.0])
        self.actualV_old = np.array([0.0, 0.0])

        self.lamb = random.uniform(0.2,0.4)
    
        self.diw_desired = 0.2

        self.ratioV = 1
        self.stressLevel = 1

        self.color = [255, 0, 0] #blue

        self.moving_tau = 0.7
        self.tpre_tau = 1.6
        self.talk_tau = 2.6
        self.talk_prob = 0.6
        
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
    
    def shoulders(self):
        if np.allclose(self.actualV, np.zeros(2)):
            direction = self.direction
            direction = normalize(direction)
        else: 
            direction = np.array([-self.actualV[1], self.actualV[0]])
            direction = normalize(direction)

        leftPx = self.pos + self.radius*direction
        rightPx = self.pos - self.radius*direction	
        return leftPx, rightPx
        

    def adaptDirection(self):
        self.direction = normalize(self.destmemeory[-1]-self.pos)
        if np.allclose(self.direction, np.zeros(2)):
            self.direction = np.zeros(2)
        return self.direction

    def adaptVel(self):
        deltaV = self.desiredV - self.actualV
        if np.allclose(deltaV, np.zeros(2)):
            deltaV = np.zeros(2)
        return deltaV*self.mass/self.tau


    def adaptP(self, flag = 'random'):
        if flag == 'random':
            self.p = self.p + random.uniform(-0.3, 0.3)
            self.p = max(-1.0, min(1.0, self.p))
        elif flag == 'increase' and self.p<1.0:
            # Use randome walk or not ???
            self.p = self.p + random.uniform(0.0, 0.3)
            self.p = min(1.0, self.p)
        elif flag == 'decrease' and self.p>-1.0:
            self.p = self.p + random.uniform(-0.3, 0.0)
            self.p = max(-1.0, self.p)
        return None

    def adaptDesiredSpeed(self, flag = 'random'):
        if flag == 'random':
            self.desiredSpeed = self.desiredSpeed + random.uniform(-0.3, 0.3)
            self.desiredSpeed = max(0.0, min(3.0, self.desiredSpeed))
        elif flag == 'increase' and self.desiredSpeed<3.0:
            self.desiredSpeed = self.desiredSpeed + random.uniform(0.0, 0.3)
            self.desiredSpeed = min(3.0, self.desiredSpeed)
        elif flag == 'decrease' and self.desiredSpeed>0.0:
            self.desiredSpeed = self.desiredSpeed + random.uniform(-0.3, 0.0)
            self.desiredSpeed = max(0.0, self.desiredSpeed)
        return None

    def selfRepulsion(self, Dfactor=1, Afactor=1, Bfactor=1):
        first = -self.direction*Afactor*self.A_CF*np.exp((self.radius*Dfactor)/(self.B_CF*Bfactor))*(self.radius*Dfactor)
        return first

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
        

    def cohesiveForce(self, other, Dfactor=1, Afactor=1, Bfactor=1):

        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        #phiij = vectorAngleCos(self.actualV , (other.pos - self.pos))
        #anisoF = self.lamb + (1-self.lamb)*(1+cos(phiij))/2

        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = Afactor*self.A_CF*np.exp((rij*Dfactor-dij)/(self.B_CF*Bfactor))*nij*(rij*Dfactor-dij) #*anisoF
        return first

    def agentForce(self, other):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = self.A_SF*np.exp((rij-dij)/self.B_SF)*nij
        second = self.bodyFactorA*ggg(rij-dij)*nij

        #Issue: nij is a vector directing from j to i.  
        #*(rij*Dfactor-dij)/20000+ self.bodyFactor*g(rij-dij)*nij/10000
        tij = np.array([-nij[1],nij[0]])
        deltaVij = (self.actualV - other.actualV)*tij
        third = self.slideFricFactorA*ggg(rij-dij)*deltaVij*tij
        #third = 300*exp(rij-dij)*deltaVij*tij/dij

        return first + second #+ third

    ############################
    # This is not used any more.  
    def physicalForce(self, other):
        rij = self.radius + other.radius
        dij = np.linalg.norm(self.pos - other.pos)
        nij = (self.pos - other.pos)/dij
        first = self.bodyFactorA*g(rij-dij)*nij
        #print >> f, "first:", first, "/n"

        return first
    # This is not used any more. 
    ############################


    def wallForce(self, wall):
        
        #ftest = open("wallForceTest.txt", "w+")
        ri = self.radius
        p0 = np.array([wall.params[0],wall.params[1]])
        p1 = np.array([wall.params[2],wall.params[3]])
        diw,niw = distanceP2L(self.pos, p0, p1)
        first = -self.A_WF*np.exp((self.diw_desired-diw)/self.B_WF)*niw
        second = -600*exp((2*ri-diw)/0.2)*niw
        #second = -self.bodyFactorW*ggg(2*ri-diw)*niw*200000
        #Issue: the diretion of niw is from the agent to the wall.  Check Needed!
        #ftest.write('first:', first, '\n')

        tiw = np.array([-niw[1],niw[0]])
        third = self.slideFricFactorW*ggg(ri-diw)*(self.actualV*tiw)*tiw/1000
        #ftest.write('second:', second, '\n')
        #ftest.close()
        return first + second + third


    def wallOnRoute(self, wall, mode=1.0, lookhead=3.0):
        p1 = self.pos
        p2 = self.pos + (mode*self.desiredV+(1-mode)*self.actualV)*lookhead
        
        #if mode=="dv":
        #    p2 = self.pos + self.desiredV*3.0
        #elif mode=="av":
        #    p2 = self.pos + self.actualV
        #else:
        #    print 'Error: mode must be either "dv" or "av"!'
        #    return
        
        
        # The time interval to look ahead is an important issue
        # It is a major issue to use whether actualV or desiredV
        w1 = np.array([wall.params[0],wall.params[1]])
        w2 = np.array([wall.params[2],wall.params[3]])
        
        result = None #np.array([0.0,0.0])
        dist = None
        if (max(p1[0], p2[0])<min(w1[0], w2[0])) or (min(p1[0], p2[0])>max(w1[0], w2[0])):
            #flag = False
            return dist
             
        if (max(p1[1], p2[1])<min(w1[1], w2[1])) or (min(p1[1], p2[1])>max(w1[1], w2[1])):
            #flag = False
            return dist
            
        result = crossPoint(p1, p2, w1, w2)
        
        #result = np.array([x,y])
        logic1 = np.dot(result-w1, result-w2)
        logic2 = np.dot(p1-p2, p1-result)
        
        fuzzyPara = random.uniform(0.0,2.0)
        # flag is true if there is a wall ahead
        # otherwise it is false
        #flag = True
        dist = np.linalg.norm(self.pos - result)
        
        if logic1>0.0 and min(np.linalg.norm(result-w1), np.linalg.norm(result-w2))>fuzzyPara:
                #flag = False
            dist = None
            
        if logic2<0.0:
                #flag = False
            dist = None
            
        return dist
        
        
    def wallInBetween(self, other, wall):
        p1 = self.pos
        p2 = other.pos
        w1 = np.array([wall.params[0],wall.params[1]])
        w2 = np.array([wall.params[2],wall.params[3]])
        
        result = None #np.array([0.0,0.0])
        if (max(p1[0], p2[0])<min(w1[0], w2[0])) or (min(p1[0], p2[0])>max(w1[0], w2[0])):
            flag = False
            return result, flag
             
        if (max(p1[1], p2[1])<min(w1[1], w2[1])) or (min(p1[1], p2[1])>max(w1[1], w2[1])):
            flag = False
            return result, flag
        
        #result = np.array([0.0,0.0])
        result = crossPoint(p1, p2, w1, w2)
        logic1 = np.dot(result-w1, result-w2)
        logic2 = np.dot(result-p1, result-p2)
        
        # flag is True if there is a wall in between.  
        # otherwise it is false. 
        flag = True
        
        if logic1>0.0:
            flag = False
            result = None
            
        if logic2>0.0:
            flag = False
            result = None
            
        return result, flag

    #####################################
    # how an agent interacts with others
    #####################################
     
    def opinionDynamics(self):
        # self.D = DMatrix(selfID, otherID)
        # self.A = AMatrix(selfID, otherID)
        # self.B = BMatrix(selfID, otherID)
        # dij = np.linalg.norm(self.pos - other.pos)
        
        otherMovingDir = np.array([0.0, 0.0])
        otherMovingSpeed = 0.0
        otherMovingNum = 0
    
        for idaj, aj in enumerate(self.others):
            otherMovingDir += normalize(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
            otherMovingSpeed += np.linalg.norm(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
            otherMovingNum += 1
        
            #otherMovingDir += normalize(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
            #otherMovingSpeed += np.linalg.norm(aj.actualV) #/DFactor[idai, idaj]*AFactor[idai, idaj]
        
        #nij = (self.pos - other.pos)/dij
            
            #if dij < self.interactionRange:
        #    self.dest = self.p*self.dest + (1-self.p)*other.dest
        
        #otherDirection = np.array([0.0, 0.0])
        #otherSpeed = 0.0
        #num = 0
        #otherV = np.array([0.0, 0.0])
        
            #if dij < self.interactionRange:
            #self.desiredV = self.p*self.desiredV + (1-self.p)*other.actualV
            #otherDirection = normalize(other.actualV)
            #otherSpeed = np.linalg.norm(other.actualV)
            #num = 1
            #otherV = other.actualV
    
        return otherMovingDir, otherMovingSpeed/otherMovingNum
        
    
if __name__ == '__main__':
    Ped1 = Agent()
    Ped2 = Agent()
    f1 = Ped1.cohesiveForce(Ped2)
    f2 = Ped2.cohesiveForce(Ped1)
    g1 = Ped1.opinionDynamics(Ped2)[0]
    g2 = Ped2.opinionDynamics(Ped1)[2]
    print('----------Testing starts here--------')
    print('Other Opinion', g1)
    print('Other Opinion', g2)
    Ped1.showAttr()
    Ped1.showAttr()
    v = Ped1.adaptVel
    Ped1.changeAttr(1,1)
    Ped2.changeAttr(2,2)

