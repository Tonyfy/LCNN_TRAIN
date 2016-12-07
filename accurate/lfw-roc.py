#!/usr/bin/env python

import logging
import os
import sys

import numpy as np

USE_L2_METRIC = False

def get_roc(predict_file,roc_file,veri_err):
    print("...start to calculate for roc")
    posi_simi_metric = []
    nega_simi_metric = []
    with open(predict_file,"r") as f:
         predicts = f.readlines()
         for line in predicts:
             ground_label = line.split('\t')[-1]
             simi_metric = line.split('\t')[-2]
             if((int)(ground_label) == 1):
                 posi_simi_metric.append(simi_metric)
             else:
                 nega_simi_metric.append(simi_metric)
    
    print 'posi_size = '+ str(len(posi_simi_metric))+' nega_size = '+str(len(nega_simi_metric))
     
    choosed_th=0
    if USE_L2_METRIC:
         a=1
    else:
        to_print = 0
        th = np.arange(0.1,0.4,0.0001)
        with open(roc_file,'w') as f:
            for i in th:
                TP = 0
                TN = 0
                for m in posi_simi_metric:
                    if float(m)>float(i):
                        TP = TP+1
                for n in nega_simi_metric:
                    if float(n)<float(i):
                        TN = TN+1
                f.write(str(i)+' '+str((TP)/(0.000001+len(posi_simi_metric)))+' '+str((TN)/(0.000001+len(nega_simi_metric)))+'\n')   
                if TN>=TP and to_print==0:
                    print 'EER is '+str((TP+TN)/6000.0)+' and the th is '+ str(i)
                    to_print = 1
                    choosed_th = i
        with open(veri_err,"w") as err:
            with open(predict_file,"r") as f:
                preds = f.readlines()
                for line in preds:
                    ground_label = line.split('\t')[-1]
                    simi_tmp = line.split('\t')[-2]
                    if int(float(simi_tmp)-float(choosed_th)+1.0)!=int(ground_label):
                        #veri err pairs
                        err.write(line)
                    else:
                        a=1

def main():
    predict_file = "predict.txt"
    roc_file = "roc.txt"
    veri_err = "veri_err.txt"
    get_roc(predict_file,roc_file,veri_err)

if __name__ == '__main__':
    main()
