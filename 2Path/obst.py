
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
        
        self.params = np.array([0, 0, 0, 0])
        self.oid = 0
        self.mode = 'line'
        
        #self.startPx = np.array([params[0], params[1]])
        #self.endPx = np.array([params[2], params[3]])
        
        
        self.arrow = 0
        #self.direction = None #self.arrow*normalize(self.endPx - self.startPx)
        self.pointer1 = np.array([0, 0])
        self.pointer2 = np.array([0, 0])


if __name__ == '__main__':
    obst = obst()
    print('Test OK')
