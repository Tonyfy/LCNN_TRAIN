
import os
import sys
import cv2
import numpy as np

def show_err(veri_err_file,imgsrc_path,show_path):
    with open(veri_err_file) as err:
        lines = err.readlines()
        for line in lines:
            ground_truth = line.split('\t')[-1]
            first = line.split('\t')[0].split('.')[0]+str('.jpg')
            second = line.split('\t')[1].split('.')[0]+str('.jpg')
            img_first = os.path.join(imgsrc_path,first)
            img_second = os.path.join(imgsrc_path,second)
            # print img_first
            img1 = cv2.imread(img_first)
            img2 = cv2.imread(img_second)
            
           # print np.shape(img1)
            
            h1,w1,c1 = img1.shape
            h2,w2,c2 = img2.shape
            w = max(w1,w2)
            h = max(h1,h2)
            img = np.zeros((h,2*w,3),dtype=np.uint8)
            img[0:h1,0:w1,:] = img1
            img[0:h2,w:w2+w,:] = img2
            
            savepath = ""
            if ground_truth == 1:
                savepath = os.path.join(show_path,"FR_"+first.split('/')[-1].split('.')[0]+"&"+second.split('/')[-1])
            else:
                savepath = os.path.join(show_path,"FA_"+first.split('/')[-1].split('.')[0]+"&"+second.split('/')[-1])
            print savepath
            cv2.imwrite(savepath,img)
            
def main():
    veri_err_file = "veri_err.txt"
    imgsrc_path = "D:/FACE_VERI/lfw-deepfunneled"
    show_path = os.path.join(os.getcwd(),"show_err")
    if not os.path.exists(show_path):
        os.makedirs(show_path)
    show_err(veri_err_file,imgsrc_path,show_path)
    
if __name__ == '__main__':
    main()