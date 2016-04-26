# -*- coding: utf-8 -*-
import os
import shutil
import string

root=r"D:\BaiduYunDownload\WebFace\CASIA-WebFace"
#out=r""
foldername = os.listdir(root)
w=0
for i in foldername:
    folder = "%s\%s"%(root,i)
    print "comlete ",w," ..."
    w=w+1
    #ÐÂÃû×Ö
    pic=os.listdir(folder)
    for j in pic:
        oldname="%s\%s"%(folder,j)
        newname = "%s\%d%s%s"%(folder,w,'_',j)  
        #newname = "%s\%s%s%s"%(folder,i,'_',j)  #将人物的名字信息加入到每张图片之中
        os.renames(oldname,newname)