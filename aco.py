import acopy
import seed as seed
import tsplib95
import time
import random
import click

from acopy import ant, solvers, plugins, utils



class add_demand(acopy.solvers.SolverPlugin):

    def __init__(self, delta=1):
        super().__init__(delta=delta)
        self.delta = delta

    def on_iteration(self, state):
        antaux = state.colony.get_ants(self.delta)
#        state.ants.append(antaux)

path = "dataset/E-n22-k4.vrp"

problem = tsplib95.load(path)

G = problem.get_graph()

alpha=2
beta=5
capacidade_feromonio=problem.capacity
quantidade_formigas=4
fator_evaporacao_feromonio=0.8
numero_interacao=1000

seed = seed or str(hash(time.time()))
click.echo(f'SEED={seed}')
random.seed(seed)

colony = ant.Colony(alpha=alpha, beta=beta)
solver = solvers.Solver(rho=fator_evaporacao_feromonio, q=capacidade_feromonio, top=quantidade_formigas)

click.echo(solver)

printout = plugins.Printout()
solver.add_plugin(printout)

timer = plugins.Timer()
solver.add_plugin(timer)

plugin = plugins.Threshold(threshold=784)
#solver.add_plugin(plugin)

recorder = plugins.StatsRecorder()
solver.add_plugin(recorder)

demand = add_demand(1)
solver.add_plugin(demand)


result=solver.solve(G, colony, gen_size=quantidade_formigas, limit=numero_interacao)

click.echo(timer.get_report())
if recorder:
    plotter = utils.plot.Plotter(recorder.stats)
    plotter.plot()
