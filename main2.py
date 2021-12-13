import tsplib95
import pants
from os import listdir
from os.path import isfile, join

from numpy.lib import math

path = 'dataset'
files = [f for f in listdir(path) if isfile(join(path, f))]
#Documentacao
#https://pypi.org/project/ACO-Pants/

#argumentos opcionais:
#  -h, --help mostra esta mensagem de ajuda e sai
# -V, --version mostra o número da versão do programa e sai
#  -a A, --alpha Uma importância relativa colocada nos feromônios; default = 1
#  -b B, --beta B importância relativa colocada nas distâncias; padrão = 3
#  -l L, --limit L número de iterações a serem executadas; padrão = 100
#  -p P, razão --rho P do feromônio evaporado (0 <= P <= 1); padrão = 0,8
#  -e E, razão --elite E do feromônio da formiga elite; padrão = 0,5
#  -q Q, --QQ capacidade total de feromônios de cada formiga (Q> 0); padrão = 1
# -t T, --t0 T quantidade inicial de feromônio em cada borda (T> 0);
#                     padrão = 0,01
#  -c N, --contar N número de formigas usadas em cada iteração (N> 0); default = 10
# -d D, --dataset D especifica um conjunto particular de dados de demonstração; padrão = 33
# calculo de distancia elclidiana
def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

path ="dataset/A-n44-k7.vrp"

dataset = tsplib95.load(path)
#lista de nos- EX x-y
nodes = list(dataset.node_coords.values())
#cria a matrix de distancia para as fromigas;
world = pants.World(nodes, euclidean)
#Configuração da capaciade das formigas e quantidade.
solver = pants.Solver(ant_count=6,Q=100,limit=1000)
solution = solver.solve(world)

print('DISTANCE:', solution.distance) #total distance of the tour performed
tour = solution.tour    #nodes visited in order
print(tour)





