# -*- coding: utf-8 -*-
import os
import shutil
import string

''''''
'''输入：某一图片集目录，目录下是所有类标号（0，1...n-1）的图片'''
'''输出：另一图片集目录，目录下是(0，1...n-1)命名的文件夹，每个文件夹下是相应类标的图片'''
''''''
def fromone2NDIR():
    Root=r'F:\code_point\processCASIA\CASIA'
    outRoot=r"F:\code_point\processCASIA\CASIAintolabels"
    if(not(os.path.exists(outRoot))):
         os.mkdir(outRoot)
    inputPartSet=Root
    outPartSet=outRoot
    picname = os.listdir(inputPartSet)
    for i in picname:           #picname=0_005121_492ea658462f71d284e09e2580c1dc201ca3f34d.jpg_001.jpg
         picnamesplit=i.split('_')
         label=picnamesplit[0]    #label=0
         if(not(os.path.exists(outPartSet))):
             os.mkdir(outPartSet)
         newDir=os.path.join(outPartSet,label)
         if(not(os.path.exists(newDir))):
             os.mkdir(newDir)
         oldpicpath=os.path.join(inputPartSet,i)
         newpicpath=os.path.join(newDir,i)
         shutil.copy(oldpicpath,newpicpath)
         print i

fromone2NDIR()