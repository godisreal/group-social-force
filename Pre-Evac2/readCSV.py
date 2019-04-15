
# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@126.com

import numpy as np
import csv

def readCSV(fileName):
    
    # 读取csv文件方式
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)  # 返回的是迭代类型
    someData = []
    for item in reader:
	#print(item)
	someData.append(item)

    print(someData)
    dataNP = np.array(someData)

    #print(someData[1:,1:])
    csvFile.close()	

    [I, J] = np.shape(dataNP)
    print "The size of tha above matrix:", [I, J]

    matrix = np.zeros((I, J))

    for i in range(1,I):
	for j in range(1,J):
	    matrix[i,j]=float(dataNP[i,j])

    print matrix[1:, 1:]
    return matrix[1:, 1:]
    

if __name__ == '__main__':
	test = readCSV("BLD2018.csv")
