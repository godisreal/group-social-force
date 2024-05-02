
# -*-coding:utf-8-*-
# Author: WP and ??
# Email: wp2204@gmail.com

import numpy as np
from math_func import *
from math import *



class obst(object):
    
    """
    screen: (Not used)
        Obstacles exists on a screen element 
    id:
        obstacle id 
    mode: 
        obstacle type (Line, Rect, Circle)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Line -> [x1,y1,x2,y2]
        Rect -> [x,y,w,h] 
        Circle -> [x,y,r,None]
        """
    
    def __init__(self, oid=0, mode='line', params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.oid = 0
        self.mode = 'line'
        
        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])
        
        self.inComp = 1
        self.arrow = 0
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        self.pointer1 = np.array([0, 0])
        self.pointer2 = np.array([0, 0])


    def direction(self):
        if self.mode=='line':
            direction = np.array([self.params[0], self.params[1]]) -np.array([self.params[2], self.params[3]])
            direction = -normalize(direction)
        elif selfmode=='rect':
            pass


    def wallInBetween(self, p1, p2):

        if self.mode == 'line':
            w1 = np.array([self.params[0],self.params[1]])
            w2 = np.array([self.params[2],self.params[3]])
            result, flag = lineIntersection(p1, p2, w1, w2)
            return result, flag

        elif self.mode == 'rect':
            w1 = np.array([self.params[0],self.params[1]])
            w2 = np.array([self.params[0],self.params[3]])
            result0, flag0 = lineIntersection(p1, p2, w1, w2)
            if flag0==True:
                return  result0, flag0

            w1 = np.array([self.params[2],self.params[1]])
            w2 = np.array([self.params[2],self.params[3]])
            result2, flag2 = lineIntersection(p1, p2, w1, w2)
            if flag2==True:
                return  result2, flag2

            w1 = np.array([self.params[0],self.params[1]])
            w2 = np.array([self.params[2],self.params[1]])
            result1, flag1 = lineIntersection(p1, p2, w1, w2)
            if flag1==True:
                return  result1, flag1

            w1 = np.array([self.params[0],self.params[3]])
            w2 = np.array([self.params[2],self.params[3]])
            result3, flag3 = lineIntersection(p1, p2, w1, w2)
            if flag3==True:
                return  result3, flag3

            result=None
            flag=False
            return result, flag



