# -*-coding:utf-8-*-
# Author: SS and WP
# Email: wp2204@gmail.com

import numpy as np

# 从世界坐标系转换到屏幕坐标，注意传入行向量
def worldCoord2ScreenCoord(worldCoord,screenSize, res):
    wc = np.append(worldCoord,1.0)
    # 要翻转y轴
    mirrorMat = np.matrix([
        [1, 0, 0],
        [0, -1, 0],
        [0, 0, 1]
    ])
    scaleMat = np.matrix([
        [res,0.0,0.0],
        [0.0,res,0.0],
        [0.0,0.0,1.0]
    ])
    transMat = np.matrix([
        [1.0,0.0,0.0],
        [0.0,1.0,0.0],
        [0.0,screenSize[1],1.0]
    ])
    result = wc*scaleMat*mirrorMat*transMat
    return np.array(np.round(result.tolist()[0][:2]),dtype=int)


def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
       return v
    return v/norm

def g(x):
    return np.max(x, 0)
    
def ggg(x):
    if(x>=0.0):
	return x
    else:
	return 0.0

def vectorAngleCos(x,y):
    if (len(x) != len(y)):
	print('error input,x and y is not in the same space')
	return
    
    if np.linalg.norm(x)*np.linalg.norm(y) != 0.0: 
	cosValue = np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
	angle = np.arccos(cosValue)
    else:
	angle = 0.0
    return angle
    
    
def GeneralEquation(first_x,first_y,second_x,second_y):
    # 一般式 Ax+By+C=0
    # from http://www.cnblogs.com/DHUtoBUAA/
    A=second_y-first_y
    B=first_x-second_x
    C=second_x*first_y-first_x*second_y
    return A,B,C
    

def GetIntersectPointofLines(x1,y1,x2,y2,x3,y3,x4,y4):
    # from http://www.cnblogs.com/DHUtoBUAA/
    A1,B1,C1=GeneralEquation(x1,y1,x2,y2)
    A2,B2,C2 = GeneralEquation(x3,y3,x4,y4)
    m=A1*B2-A2*B1
    if m==0:
        print("无交点")
    else:
        x=(C2*B1-C1*B2)/m
        y=(C1*A2-C2*A1)/m
    return x,y


def crossPoint(p1, p2, p3, p4):#计算交点函数
    
    x1=p1[0]#取四点坐标
    y1=p1[1]
    x2=p2[0]
    y2=p2[1]
    
    x3=p3[0]
    y3=p3[1]
    x4=p4[0]
    y4=p4[1]
    
    k1=(y2-y1)*1.0/((x2-x1)*1.0) #计算k1,由于点均为整数，需要进行浮点数转化
    b1=y1*1.0-x1*k1*1.0 #整型转浮点型是关键
    if (x4-x3)==0: #L2直线斜率不存在操作
        k2=None
        b2=0
    else:
        k2=(y4-y3)*1.0/(x4-x3) #斜率存在操作
        b2=y3*1.0-x3*k2*1.0
    if k2==None:
        x=x3
    else:
        x=(b2-b1)*1.0/(k1-k2)
    y=k1*x*1.0+b1*1.0
    return [x, y]



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
    # v1 = np.array([3.33,3.33])
    # print(worldCoord2ScreenCoord(v1, [1000,800],30))
    # v2 = np.array([23.31,3.33])
    # print(worldCoord2ScreenCoord(v2,[1000,800] ,30))
    # v3 = np.array([29.97,23.31])
    # print(worldCoord2ScreenCoord(v3, [1000,800],30))
    wall = [3.33, 3.33, 29.97, 3.33]
    print distanceP2W(np.array([10.0,10.0]),wall)
    # print distanceP2W(np.array([0.5,2.0]),wall)
    # print distanceP2W(np.array([2.0,2.0]),wall)
