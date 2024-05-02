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
    

def GetIntersectPointofLines(p1, p2, p3, p4):
    # from http://www.cnblogs.com/DHUtoBUAA/
    A1,B1,C1=GeneralEquation(p1[0], p1[1], p2[0], p2[1])
    A2,B2,C2 = GeneralEquation(p3[0], p3[1], p4[0], p4[1])
    m=A1*B2-A2*B1
    if m==0:
        print("无交点")
        return None
    else:
        x=(C2*B1-C1*B2)/m
        y=(C1*A2-C2*A1)/m
        #print '有交点', [x, y]
        return [x, y]


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

	
def lineIntersection(p1, p2, w1, w2, fuzP=0.0, fuzW=0.0): #wall):
    #p1 = self.pos
    #p2 = other.pos
    #w1 = np.array([wall.params[0],wall.params[1]])
    #w2 = np.array([wall.params[2],wall.params[3]])
    
    result = None #np.array([0.0,0.0])
    if max(p1[0], p2[0])<min(w1[0], w2[0]) or min(p1[0], p2[0])>max(w1[0], w2[0]):
        flag = False
        return result, flag
         
    if max(p1[1], p2[1])<min(w1[1], w2[1]) or min(p1[1], p2[1])>max(w1[1], w2[1]):
        flag = False
        return result, flag
    
    #result = np.array([0.0,0.0])
    result = GetIntersectPointofLines(p1, p2, w1, w2)
    #result = crossPoint(p1, p2, w1, w2)
    if result == None:
        flag = False
        return result, flag
    
    logic1 = np.dot(result-w1, result-w2)
    logic2 = np.dot(result-p1, result-p2)
    
    # flag is True if there is a wall in between.  
    # otherwise it is false. 
    flag = True
    
    if logic1>0.0 and min(np.linalg.norm(result-w1), np.linalg.norm(result-w2))>=fuzW:
        flag = False
        result = None

    if logic2>0.0: #and min(np.linalg.norm(result-p1), np.linalg.norm(result-p2))>=fuzP:
        flag = False
        result = None
    
    return result, flag


# 计算点到线段的距离，并计算由点到与线段交点的单位向量
#def distanceP2W(point, wall):
    #p0 = np.array([wall[0],wall[1]])
    #p1 = np.array([wall[2],wall[3]])


def distanceP2L(point, p0, p1):
    d = p1-p0
    ymp0 = point-p0
    ymp1 = point-p1
    dist1 = np.linalg.norm(p0-point)
    dist2 = np.linalg.norm(p1-point)
    
    if np.allclose(np.dot(d,d), np.zeros(2)):
    #if np.linalg.norm(d)<1.0:
    #if np.linalg.norm(d)/min(dist1, dist2)<1.0:
        
        if dist1<dist2:
            npw = normalize(p0-point)
            dist = dist1
        else:
            npw = normalize(p1-point)
            dist = dist2
        return dist, npw
    
    t = np.dot(d,ymp0)/np.dot(d,d)
    if t <= 0.0:
        dist = np.sqrt(np.dot(ymp0,ymp0))
        #cross = p0 + t*d
        cross = p0
    elif t >= 1.0:
        #ymp1 = point-p1
        dist = np.sqrt(np.dot(ymp1,ymp1))
        #cross = p0 + t*d
        cross = p1
    else:
        cross = p0 + t*d
        dist = np.linalg.norm(cross-point)
    npw = normalize(cross-point)
    return dist, npw


if __name__ == '__main__':
    # v1 = np.array([3.33,3.33])
    # print(worldCoord2ScreenCoord(v1, [1000,800],30))
    # v2 = np.array([23.31,3.33])
    # print(worldCoord2ScreenCoord(v2,[1000,800] ,30))
    # v3 = np.array([29.97,23.31])
    # print(worldCoord2ScreenCoord(v3, [1000,800],30))
    wall = [3.33, 3.33, 29.97, 3.33]
    w1 = np.array([wall[0], wall[1]])
    w2 = np.array([wall[2], wall[3]])
    print(distanceP2L(np.array([10.0,10.0]), w1, w2))
    # print distanceP2W(np.array([0.5,2.0]),wall)
    # print distanceP2W(np.array([2.0,2.0]),wall)
    
