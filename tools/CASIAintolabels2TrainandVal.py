# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:06:53 2015
输入：所有的数据集的目录，再以类标号（0，1...n-1）为目录的数据组织形式
输出：创建验证集合的目录，再以类标号（0，1...n-1）为目录的数据组织形式
      遗留的目录中，仍以类标号（0，1...n-1）为目录的数据组织形式，作为训练集合
@author: Administrator
"""

import os
import string
import random
import numpy as np
import shutil
import sys

Root = os.path.join(os.getcwd(),sys.argv[1])
outRoot = os.path.join(os.getcwd(),sys.argv[2])

def allset2TrainandVal():
    # Root=r"F:\code_point\processCASIA\CASIAintolabels" 
    # outRoot=r"F:\code_point\processCASIA\CASIAtoCaffe"
    newDIR=outRoot
    if(not(os.path.exists(newDIR))):
        os.mkdir(newDIR)
    inputPartSet=Root   
    outValPartSet = newDIR    

    foldername = os.listdir(inputPartSet)
    xx=0
    for i in foldername:        
        folder = "%s\%s"%(inputPartSet,i)    

        newfolder = "%s\%s"%(outValPartSet,string.atoi(i)+xx)         

        if(not(os.path.exists(newfolder))):
            os.mkdir(newfolder)
        pics=os.listdir(folder)
        N=len(pics)
        rng_state = np.random.get_state()
        np.random.shuffle(pics)
        for index in range(int(max(1,N*0.05))):
            srcpic="%s\%s"%(folder,pics[index])
            dstvalpic="%s\%s"%(newfolder,pics[index])
            shutil.copy(srcpic,dstvalpic)  #val集合只是train集合的子集，
        print i

allset2TrainandVal()