#!/usr/bin/env python2
#-*-encoding:utf-8-*-

"""
遍历输入图片的目录，得到所有图片的相对路径列表，存入imagelist.txt。
os.walk(path),遍历path，返回一个对象，
他的每个部分都是一个三元组,
('目录x'，[目录x下的目录list]，目录x下面的文件)


功能：将root目录下所有文件夹中的所有图片复制到newroot目录下，并将newroot中的图片的总数和新路径写入imagelist.txt中。
"""

import os
import shutil
import string

#root = r'D:\BaiduYunDownload\WebFace\CASIA-WebFace'
root=r'D:\FACE\lfw-deepfunneled'
#newroot=r'F:\code_face\image'
newroot=r'D:\FACE\lfwimgInonedir'
#fileinfo = open('F:\code_face\imagelist.txt','w')
fileinfo=open('D:\FACE\lfwimglists.txt','w')
if not(os.path.exists(newroot)):
    os.mkdir(newroot)
NumofPic=0
dirs=os.listdir(root)
for dir in dirs:
    onedirpath=os.path.join(root,dir)
    pics=os.listdir(onedirpath)
    NuminoneDir=len(pics)
    NumofPic=NumofPic+NuminoneDir
strN='%d'%NumofPic
fileinfo.write(strN+'\n')
w=0       
for dir in dirs:
    onedirpath=os.path.join(root,dir)
    pics=os.listdir(onedirpath)
    print "process ",w
    for pic in pics:
        print "process ",pic
        onepicpath=os.path.join(onedirpath,pic)
        newpicpath="%s/%s"%(newroot,pic) 
        shutil.copy(onepicpath,newpicpath)
        #fileinfo.write('image'+'/'+pic+'\n')            
        fileinfo.write('lfwimgInonedir/'+pic+'\n')
fileinfo.close()