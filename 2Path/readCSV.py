
# -*-coding:utf-8-*-
# Author: WP
# Email: wp2204@126.com

import numpy as np
import csv

def readCSV(fileName, mode='float'):
    
    # read .csv file
    csvFile = open(fileName, "r")
    reader = csv.reader(csvFile)  # 返回的是迭代类型
    strData = []
    for item in reader:
        #print(item)
        strData.append(item)

    print(strData)
    print('np.shape(strData)=', np.shape(strData))
    print('\n')
    
    dataNP = np.array(strData)
    print(dataNP)
    print('np.shape(dataNP)', np.shape(dataNP))
    print('\n')

    #print(strData[1:,1:])
    csvFile.close()	
    
    if mode=='string':
        print(dataNP[1:, 1:])
        return dataNP[1:, 1:]

    if mode=='float':
        print(dataNP[1:, 1:])
        (I, J) = np.shape(dataNP)
        print("The size of tha above matrix:", [I, J])
        #print("The effective data size:", [I-1, J-1])

        matrix = np.zeros((I, J))
        #print matrix

        for i in range(1,I):
            for j in range(1,J):
                matrix[i,j] = float(dataNP[i,j])

    print(matrix[1:, 1:])
    return matrix[1:, 1:]
    

if __name__ == '__main__':
    test = readCSV("Agent_Data2018.csv", 'string')
    
    
