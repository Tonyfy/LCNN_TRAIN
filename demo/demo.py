# coding:utf-8
import os
import numpy as np
import cv2
import caffe
import matplotlib.pyplot as plt

prototxt = r"../prototxt/LCNN_deploy.prototxt"
caffemodel = r"../models/_iter_3560000.caffemodel"

if not os.path.isfile(caffemodel):
    print ("caffemodel not found!")
caffe.set_mode_cpu()
net = caffe.Net(prototxt,caffemodel,caffe.TEST)

#print("blobs {}\nparams {}".format(net.blobs.keys(), net.params.keys()))
input = cv2.imread("lxl.png",0)   #read face image
input = cv2.resize(input,(128,128),interpolation=cv2.INTER_CUBIC)   #we just need to resize the face to (128,128) 
plt.imshow(input,cmap='gray')
#plt.show()
img_blobinp = input[np.newaxis, np.newaxis, :, :]/255.0    #divide 255.0 ,make input is between 0-1
net.blobs['data'].reshape(*img_blobinp.shape)
net.blobs['data'].data[...] = img_blobinp

net.blobs['data'].data.shape
net.forward()  #go through the LCNN network

feature = net.blobs['eltwise_fc1'].data    #feature is from eltwise_fc1 layer
print feature.shape
print feature