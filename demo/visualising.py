# coding:utf-8
# visualize face during flow in convulotion layer

import os
import numpy as np
import cv2
import caffe
import matplotlib.pyplot as plt
import scipy
from scipy import misc

def visualize_feature(net, layer_name, padding=0, filename=''):
    '''
    :param net:  net structure of the nerual network
    :param layer_name: the layer name which your want to visualize
    :param padding:
    :param filename:
    :return:
    '''
    # The parameters are a list of [weights, biases]
    #data = np.copy(net.params[layer_name][0].data)
    data = np.copy(net.blobs[layer_name].data)
    # N is the total number of feature map
    N = data.shape[1]
    # Ensure the resulting image is square
    feature_per_row = int(np.ceil(np.sqrt(N)))
    # Assume the featutrmap are square
    feature_size = data.shape[2]
    # Size of the result image including padding
    result_size = feature_per_row*(feature_size + padding) - padding
    # Initialize result image to all zeros
    result = np.zeros((result_size, result_size))

    # Tile the filters into the result image
    filter_x = 0
    filter_y = 0
    for n in range(data.shape[0]):
        for c in range(data.shape[1]):
            if filter_x == feature_per_row:
                filter_y += 1
                filter_x = 0
            for i in range(feature_size):
                for j in range(feature_size):
                    result[filter_y*(feature_size + padding) + i, filter_x*(feature_size + padding) + j] = data[n, c, i, j]
            filter_x += 1

    # Normalize image to 0-1
    min = result.min()
    max = result.max()
    result = (result - min) / (max - min)
    result *= 255.0
    # Plot figure
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(result, cmap='gray', interpolation='nearest')
    # Save plot if filename is set
    if filename != '':
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)

    #plt.show()

def visualize_weight(net, layer_name, padding=0, filename=''):
    '''
    :param net:  net structure of the nerual network
    :param layer_name: the layer name which your want to visualize
    :param padding:
    :param filename:
    :return:
    '''
    # The parameters are a list of [weights, biases]
    #data = np.copy(net.params[layer_name][0].data)
    data = np.copy(net.params[layer_name][0].data)
    # N is the total number of convolutions
    N = data.shape[0] * data.shape[1]
    # Ensure the resulting image is square
    filters_per_row = int(np.ceil(np.sqrt(N)))
    # Assume the filters are square
    filter_size = data.shape[2]
    # Size of the result image including padding
    result_size = filters_per_row * (filter_size + padding) - padding
    # Initialize result image to all zeros
    result = np.zeros((result_size, result_size))

    # Tile the filters into the result image
    filter_x = 0
    filter_y = 0
    for n in range(data.shape[0]):
        for c in range(data.shape[1]):
            if filter_x == filters_per_row:
                filter_y += 1
                filter_x = 0
            for i in range(filter_size):
                for j in range(filter_size):
                    result[filter_y * (filter_size + padding) + i, filter_x * (filter_size + padding) + j] = data[
                        n, c, i, j]
            filter_x += 1

    # Normalize image to 0-1
    min = result.min()
    max = result.max()
    result = (result - min) / (max - min)
    # Plot figure
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(result, cmap='gray', interpolation='nearest')

    # Save plot if filename is set
    if filename != '':
        plt.savefig(filename, bbox_inches='tight', pad_inches=0)

    #plt.show()

prototxt = r"../prototxt/LCNN_deploy.prototxt"
caffemodel = r"../models/_iter_3560000.caffemodel"
if not os.path.isfile(caffemodel):
    print ("caffemodel not found!")
caffe.set_mode_cpu()
net = caffe.Net(prototxt, caffemodel, caffe.TEST)

# print("blobs {}\nparams {}".format(net.blobs.keys(), net.params.keys()))
ims = ['75-1.jpg']  #, '75-2.jpg', '76-1.jpg'
inp = []
for i in range(0, 1):
    input = cv2.imread(ims[i], 0)  # read face image
    input = cv2.resize(input, (128, 128),
                       interpolation=cv2.INTER_CUBIC)  # we just need to resize the face to (128,128)
    inp.append(input)
    img_blobinp = input[np.newaxis, np.newaxis, :, :] / 255.0  # divide 255.0 ,make input is between 0-1
    net.blobs['data'].reshape(*img_blobinp.shape)
    net.blobs['data'].data[...] = img_blobinp
    net.blobs['data'].data.shape
    net.forward()  # go through the LCNN network

    # visualising the feature map on conv layers
    # {conv1,conv2a,conv2,conv3a,conv3,conv4a,conv4,conv5a,conv5}
    visualize_feature(net,'conv1',0,'conv1.jpg')
    visualize_feature(net,'conv2a',0,'conv2a.jpg')
    visualize_feature(net,'conv2',0,'conv2.jpg')
    visualize_feature(net,'conv3a',0,'conv3a.jpg')
    visualize_feature(net,'conv3',0,'conv3.jpg')
    visualize_feature(net,'conv4a',0,'conv4a.jpg')
    visualize_feature(net,'conv4',0,'conv4.jpg')
    visualize_feature(net,'conv5a',0,'conv5a.jpg')
    visualize_feature(net,'conv5',0,'conv5.jpg')

    visualize_weight(net,'conv1', filename='conv1w.jpg')
    visualize_weight(net,'conv2a', filename='conv2aw.jpg')
    visualize_weight(net,'conv2', filename='conv2w.jpg')
    visualize_weight(net,'conv3a', filename='conv3aw.jpg')
    visualize_weight(net,'conv3', filename='conv3w.jpg')
    visualize_weight(net,'conv4a', filename='conv4aw.jpg')
    visualize_weight(net,'conv4', filename='conv4w.jpg')
    visualize_weight(net,'conv5a', filename='conv5aw.jpg')
    visualize_weight(net,'conv5', filename='conv5w.jpg')





