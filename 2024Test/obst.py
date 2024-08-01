
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
    
    def __init__(self, mode='line', params=[0,0,0,0]):

        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.oid = 0
        self.mode = 'line'
        self.name = 'None'
        
        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])
        
        #self.attachedDoors=[]
        #self.isSingleWall = False
        self.inComp = 1
        self.arrow = 0
        #self.exitSign = 0
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        self.pointer1 = np.array([float('NaN'), float('NaN')])
        self.pointer2 = np.array([float('NaN'), float('NaN')])


class passage(object):
    
    """
    screen: (Not used)
        Passages exist on a screen element 
    oid:
        door id 
    mode: 
        door type (Rect, Circle)
    params:
        Obstacle parameters according to the type. This in the form 
        of: Rect -> [x,y,w,h] 
        Circle -> [x,y,r,None]
    """
    
    def __init__(self, oid=0, params=[0,0,0,0]):
        
        self.params = np.array([0.0, 0.0, 0.0, 0.0])
        self.oid = 0
        #self.mode = 'rect' # All the door are in form of rect
        #self.exitSign = 0
        self.mode = 'rect'
        self.name = 'None'

        #self.attachedWalls=[]
        self.inComp = 1
        #self.isSingleDoor = False
        self.arrow = 0 # The default doorway direction: Using nearest-exit strategy 
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        #self.pointer1 = np.array([0, 0])
        #self.pointer2 = np.array([0, 0])
        self.pos = (np.array([self.params[0], self.params[1]]) + np.array([self.params[2], self.params[3]]))*0.5

if __name__ == '__main__':
    obst = obst()
    passage = passage()
    print('Test OK')
