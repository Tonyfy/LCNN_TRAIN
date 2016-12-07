#!/usr/bin/env python

import argparse
import logging
import os
import sys

import cv2
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score


logger = logging.getLogger()
logger.setLevel(logging.INFO)

USE_L2_METRIC = False

def load_pairs(pairs_path):
    print("...Reading pairs.")
    pairs = []
    with open(pairs_path, 'r') as f:
        for line in f.readlines()[1:]:
            pair = line.strip().split()
            pairs.append(pair)
    assert(len(pairs) == 6000)
    return np.array(pairs)


def pairs_info(pair, suffix):
    if len(pair) == 3:
        name1 = "{}/{}_{}.{}".format(pair[0], pair[0], pair[1].zfill(4), suffix)
        name2 = "{}/{}_{}.{}".format(pair[0], pair[0], pair[2].zfill(4), suffix)
        same = 1
    elif len(pair) == 4:
        name1 = "{}/{}_{}.{}".format(pair[0], pair[0], pair[1].zfill(4), suffix)
        name2 = "{}/{}_{}.{}".format(pair[2], pair[2], pair[3].zfill(4), suffix)
        same = 0
    else:
        raise Exception(
            "Unexpected pair length: {}".format(len(pair)))
    return (name1, name2, same)


def read2feature(root, name1, name2):
    f1 = np.fromfile(os.path.join(root, name1), dtype=np.float32)
    f2 = np.fromfile(os.path.join(root, name2), dtype=np.float32)
    assert len(f1) == len(f2)
    return f1, f2


def eval_acc(threshold, diff):
    y_true = []
    y_predict = []
    for d in diff:
        if USE_L2_METRIC:
            same = 1 if float(d[2]) < threshold else 0
        else:
            same = 1 if float(d[2]) > threshold else 0
        y_predict.append(same)
        y_true.append(int(d[3]))
    y_true = np.array(y_true)
    y_predict = np.array(y_predict)
    accuracy = accuracy_score(y_true, y_predict)
    return accuracy


def find_best_threshold(thresholds, predicts):
    best_threshold = best_acc = 0
    for threshold in thresholds:
        accuracy = eval_acc(threshold, predicts)
        if accuracy >= best_acc:
            best_acc = accuracy
            best_threshold = threshold
    return best_threshold


def acc(predict_file):
    print("...Computing accuracy.")
    folds = KFold(n=6000, n_folds=10, shuffle=False)
    if USE_L2_METRIC:
        thresholds = np.arange(170, 180, 0.5)
    else:
        thresholds = np.arange(-1.0, 1.0, 0.005)
    accuracy = []
    thd = []
    with open(predict_file, "r") as f:
        predicts = f.readlines()
        predicts = np.array(map(lambda line:line.strip('\n').split(), predicts))
        for idx, (train, test) in enumerate(folds):
            logging.info("processing fold {}...".format(idx))
            best_thresh = find_best_threshold(thresholds, predicts[train])
            accuracy.append(eval_acc(best_thresh, predicts[test]))
            thd.append(best_thresh)
    return accuracy,thd


def get_predict_file(args):
    assert(os.path.exists(args.lfw_feature))
    pairs = load_pairs(args.pairs)
    with open(args.predict_file, 'w') as f:
        for pair in pairs:
            name1, name2, same = pairs_info(pair, args.suffix)
            logging.info("processing name1:{} <---> name2:{}".format(name1, name2))
            f1, f2 = read2feature(args.lfw_feature, name1, name2)
            if USE_L2_METRIC:
                dis = np.sqrt(np.sum(np.square(f1-f2)))
            else:
                dis = np.dot(f1, f2)/np.linalg.norm(f1)/np.linalg.norm(f2)
            f.write(name1 + '\t' + name2 + '\t' + str(dis) + '\t' + str(same) + '\n')


def print_result(args):
    accuracy, threshold = acc(args.predict_file)
    logging.info("10-fold accuracy is:\n{}\n".format(accuracy))
    logging.info("10-fold threshold is:\n{}\n".format(threshold))
    logging.info("mean threshold is:%.4f\n", np.mean(threshold))
    logging.info("mean is:%.4f, var is:%.4f", np.mean(accuracy), np.std(accuracy))



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pairs', type=str, default="./pairs.txt",
                        help='Location of the LFW pairs file from http://vis-www.cs.umass.edu/lfw/pairs.txt')
    parser.add_argument('--lfw-feature', type=str, default="D:/FACE_VERI/lfw-deepfunneled",
                        help='The directory of lfw-feature, which contains the feature lfw faces')
    parser.add_argument('--suffix', type=str, default="data",
                        help='The type of feature')
    parser.add_argument('--predict-file', type=str, default='./predict.txt',
                        help='The file which contains similarity distance of every pair image given in pairs.txt')
    parser.add_argument('--l2', action='store_true', help='use l2 distance, default use cos distance')
    args = parser.parse_args()
    if args.l2:
        global USE_L2_METRIC
        USE_L2_METRIC = True
    logging.info(args)
    if not os.path.isfile(args.pairs):
        logging.info("Error: LFW pairs (--lfwPairs) file not found.")
        logging.info("Download from http://vis-www.cs.umass.edu/lfw/pairs.txt.")
        logging.info("Default location:", "./pairs.txt")
        sys.exit(-1)
    print("Loading embeddings done")
    if not os.path.exists(args.lfw_feature):
        logging.info("Error: lfw dataset not aligned.")
        logging.info("Please use ./utils/align_face.py to align lfw firstly")
        sys.exit(-1)
    if not os.path.isfile(args.predict_file):
        logging.info("begin generate the predict.txt.")
        get_predict_file(args)
        logging.info("predict.txt has benn generated")
    print_result(args)
if __name__ == '__main__':
    main()
