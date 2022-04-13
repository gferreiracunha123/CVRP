import csv
import math
from os import listdir
from os.path import isfile, join

import tsplib95
from acopy import ant, solvers, plugins


def dist(a, b):
    (x1, y1), (x2, y2) = a, b
    return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def procurarota(alpha, beta, capacidade_feromonio, quantidade_formigas, fator_evaporacao_feromonio, numero_interacao,
                rotas_ja_visitadas, problem):
    #  click.echo(f'SEED={seed}')

    if (len(problem.node_coords) != 1):
        listremover = dict(problem.node_coords)
        for rotas in rotas_ja_visitadas:
            if (rotas != 1):
                listremover.pop(rotas)

        problem.node_coords = listremover

    G = problem.get_graph()

    colony = ant.Colony(alpha=alpha, beta=beta)
    solver = solvers.Solver(rho=fator_evaporacao_feromonio, q=capacidade_feromonio)

    # click.echo(solver)

    printout = plugins.Printout()
    solver.add_plugin(printout)

    timer = plugins.Timer()
    solver.add_plugin(timer)

    recorder = plugins.StatsRecorder()
    solver.add_plugin(recorder)

    result = solver.solve(G, colony, gen_size=quantidade_formigas, limit=numero_interacao)

    # timer.get_report()
    return result
    # if recorder:
    # plotter = utils.plot.Plotter(recorder.stats)
    # plotter.plot()


def carga(problem):
    dict_solucao = dict({})
    list_dict_solucao = []
    alpha = 2
    beta = 5
    capacidade_feromonio = problem.capacity
    quantidade_formigas = 5
    try:
        quantidade_formigas = int(str(problem.comment).split(":")[1].split(",")[0])
    except:
        print("Quantidade formigas default")
    fator_evaporacao_feromonio = 0.8
    numero_interacao = 100

    rotas = procurarota(alpha, beta, capacidade_feromonio, quantidade_formigas, fator_evaporacao_feromonio,
                        numero_interacao, [], problem)

    rotas = [int(x) for x in str(rotas).split("\t")[1].split(",")]

    capacidade = 0
    veiculo = 0
    capacidadetotal = 0
    solucao = []

    totalallrotascapaciti = 0

    for demandcount in problem.demands:
        totalallrotascapaciti = problem.demands[demandcount] + totalallrotascapaciti

    while capacidadetotal < totalallrotascapaciti:
        index = 0
        distancia = 0

        rotas = (rotas)
        for demand in rotas:
            capacidade = problem.demands[demand] + capacidade
            if capacidade <= problem.capacity:
                solucao.append(demand)
                if index + 1 <= len(rotas) - 1:
                    distancia = dist(problem.node_coords[rotas[index]],
                                     problem.node_coords[rotas[index + 1]]) + distancia
                else:
                    distancia = dist(problem.node_coords[rotas[index]],
                                     problem.node_coords[rotas[0]]) + distancia
            else:
                capacidade = capacidade - problem.demands[demand]
                break
            index = index + 1

        # print("veiculo-", veiculo, (solucao), " capacidade:", capacidade, " distancia ", distancia)
        dict_solucao.update({"veiculo": veiculo})
        dict_solucao.update({"capacidade": capacidade})
        dict_solucao.update({"rota": solucao})
        dict_solucao.update({"distancia": distancia})

        list_dict_solucao.append(dict_solucao)
        dict_solucao = dict({})

        if capacidadetotal < totalallrotascapaciti:
            try:
                rotas = procurarota(alpha, beta, capacidade_feromonio, quantidade_formigas, fator_evaporacao_feromonio,
                                    numero_interacao, solucao, problem)
            except:
                print("Carga distribuida")
                return list_dict_solucao

        rotas = [int(x) for x in str(rotas).split("\t")[1].split(",")]

        veiculo = veiculo + 1
        capacidadetotal = capacidade + capacidadetotal
        capacidade = 0
        solucao = []

    return list_dict_solucao


def main():
    open('dataset/analise/analise_Ant.csv', 'w', newline='', encoding='utf-8')
    raiz = 'dataset'
    files = [f for f in listdir(raiz) if isfile(join(raiz, f))]
    index = 0
    for file in files:
        if file != "Loggi-n501-k24.vrp":
            total_carga = 0
            total_distancia = 0
            problem = tsplib95.load(raiz + "/" + file)
            list_veiculos = carga(problem)
            print(problem.name)
            for veiculo in list_veiculos:
                print(veiculo)
                total_carga = total_carga + veiculo.get("capacidade")
                total_distancia = total_distancia + veiculo.get("distancia")
            print('Capacidade Total %s "Distancia Rotas Total %s' % (total_carga, total_distancia))
            cria_csv(index == 0, file, len(list_veiculos), total_carga, total_distancia, 0)
            index = index + 1


    exit(1)


def cria_csv(inicio, nome, qnt_veiculo, total_capacidade, total_distancia, interacao):
    f = open('dataset/analise/analise_Ant.csv', 'a', newline='', encoding='utf-8')

    # 2. cria o objeto de gravação
    w = csv.writer(f)

    # 3. grava as linhas
    if inicio:
        w.writerow(["Nome", "qnt Veiculos ", "Total Capacidade", "Total Distancia", "qnt Interacao","Tempo"])
    w.writerow([nome, qnt_veiculo, total_capacidade, total_distancia, interacao, 0])

    # Recomendado: feche o arquivo
    f.close()


if __name__ == '__main__':
    main()
