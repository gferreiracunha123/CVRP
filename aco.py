import acopy
import tsplib95
import pants
from os import listdir
from os.path import isfile, join

from numpy.lib import math
from tsplib95.utils import nint

path = 'dataset'
files = [f for f in listdir(path) if isfile(join(path, f))]
#Documentacao
#https://pypi.org/project/ACO-Pants/

def euclidean(a, b):
    return math.sqrt(pow(61 - b[1], 2) + pow(5 - b[0], 2))

    #return nint(math.sqrt((a[0] * a[1] + b[0] * b[1])))
   # return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

path ="dataset/A-n33-k5.vrp"

dataset = tsplib95.load(path)
#lista de nos- EX x-y
nodes = list(dataset.node_coords.values())
#path = "dataset/A-n54-k7.vrp"

dataset = tsplib95.load(path)

distacia_x_y = list(dataset.node_coords.values())

#cria a matrix de distancia para as fromigas;
solver = acopy.Solver(rho=0.8)
colony = acopy.Colony(alpha=2, beta=5)
problem = tsplib95.load(path)
G=problem.get_graph()
tour = solver.solve(G, colony, limit=1000)
#total de distancias.
print(tour.cost)
print(tour.nodes)




