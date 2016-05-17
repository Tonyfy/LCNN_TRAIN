---
title: 人脸识别CNN网络训练流程 #文章页面上的显示名称，可以任意修改，不会出现在URL中
date: 2016-05-06 20:30:16 #文章生成时间，一般不改，当然也可以任意修改
categories: CNN #分类
tags: [CNN,facerecognition,DL] #文章标签，可空，多标签请用格式，注意:后面有个空格
description: 训练LCNN。
---

#人脸识别网络训练流程

## 目标

训练论文"A Lightened CNN for Deep Face Representation"中的caffe网络。

## 数据

CASIA-WebFace 可在[这里](http://www.cbsr.ia.ac.cn/english/CASIA-WebFace-Database.html)申请。

## 网络配置

详细配置查看查看我的github项目中[prototxt/](https://github.com/Tonyfy/LCNN_TRAIN/tree/master/prototxt)中的[LCNN_solver.prototxt](https://github.com/Tonyfy/LCNN_TRAIN/blob/master/prototxt/LCNN_solver.prototxt)和[LCNN_train_test.prototxt](https://github.com/Tonyfy/LCNN_TRAIN/blob/master/prototxt/LCNN_train_test.prototxt)。

对学习率的设置
初始学习率设置为0.01，训练过程中，发现初始loss为9.3，约为-log(1/10575)正常，稍加训练后，loss上升到80+，说明学习率设置过大，调整为0.001，并以inv方式进行衰减。发现loss逐渐衰减了。

## 测试记录

测试数据集：[lfw](http://vis-www.cs.umass.edu/lfw/)。取官方给出的[pairs.txt](http://vis-www.cs.umass.edu/lfw/pairs.txt)进行测试。保证pairs.txt中的图片不会出现在训练集中。

|数据组织|数量|描述|
|--|--|--|
|Intra-pair|3000|每一个pair是同一个人物的两张不同场景下的人脸图片对|
|Extra-pair|3000|每一个pair是不同人物的人脸图片对|

使用pairs.txt中给出的6000对人脸对测试本模型的准确度。按照标准的ROC评测方案，并在True Positive Rate与False Reject Rate相当时，取出准确率用于表征模型的准确率。将不同迭代次数时的测试结果记录在下表中。

|迭代次数(万)|True Positive Rate(%)|False Reject Rate(%)|Average(%)|
|--|--|--|--|
|115|96.2|96.2|96.2|
|165|96.8333|96.8667|96.85|
|183|96.7|96.8333|96.7667|
|196.5|96.9333|96.9667|96.95|
|206|96.7333|96.8333|96.7833|
|260|96.7667|96.8333|96.8|

## 计算环境

NVIDIA GTX970 

