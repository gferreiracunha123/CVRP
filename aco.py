import csv
import math
import random
import time
from os import listdir
from os.path import isfile, join
from random import randint

import matplotlib.pyplot as plt

import tsplib95
from acopy import ant, solvers, plugins, utils, SolverPlugin

import tsplib95
from acopy import ant, solvers, plugins, Ant
from numpy.random import random

interacao = ""


def dist(a, b):
    (x1, y1), (x2, y2) = a, b
    return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def procurarota(alpha, beta, capacidade_feromonio, fator_evaporacao_feromonio, numero_interacao,
                problem):
    #  click.echo(f'SEED={seed}')

    G = problem.get_graph()

    colony = ant.Colony(alpha=alpha, beta=beta)
    solver = solvers.Solver(rho=fator_evaporacao_feromonio, q=capacidade_feromonio)

    # click.echo(solver)

    printout = Printout()
    solver.add_plugin(printout)

    tour = solver.solve(G, colony, limit=numero_interacao)

    rotas = [int(x) for x in str(tour).split("\t")[1].split(",")]
    rotamodelo = list(dict({}))
    indexrotamodelo = 0
    rotamodelo.append({"interacao": solver.plugins['Printout'].name})
    for _ in rotas:
        try:
            rotamodelo.append({"rota": [rotas[indexrotamodelo], rotas[indexrotamodelo + 1]]})
            indexrotamodelo = indexrotamodelo + 1
        except:
            return rotamodelo


class Printout(SolverPlugin):
    _ROW = '{:<10} {:<20} {}'
    interacao

    def initialize(self, solver):
        super().initialize(solver)
        self.iteration = 0
        self._last_line = ''

    def on_start(self, state):
        self.iteration = 0

    #  print(f'Using {state.gen_size} ants from {state.colony}')
    # print(f'Performing {state.limit} iterations:')
    # print(self._ROW.format('Iteration', 'Cost', 'Solution'))

    def on_iteration(self, state):
        self.iteration += 1
        line = self._ROW.format(self.iteration, state.best.cost,
                                state.best.get_easy_id())
        print(line, end='\n' if state.is_new_record else '\r')
        if state.is_new_record:
            self.name = str(self.iteration)
        self._last_line = line

    def on_finish(self, state):
        eraser = '-' * len(self._last_line)
        return self._last_line


def carga(problem):
    dict_solucao = dict({})
    list_dict_solucao = []
    alpha = 2
    beta = 5
    capacidade_feromonio = problem.capacity
    quantidade_formigas = 20
    # try:
    # quantidade_formigas = int(str(problem.comment).split(":")[1].split(",")[0])
    # except:
    #   print("Quantidade formigas default")
    fator_evaporacao_feromonio = 0.8
    numero_interacao = 200

    rotas_completo = procurarota(alpha, beta, capacidade_feromonio, fator_evaporacao_feromonio,
                                 numero_interacao, problem)
    rotas = rotas_completo[1:len(rotas_completo)]
    capacidade = 0
    veiculo = 0
    capacidadetotal = 0
    solucao = list(dict({}))

    totalrotascapacidade = 0

    for demandcount in problem.demands:
        totalrotascapacidade = problem.demands[demandcount] + totalrotascapacidade

    voltaInicio = 1
    while capacidadetotal < totalrotascapacidade:
        index = 0
        distancia = 0

        rotas = (rotas)

        for _ in rotas:

            capacidade = problem.demands[rotas[index].get("rota")[0]] + capacidade

            if capacidade <= problem.capacity:
                distanciaSingle = dist(problem.node_coords[rotas[index].get("rota")[0]],
                                       problem.node_coords[rotas[index].get("rota")[1]])
                distancia = distancia + distanciaSingle

                solucao.append([{"rota": [rotas[index].get("rota")[0], rotas[index].get("rota")[1]]},
                                {"distancia": distanciaSingle},
                                {"capacidade": problem.demands[rotas[index].get("rota")[0]]}])
            else:
                break
            index = index + 1

        solucao.append([{"rota": [rotas[len(solucao) - 1].get("rota")[1], 1]},
                        {"distancia": dist(problem.node_coords[rotas[len(solucao) - 1].get("rota")[1]],
                                           problem.node_coords[1])},
                        {"capacidade": problem.demands[1]}])

        dict_solucao.update({"veiculo": veiculo})
        dict_solucao.update({"capacidade": capacidade})
        dict_solucao.update({"rota": solucao})
        dict_solucao.update({"distancia_total": distancia})
        dict_solucao.update({"interacao": rotas_completo[0]['interacao']})

        list_dict_solucao.append(dict_solucao)
        dict_solucao = dict({})

        solucaoaux = solucao[:]
        if capacidadetotal < totalrotascapacidade:
            try:
                lista_remover = rotas[:]
                for rota in solucaoaux:
                    if rota[0].get("rota")[1] != 1:
                        lista_remover.remove(rota[0])

                rotas = lista_remover
                rotas.insert(0, {'rota': [1, lista_remover[0].get("rota")[1]]})
                rotas.pop(1)
            except:
                print("Carga distribuida")
                return list_dict_solucao

        veiculo = veiculo + 1
        capacidadetotal = capacidade + capacidadetotal
        capacidade = 0
        solucao = list(dict({}))
        voltaInicio = voltaInicio + 1

    return list_dict_solucao


