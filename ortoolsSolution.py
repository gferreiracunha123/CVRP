import tsplib95
from numpy.lib import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def distance(lat1, long1, lat2, long2):
    return euclidean([lat1,long1],[lat2,long2])

def create_data_model():
    """Stores the data for the problem."""
    path = "dataset/E-n22-k4.vrp"

    dataset = tsplib95.load(path)


    distacia_x_y=list(dataset.node_coords.values())
    distacia=[]

    index = 0
    #cria matriz de distancia
    for x in distacia_x_y:
        indey: int  = int(0)
        distaciaux=[]
        for y in distacia_x_y:
            distaciaux.append(euclidean(x,y))
            indey=indey+1
        distacia.append(distaciaux)
        index=index+1

    data = {}
    data['distance_matrix'] =distacia
        #calculate_distance_matrix( list(dataset.node_coords.values()))
    data['demands'] =list(dataset.demands.values())
        #list(dataset.demands.values())
    data['num_vehicles'] = 4
    data['vehicle_capacities'] = [6000] *  data['num_vehicles']
    data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution):
    path = "dataset/E-n22-k4.vrp"

    dataset = tsplib95.load(path)

    distacia_x_y = list(dataset.node_coords.values())
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
            plan_output2 += ' [{0} , {1}]= {2} -> '.format(distacia_x_y[node_index][0], distacia_x_y[node_index][1],data['demands'][node_index])
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)

        plan_output += ' {0} Carga ({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output2 += ' [{0} , {1}]= {2} -> '.format(distacia_x_y[manager.IndexToNode(index)][0], distacia_x_y[manager.IndexToNode(index)][1],
                                                       data['demands'][manager.IndexToNode(index)])
        plan_output += 'Distância da rota: {}m\n'.format(route_distance)
        plan_output += 'Carga da rota: {}\n'.format(route_load)
        print(plan_output)
        print(plan_output2)

        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))

def euclidean(a, b):
    return math.sqrt(pow(a[1] - b[1], 2) + pow(a[0] - b[0], 2))

def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

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
        print_solution(data, manager, routing, solution)
    else:
        print("Nada")
    rou=[]
    rou.append(manager.IndexToNode(routing.Start(0)))
    #print(rou," : ",solution.ObjectiveValue())


if __name__ == '__main__':
    main()