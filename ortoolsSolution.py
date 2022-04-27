import csv
from os import listdir
from os.path import isfile, join

import tsplib95
from numpy.lib import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp


def distance(lat1, long1, lat2, long2):
    return dist([lat1, long1], [lat2, long2])


def create_data_model(path):
    """Stores the data for the problem."""
    dataset = tsplib95.load(path)

    distacia_x_y = list(dataset.node_coords.values())
    distacia = []

    index = 0
    # cria matriz de distancia
    for x in distacia_x_y:
        indey = int(0)
        distaciaux = []
        for y in distacia_x_y:
            distaciaux.append(dist(x, y))
            indey = indey + 1
        distacia.append(distaciaux)
        index = index + 1

    data = {}
    data['distance_matrix'] = distacia
    # calculate_distance_matrix( list(dataset.node_coords.values()))
    data['demands'] = list(dataset.demands.values())
    # list(dataset.demands.values())
    quantidade_formigas = 5
    try:
        quantidade_formigas = int(str(dataset.comment).split(":")[1].split(",")[0])
    except:
        print("Quantidade formigas default")

    data['num_vehicles'] = quantidade_formigas
    data['vehicle_capacities'] = [dataset.capacity] * data['num_vehicles']
    data['depot'] = 0
    return data


def print_solution(inicio,file,path,data, manager, routing, solution):
    dict_solucao = dict({})
    list_dict_solucao = []
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        plan_output2 = 'cordenadas {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} --- ({1}) -> '.format(node_index, route_load)

            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)

        plan_output += ' {0} Carga ({1})\n'.format(manager.IndexToNode(index),
                                                   route_load)

        plan_output += 'Distância da rota: {}m\n'.format(route_distance)
        plan_output += 'Carga da rota: {}\n'.format(route_load)
        print(plan_output)
        print(plan_output2)

        total_distance += route_distance
        total_load += route_load
        dict_solucao.update({"veiculo": vehicle_id})
        dict_solucao.update({"capacidade": route_load})
        dict_solucao.update({"rota": route_load})
        dict_solucao.update({"distancia": route_distance})
        list_dict_solucao.append(dict_solucao)
        dict_solucao = dict({})
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))
    cria_csv(inicio, file, len(list_dict_solucao), total_load, total_distance, 0)

''
def dist(a, b):
    (x1, y1), (x2, y2) = a, b
    return math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    open('dataset/analise/analise_Ortools.csv', 'w', newline='', encoding='utf-8')
    raiz = 'dataset'
    files = [f for f in listdir(raiz) if isfile(join(raiz, f))]
    index = 0
    for file in files:
        if file != "Loggi-n501-k24.vrp":
            path = raiz+"/"+file
            data = create_data_model(path)

            # Create the routing index manager.
            manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                                   data['num_vehicles'], data['depot'])

            # Create Routing Model.
            routing = pywrapcp.RoutingModel(manager)

            # Create and register a transit callback.
            def distance_callback(from_index, to_index):
                """Returns the distance between the two nodes."""
                # Convert from routing variable Index to distance matrix NodeIndex.
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                return data['distance_matrix'][from_node][to_node]

            transit_callback_index = routing.RegisterTransitCallback(distance_callback)

            # Define cost of each arc.
            routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            # Add Capacity constraint.
            def demand_callback(from_index):
                """Returns the demand of the node."""
                # Convert from routing variable Index to demands NodeIndex.
                from_node = manager.IndexToNode(from_index)
                return data['demands'][from_node]

            demand_callback_index = routing.RegisterUnaryTransitCallback(
                demand_callback)
            routing.AddDimensionWithVehicleCapacity(
                demand_callback_index,
                0,  # null capacity slack
                data['vehicle_capacities'],  # vehicle maximum capacities
                True,  # start cumul to zero
                'Capacity')

            # Setting first solution heuristic.
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
            search_parameters.local_search_metaheuristic = (
                routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
            search_parameters.time_limit.FromSeconds(1)

            # Solve the problem.
            solution = routing.SolveWithParameters(search_parameters)

            # Print solution on console.
            if solution:
                print_solution(index==0,file,path,data, manager, routing, solution)
            else:
                print("Nada")

            index = index + 1

    exit()

def cria_csv(inicio, nome, qnt_veiculo, total_capacidade, total_distancia, interacao):
    f = open('dataset/analise/analise_Ortools.csv', 'a', newline='', encoding='utf-8')

    # 2. cria o objeto de gravação
    w = csv.writer(f)

    # 3. grava as linhas
    if inicio:
        w.writerow(["Nome", "qnt Veiculos ", "Total Capacidade", "Total Distancia", "qnt Interacao", "Tempo"])
    w.writerow([nome, qnt_veiculo, total_capacidade, total_distancia, interacao, 0])

    # Recomendado: feche o arquivo
    f.close()


if __name__ == '__main__':
    main()
