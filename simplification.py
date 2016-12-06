from overlap import *
from plot_graphs import *

g = Graph.Read_GraphMLz('output/alien_graph_full.gmlz')
# g = Graph.Read_GraphMLz('output/test_graph.gmlz')
g_s = simplify(g)
print(g_s.summary())
plot_graph(g_s)
print([len(name) for name in g_s.vs['name']])