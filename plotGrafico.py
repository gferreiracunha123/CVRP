from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt

raiz = 'dataset/plot/'
files = [f for f in listdir(raiz) if isfile(join(raiz, f))]
for file in files:
    f = open('dataset/plot/%s' % file, 'r')
    listaux = f.read().replace("\"", "")
    # 2. cria o objeto de gravação
    listCarro = listaux.split(",[[")
    novaList = []
    novaListVetor = []
    for x in listCarro:
        novaList.append([int(i) for i in x.split("],")[0].replace("[", "").replace("\\'", "").split(",")])
        novaList.append([int(i) for i in x.split("],")[1].replace("[", "").replace("\\'", "").split(",")])
        novaList.append(x.split("],")[2].replace("]", "").replace("\'", ""))
        novaListVetor.append(novaList)
        novaList = []
    list_cor = ['r', 'c', 'y', 'm', 'g', 'b', 'k', 'w']
    for nova in novaListVetor:
        plt.plot(nova[0], nova[1], marker='o', ms=5, label="Carro %s" % nova[2])
    plt.legend(bbox_to_anchor=(0.1, 0.3, 1.2, 0.8))
    plt.tight_layout()
    plt.grid()
    plt.xlabel('X ')
    plt.ylabel('Y ')
    plt.title(file)
    plt.show()
exit()
