
# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@gmail.com

import numpy as np
from math_func import *
from math import *
#from config import *
#import random
#import os
import re
import pygame
import pygame.draw

xSpace=10.0
ySpace=10.0

red=255,0,0
green=0,255,0
blue=0,0,255
white=255,255,255
yellow=255,255,0
IndianRed=205,92,92
tan = 210,180,140
skyblue = 135,206,235
orange = 255,128,0
khaki = 240,230,140


fin = open("Ex2017.fds","r")
fo = open("out.txt", "w+")

filedata = fin.read()
filesize = fin.tell()
#filedata2 = bytearray(filedata)
print filedata
#print >> fo, filedata

fin.close()

#wallFeatures = []
#for line in open("wallTest.txt"):
#    coords = line.split(',')
#    wallFeature = []
#    wallFeature.append(float(coords[0]))
#    wallFeature.append(float(coords[1]))
#    wallFeature.append(float(coords[2]))
#    wallFeature.append(float(coords[3]))
#    wallFeatures.append(wallFeature)

obstFeatures = []
for line in open("Ex2017.fds"):
    if re.match('&OBST', line):

        temp =  line.split('=')
        dataXYZ = temp[1]
        coords = dataXYZ.split(',')
        obstFeature = []
        obstFeature.append(float(coords[0]))
        obstFeature.append(float(coords[1]))
        obstFeature.append(float(coords[2]))
        obstFeature.append(float(coords[3]))
        obstFeatures.append(obstFeature)
	
        print line
        print >>fo, line
        print obstFeature
        print >>fo, obstFeature

	
print >>fo, 'test\n'
print >>fo, 'OBST Features\n'
print >>fo, obstFeatures


holeFeatures = []
for line in open("Ex2017.fds"):
    if re.match('&HOLE', line):
                
        temp =  line.split('=')
        dataXYZ = temp[1]
        coords = dataXYZ.split(',')
        holeFeature = []
        holeFeature.append(float(coords[0]))
        holeFeature.append(float(coords[1]))
        holeFeature.append(float(coords[2]))
        holeFeature.append(float(coords[3]))
        holeFeatures.append(holeFeature)
	
        print line
        print >>fo, line
	
        print holeFeature
        print >>fo, holeFeature

print >>fo, 'test\n'
print >>fo, 'HOLE Features\n'
print >>fo, holeFeatures


zoomfac = 10.0
pygame.init()
screen = pygame.display.set_mode([600,300])
pygame.display.set_caption('Show FDS+Evac 2D Geometry')
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
        # elif event.type == pygame.MOUSEBUTTONUP:
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                zoomfac = zoomfac +1
            elif event.key == pygame.K_PAGEDOWN:
                zoomfac = zoomfac -1
            elif event.key == pygame.K_UP:
                ySpace=ySpace-10
            elif event.key == pygame.K_DOWN:
                ySpace=ySpace+10
            elif event.key == pygame.K_LEFT:
                xSpace=xSpace-10
            elif event.key == pygame.K_RIGHT:
                xSpace=xSpace+10

    screen.fill(white)

    for obstFeature in obstFeatures:
        x= zoomfac*obstFeature[0]
        y= zoomfac*obstFeature[2]
        w= zoomfac*(obstFeature[1] - obstFeature[0])
        h= zoomfac*(obstFeature[3] - obstFeature[2])
	
        pygame.draw.rect(screen, blue, [x+xSpace, y+ySpace, w, h], 2)


    for holeFeature in holeFeatures:
        x= zoomfac*holeFeature[0]
        y= zoomfac*holeFeature[2]
        w= zoomfac*(holeFeature[1] - holeFeature[0])
        h= zoomfac*(holeFeature[3] - holeFeature[2])
	
        pygame.draw.rect(screen, green, [x+xSpace, y+ySpace, w, h], 2)

	
    pygame.display.flip()
    clock.tick(20)


