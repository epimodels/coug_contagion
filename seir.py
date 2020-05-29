import networkx as nx
import matplotlib.pyplot as plt
import EoN
import random
from collections import defaultdict

## Create Population Network
N = 25000
G = nx.watts_strogatz_graph(N,4,0.01,seed=59202)

## Set Node and Edge Transition Weights
# Note at present this is not used - could be used to make some individuals immune (due to previous infection etc.)

node_attribute_dict = {node: 1 for node in G.nodes()}
edge_attribute_dict = {edge: 1 for edge in G.edges()}

nx.set_node_attributes(G, values=node_attribute_dict, name='expose2infect_weight')
nx.set_edge_attributes(G, values=edge_attribute_dict, name='transmission_weight')

## Build SEIR Transition Graph
# Neighbor-independent Transitions
H = nx.DiGraph()
H.add_node('S') 
H.add_edge('E', 'I', rate = 0.6, weight_label='expose2infect_weight') #speed is 0.6*weight
H.add_edge('I', 'R', rate = 0.01)

# Neighbor-dependent Transitions
J = nx.DiGraph()
J.add_edge(('I', 'S'), ('I', 'E'), rate = 0.5, weight_label='transmission_weight')

## Set Initial Conditions
IC = defaultdict(lambda: 'S')

random_infected = random.sample(list(G.nodes),k=1)
for node in random_infected:
    IC[node] = 'I'

return_statuses = ('S', 'E', 'I', 'R')

epidemic = EoN.Gillespie_simple_contagion(G, H, J, IC, return_statuses,
                                        tmax = float('Inf'),return_full_data=True)


# Simple sample plotting
plt.plot(epidemic.t(),epidemic.I())
plt.savefig('epidemic_curve.png')