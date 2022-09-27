import math
from itertools import islice
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import tsplib95
import numpy as np
from scipy.spatial.distance import squareform, pdist
from tsplib95.distances import euclidean, geographical, pseudo_euclidean

raiz = 'dataset/result/'
raizDataset = 'dataset/'
files = [f for f in listdir(raiz) if isfile(join(raiz, f))]


def route_cost(self, routes):
    cost = 0
    for r in routes:
        for i in range(1, len(r)):
            cost += self[r[i - 1], r[i]]
        cost += self[r[-1], r[0]]
    return cost



for file in files:
    f = open('dataset/result/%s' % file, 'r')
    listRoute = f.read().split("\n")
    problem_aux = tsplib95.load(raizDataset + "/" + "A-n33-k5.vrp")
    distanciaSingle = 0
    distanci = 0

    passo_1=pdist(list(problem_aux.node_coords.values()))
    passo_2 = squareform(passo_1)
    passo_3 = np.matrix(data=passo_2)
    passo_4 = np.round(passo_3)
    testeList=passo_4

    #A-n32-k5.vrp"
    #route_cost(testeList,[[0, 21, 31, 19, 17, 13, 7, 26],[0, 12, 1, 16, 30], [0, 27, 24],[0, 29, 18, 8, 9, 22, 15, 10, 25, 5, 20],[0, 14, 28, 11, 4, 23, 3, 2, 6]])
    # A-n33-k5.vrp"
    #route_cost(testeList,[[0, 15, 17, 9, 3, 16, 29],[0, 12, 5, 26, 7,8,13,32,2], [0,20, 4, 27,25,30,10],[0,23, 28, 18, 22],[0,24, 6, 19, 21, 1, 31, 11]])