def main():
    open('dataset/analise/analise_Ant.csv', 'w', newline='', encoding='utf-8')
    raiz = 'dataset'
    files = [f for f in listdir(raiz) if isfile(join(raiz, f))]
    index = 0
    x = []
    y = []
    list_cor = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
    indexcor = 0
    listr = []
    for file in files:
        #if file == "E-n22-k4.vrp":

            inicio = time.time()
            total_carga = 0
            total_distancia = 0
            problem = tsplib95.load(raiz + "/" + file)
            problem_aux = tsplib95.load(raiz + "/" + file)
            list_veiculos = carga(problem)
            print(problem.name)
            indexveiculo = 0
            rotaaux = []
            listr = []
            for veiculo in list_veiculos:
                print("veiculo: %s" % (veiculo.get("veiculo")))
                for rotas in veiculo.get("rota"):
                    print(rotas)
                    rotaaux.append(rotas[0].get("rota")[0])
                rotaaux.append(1)

                total_carga = total_carga + veiculo.get("capacidade")
                total_distancia = total_distancia + veiculo.get("distancia_total")
                for r in rotaaux:
                    x.append(problem_aux.node_coords[r][0])
                    y.append(problem_aux.node_coords[r][1])
                listr.append([x, y, indexveiculo])
                x = []
                y = []
                rotaaux = []
                indexcor = indexcor + 1
                indexveiculo = indexveiculo + 1
            # plotGrafico(listr, file)
            fim = time.time()
            print(total_distancia)
            plotGrafico(listr, file)
            cria_csv(index == 0, file, len(list_veiculos), total_carga, total_distancia,
                     str(problem.comment).split(",")[2].split(":")[1].replace(")", ""), list_veiculos[0]['interacao'],
                     str(fim - inicio))
            index=index+1

    exit(1)


def plotGrafico(listr, file):
    f = open('dataset/plot/plot_%s.csv' % file , 'a', newline='', encoding='utf-8')
    w = csv.writer(f)
    w.writerow(listr)
    f.close()
    #plotGraficoteste(listr, file)

def plotGraficoteste(listr, file):
    for x in listr:
        plt.plot(x[0], x[1], marker='o', ms=5, label="Carro %s" % x[2])
    plt.legend(bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.grid()
    plt.xlabel('cod -X ')
    plt.ylabel('cod -Y ')
    plt.title(file)
    plt.show()


def cria_csv(inicio, nome, qnt_veiculo, total_capacidade, total_distancia, distancia_optima, interacao, tempo):
    f = open('dataset/analise/analise_Ant.csv', 'a', newline='', encoding='utf-8')

    # 2. cria o objeto de gravação
    w = csv.writer(f)

    # 3. grava as linhas
    if inicio:
        w.writerow(["Nome", "qnt Veiculos ", "Total Capacidade", "Total Distancia", "Distancia otima", "qnt Interacao",
                    "Tempo"])
    w.writerow([nome, qnt_veiculo, total_capacidade, total_distancia, distancia_optima, interacao, tempo])

    # Recomendado: feche o arquivo
    f.close()


if __name__ == '__main__':
    main()
