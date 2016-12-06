from overlap import *

# Build graph
# with open('data/alien.dna', 'r') as f:
#     reads = [line.strip() for line in f.readlines()]
#     g = build_graph(reads, 40)
#     # Remove weak edges
#     g.delete_edges([i for i, w in enumerate(g.es['weight']) if w < 20])
#     g.write_graphmlz('output/alien_graph_full.gmlz')


# Loading graph
# g = Graph.Read_GraphMLz('output/alien_graph.gmlz')
g = Graph.Read_GraphMLz('output/alien_graph_full.gmlz')
# g = Graph.Read_GraphMLz('output/test_graph.gmlz')
print('Graph was loaded.')

# Delete weak edges
g.delete_edges([i for i, w in enumerate(g.es['weight']) if w < 20])
g.summary()

# Graph decomposition
g_plain = g.as_undirected()
g_plain.es['weight'] = g.es['weight']
# Select only subgraphs with edges
subgraphs = [subgraph for subgraph in g_plain.decompose() if subgraph.ecount() != 0]


print('I am going to assemble %s subgraphs\n' % len(subgraphs))
strands = []
for i, subgraph in enumerate(subgraphs):
    print('%s.' % i)
    print(subgraph.summary())
    if is_cyclic(subgraph):
        print("This graph is cyclic")
        path_in_subgraph = get_cyclic_path(subgraph)
    else:
        path_in_subgraph = subgraph.get_diameter()\

    path = convert_path(path_in_subgraph, subgraph, g)
    dna = assemble_by_path(g, path)
    # If all reads from subgraph are in strand, save chromosome
    if validate_assembling(dna, subgraph.vs['name'], path_in_subgraph):
        with open('output/assembled_chromosome%s' % i, 'w') as f:
            f.write(dna)
    print("Assembled %s nucleotides\n" % (len(dna)))
    strands.append(dna)