class passage(object):
    
    """
    screen: (Not used)
        Passages exist on a screen element 
    id:
        door id 
    mode: 
        door type (Rect, Circle)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Rect -> [x,y,w,h] 
        Circle -> [x,y,r,None]
        """
    
    def __init__(self, oid=0, mode='rect', params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.oid = 0
        #self.mode = 'rect' # All the door are in form of rect
        self.exitSign = 0

        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])

        
        self.inComp = 1
        self.arrow = 1
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        #self.pointer1 = np.array([0, 0])
        #self.pointer2 = np.array([0, 0])
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5


    def direction(self):
        ### +1: +x
        ###  -1: -x
        ### +2: +y
        ###  -2: -y 
        if self.arrow == 1:
            direction = -np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            direction = np.array([1.0, 0.0])
        elif self.arrow == -1:
            direction = np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            direction = np.array([-1.0, 0.0])
        elif self.arrow == 2:
            direction = -np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            direction = normalize(direction)
            direction = np.array([0.0, 1.0])
        elif self.arrow == -2:
            direction = np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            direction = normalize(direction)
            direction = np.array([0.0, -1.0])
        return direction
            

    def computePos(self):
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5


    def doorEdge(self):
        if self.arrow == 1 or self.arrow == -1:
            edge1=  0.5*(np.array([self.params[0], self.params[1]]) + np.array([self.params[0], self.params[3]]))
            edge2 = 0.5*(np.array([self.params[2], self.params[1]]) + np.array([self.params[2], self.params[3]]))
            return edge1, edge2
        if self.arrow == 2 or self.arrow == -2:
            edge1= 0.5*(np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[1]]))
            edge2= 0.5*(np.array([self.params[0], self.params[3]]) + np.array([self.params[2], self.params[3]]))
            return edge1, edge2


    def intersecWithLine(self, w1, w2):

        ########################
        ### p1-----------------p4 ###
        ###  |                              |  ###
        ###  |                              |  ###
        ###  |                              |  ###
        ### p3-----------------p2 ###
        ########################
        
        p1 = np.array([self.params[0], self.params[1]])
        p2 = np.array([self.params[2], self.params[3]])
        p3 = np.array([self.params[0], self.params[3]])
        p4 = np.array([self.params[2], self.params[1]])

        #w1 = np.array([wall.params[0],wall.params[1]])
        #w2 = np.array([wall.params[2],wall.params[3]])

        result, flag = lineIntersection(p1, p2, w1, w2)
        return flag

        #if wall.mode == 'line':
            #pass
        #if wall.mode == 'rect':
            #pass
        #return np.array([0.0, 0.0])

        
    def doorForce(self, agent):
        if self.insideDoor(agent.pos)==False:
            doordir = self.direction()
            agentdir = self.pos-agent.pos
            if np.dot(doordir, agentdir)>=0:
                ri = agent.radius
                #mid= (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))/2.0
                dist=np.linalg.norm(self.pos - agent.pos)
                dire = normalize(self.pos-agent.pos)

                first = 1.6*agent.A_WF*np.exp((ri-dist)/agent.B_WF)*dire
                second = 160*exp((2*ri-dist)/1.8)*dire  #0.2)*dire
                return first + second
            else:
                return np.array([0.0, 0.0])
        else:
            if self.arrow == 1 or self.arrow == -1:
                w1= np.array([self.params[0], self.params[1]])
                w2 = np.array([self.params[2], self.params[1]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                first = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                #second = -600*exp((2*ri-diw)/0.2)*niw

                w1= np.array([self.params[0], self.params[3]])
                w2 = np.array([self.params[2], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                second = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                return first + second
            
            if self.arrow == 2 or self.arrow == -2:
                w1= np.array([self.params[0], self.params[1]])
                w2= np.array([self.params[0], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                first = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw

                w1= np.array([self.params[2], self.params[1]])
                w2= np.array([self.params[2], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                second = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                return first + second



    def insideDoor(self, pos):
        if pos[0]>=self.params[0] and pos[0]<=self.params[2]:
            if  pos[1]>=self.params[1] and pos[1]<=self.params[3]:
                return True
        else:
            return False



class outlet(object):
    
    """
    screen: (Not used)
        Passages exist on a screen element 
    id:
        outlet id 
    mode: 
        door type (Rect, Circle)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Rect -> [x,y,w,h] 
        Circle -> [x,y,r,None]
        """
    
    def __init__(self, oid=0, mode='rect', params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.oid = 0
        #self.mode = 'rect' # All the door are in form of rect
        self.exitSign = 1

        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])

        
        self.inComp = 1
        self.arrow = 1
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        #self.pointer1 = np.array([0, 0])
        #self.pointer2 = np.array([0, 0])
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5


    def direction(self):
        ### +1: +x
        ###  -1: -x
        ### +2: +y
        ###  -2: -y 
        if self.arrow == 1:
            direction = -np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            direction = np.array([1.0, 0.0])
        elif self.arrow == -1:
            direction = np.array([self.params[0], self.params[3]]) -np.array([self.params[2], self.params[3]])
            direction = normalize(direction)
            direction = np.array([-1.0, 0.0])
        elif self.arrow == 2:
            direction = -np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            direction = normalize(direction)
            direction = np.array([0.0, 1.0])
        elif self.arrow == -2:
            direction = np.array([self.params[0], self.params[1]]) -np.array([self.params[0], self.params[3]])
            direction = normalize(direction)
            direction = np.array([0.0, -1.0])
        return direction
            

    def computePos(self):
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5


    def doorEdge(self):
        if self.arrow == 1 or self.arrow == -1:
            edge1=  0.5*(np.array([self.params[0], self.params[1]]) + np.array([self.params[0], self.params[3]]))
            edge2 = 0.5*(np.array([self.params[2], self.params[1]]) + np.array([self.params[2], self.params[3]]))
            return edge1, edge2
        if self.arrow == 2 or self.arrow == -2:
            edge1= 0.5*(np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[1]]))
            edge2= 0.5*(np.array([self.params[0], self.params[3]]) + np.array([self.params[2], self.params[3]]))
            return edge1, edge2


    def intersecWithLine(self, w1, w2):

        ########################
        ### p1-----------------p4 ###
        ###  |                              |  ###
        ###  |                              |  ###
        ###  |                              |  ###
        ### p3-----------------p2 ###
        ########################
        
        p1 = np.array([self.params[0], self.params[1]])
        p2 = np.array([self.params[2], self.params[3]])
        p3 = np.array([self.params[0], self.params[3]])
        p4 = np.array([self.params[2], self.params[1]])

        #w1 = np.array([wall.params[0],wall.params[1]])
        #w2 = np.array([wall.params[2],wall.params[3]])

        result, flag = lineIntersection(p1, p2, w1, w2)
        return flag

        #if wall.mode == 'line':
            #pass
        #if wall.mode == 'rect':
            #pass
        #return np.array([0.0, 0.0])

        
    def doorForce(self, agent):
        if self.insideDoor(agent.pos)==False:
            doordir = self.direction()
            agentdir = self.pos-agent.pos
            if np.dot(doordir, agentdir)>=0:
                ri = agent.radius
                #mid= (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))/2.0
                dist=np.linalg.norm(self.pos - agent.pos)
                dire = normalize(self.pos-agent.pos)

                first = 1.6*agent.A_WF*np.exp((ri-dist)/agent.B_WF)*dire
                second = 160*exp((2*ri-dist)/1.8)*dire  #0.2)*dire
                return first + second
            else:
                return np.array([0.0, 0.0])
        else:
            if self.arrow == 1 or self.arrow == -1:
                w1= np.array([self.params[0], self.params[1]])
                w2 = np.array([self.params[2], self.params[1]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                first = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                #second = -600*exp((2*ri-diw)/0.2)*niw

                w1= np.array([self.params[0], self.params[3]])
                w2 = np.array([self.params[2], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                second = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                return first + second
            
            if self.arrow == 2 or self.arrow == -2:
                w1= np.array([self.params[0], self.params[1]])
                w2= np.array([self.params[0], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                first = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw

                w1= np.array([self.params[2], self.params[1]])
                w2= np.array([self.params[2], self.params[3]])
                diw, niw = distanceP2L(agent.pos, w1, w2)
                second = -agent.A_WF*np.exp((agent.diw_desired-diw)/agent.B_WF)*niw
                return first + second



    def insideDoor(self, pos):
        if pos[0]>=self.params[0] and pos[0]<=self.params[2]:
            if  pos[1]>=self.params[1] and pos[1]<=self.params[3]:
                return True
        else:
            return False
            

if __name__ == '__main__':
    doorTest2 = passage()
    doorTest2.params = np.array([60.3, 3.0, 66.0, 6.0])
    doorTest2.arrow = -2
    print(doorTest2.direction())
    print(doorTest2.doorEdge())

    doorTest3 = passage()
    doorTest3.params = np.array([18.9, 16, 23, 20])
    doorTest3.arrow = 1
    print(doorTest3.direction())
    print('Test OK')
