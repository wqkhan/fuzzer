#!/usr/bin/python3.5
'''
created on: Feb 4th 2019
author: John DiMatteo
description: 

trains the clustering algorithm on offline data

in: offline data directory (directory)
out: centroids of kmeans centroids.txt

'''

from classifiers.kmeans import Kmeans
from classifiers.kmeans_dba import KmeansDBA
import numpy as np
import os
import sys

K=int(sys.argv[1]) # no. of clusters
DATA_IN=sys.argv[2] # location of training dataset
CENTROIDS_OUT=sys.argv[3] # location to put centroids after training
ALGORITHM=sys.argv[4] # kmeans or dba?


def pad(s, m, fillval=0.0):
    """ pads with zeros so they are all equal length """
    lens = np.array([len(item) for item in s])
    mask = lens[:, None] > np.arange(lens.max())
    out = np.full(mask.shape, fillval)
    out[mask] = np.concatenate(s)
    return out

def load_no_pad(path):
    signals = []
    for filename in os.listdir(path):
        filename = path + '/' + filename
        signals.append(np.load(filename))
    return signals

def load_interpolate(path):
    signals = []
    for filename in os.listdir(path):
        filename = path + '/' + filename
        signals.append(np.load(filename))

    
    return signals

def load(path):
    max_length = 0
    signals = []
    for filename in os.listdir(path):
        filename = path + '/' + filename
        signals.append(np.load(filename))
    signals = pad(signals, max_length)
    return signals


def train():

    if ALGORITHM.lower() == 'kmeans':
        Detector = Kmeans(K)
        data = load(DATA_IN)
        data = np.vstack(data)
    elif ALGORITHM.lower() == 'dba':
        Detector = KmeansDBA(K)
        data = load_no_pad(DATA_IN)
    else:
        print("Improper argument specified. kmeans or dba!")
        exit()

    print("%d signals loaded from %s" % (len(data), DATA_IN)) 


    Detector.k_means_clust(data, 10, 100)
    Detector.save_centroids(CENTROIDS_OUT)

if __name__ == "__main__":
    train()
    exit()
