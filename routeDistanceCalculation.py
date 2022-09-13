import math
from itertools import islice
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import tsplib95

raiz = 'dataset/result/'
raizDataset = 'dataset/'
files = [f for f in listdir(raiz) if isfile(join(raiz, f))]


def distance(lat1, long1, lat2, long2):
    return dist([lat1, long1], [lat2, long2])


def dist(a, b):
    (x1, y1), (x2, y2) = a, b
    return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def group_elements(lst, chunk_size):
    listAux = []
    listAux2 = []
    index = 1
    for aux in lst:
        listAux.append(aux)
        if index == chunk_size:
            index = 1
            listAux2.append(listAux.copy())
            listAux = []
        else:
            index = index + 1
    return listAux2


for file in files:
    f = open('dataset/result/%s' % file, 'r')
    listRoute = f.read().split("\n")
    problem_aux = tsplib95.load(raizDataset + "/" + file.replace(".sol", ".vrp"))
    distanciaSingle = 0
    distanci=0
    for rote in listRoute:

        rote = rote.replace(rote.split(":")[0], "").replace(":", "")
        listVeiculos = rote.split(" ")[1:]
        x = 2
        listVeiculos = group_elements(listVeiculos, 2)

        for cood in listVeiculos:
            if len(cood) != 1:
                distanci = dist(problem_aux.node_coords[int(cood[0])],
                                                         problem_aux.node_coords[int(cood[1])])
                print(cood[0],str(problem_aux.node_coords[int(cood[0])]))
                print(cood[1],str(problem_aux.node_coords[int(cood[1])]))
                distanciaSingle = distanciaSingle + distanci

    print(distanciaSingle)


