#-*-encoding:utf-8-*-

"""
从code_face得到的bbox.txt文件，得到code_point中需要使用的bbox.txt文件.

遍历输入图片的目录，得到所有图片的相对路径列表，存入imagelist.txt。
os.walk(path),遍历path，返回一个对象，
他的每个部分都是一个三元组,
('目录x'，[目录x下的目录list]，目录x下面的文件)
"""

import os
import string
import sys
import os.path as osp

trainRootSet = osp.join(os.getcwd(),sys.argv[1])
valRootSet = osp.join(os.getcwd(),sys.argv[2])

def getTraintxtandValtxt():
    # trainRootSet=r'F:\code_point\processCASIA\CASIAintolabels'
    # valRootSet=r'F:\code_point\processCASIA\CASIAtoCaffe\valSET'
    partpath=trainRootSet         #E:/teamPro/DeepID/lmdb/allpart60/part10
    partTrainSet=trainRootSet  #E:/teamPro/DeepID/lmdb/allpart60/part10/trainSET
    partValSet=valRootSet
    tlabels=os.listdir(partTrainSet)
    vlabels=os.listdir(partValSet)
    traintxtpath="%s%s"%(partpath,'/train.txt')
    valtxtpath="%s%s"%(partpath,'/val.txt')
    traintxt=open(traintxtpath,'w')       #E:/teamPro/DeepID/lmdb/allpart60/part10/train.txt
    valtxt=open(valtxtpath,'w')           #E:/teamPro/DeepID/lmdb/allpart60/part10/val.txt
    for i_tl in tlabels:     #i_tl likes 0,1,2...n-1
        labelDir=os.path.join(partTrainSet,i_tl)
        pics=os.listdir(labelDir)
        for i_pic in pics:
            linestr="%s/%s%s%s%s"%(i_tl,i_pic,' ',i_tl,'\n')
            linestr = "CASIA_img/"+linestr
            traintxt.write(linestr)
    traintxt.close()

    for i_vl in vlabels:     #i_vl likes 0,1,2...n-1
        labelDir=os.path.join(partValSet,i_vl)
        pics=os.listdir(labelDir)
        for i_pic in pics:
            linestr="%s/%s%s%s%s"%(i_vl, i_pic, ' ',i_vl,'\n')
            linestr = "CASIA_img/"+linestr
            valtxt.write(linestr)
    valtxt.close()

getTraintxtandValtxt()

