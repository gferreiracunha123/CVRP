import acopy
import seed as seed
import tsplib95
import time
import random
import click
from os import listdir
from os.path import isfile, join

from acopy import ant, solvers, plugins, utils
from numpy.lib import math


class add_demand(acopy.solvers.SolverPlugin):

    def __init__(self, delta=1):
        super().__init__(delta=delta)
        self.delta = delta

    def on_iteration(self, state):
        antaux = state.colony.get_ants(self.delta)
#        state.ants.append(antaux)


path = "dataset/A-n32-k5.vrp"

problem = tsplib95.load(path)

G = problem.get_graph()

seed = seed or str(hash(time.time()))
click.echo(f'SEED={seed}')
random.seed(seed)

colony = ant.Colony(alpha=2, beta=5)
solver = solvers.Solver(rho=0.8, q=problem.capacity, top=5)

click.echo(solver)

printout = plugins.Printout()
click.echo(f'Registering plugin: {printout}')
solver.add_plugin(printout)

timer = plugins.Timer()
click.echo(f'Registering plugin: {timer}')
solver.add_plugin(timer)

plugin = plugins.Threshold(threshold=784)
click.echo(f'Registering plugin: {plugin}')
solver.add_plugin(plugin)

recorder = plugins.StatsRecorder()
click.echo(f'Registering plugin: {recorder}')
solver.add_plugin(recorder)

demand = add_demand(1)
solver.add_plugin(demand)
click.echo(f'Registering plugin: {demand}')

solver.solve(G, colony, gen_size=1, limit=50)

click.echo(timer.get_report())
if recorder:
    plotter = utils.plot.Plotter(recorder.stats)
    plotter.plot()
