from overlap import *
from plot_graphs import *


def path_is_cyclic(path):
    return path[0] == path[-1]


def build_full_path(g, initial_node):
    vertices = {v.index: v.degree(mode=OUT) for v in g.vs}
    print(vertices)
    path = [initial_node]
    vertices[initial_node] -= 1
    current = initial_node
    neighbors = g.neighbors(current, mode=OUT)

    # While there are next neighbors and path haven't cycled
    while neighbors:
        print(current)
        if len(neighbors) == 1:
            current = neighbors[0]
            neighbors = g.neighbors(current, mode=OUT)

            path.append(current)
            vertices[current] -= 1
        else:
            short_paths = []
            print('Observe neighbors of %s:' % current, neighbors)
            for neighbor in neighbors:
                if vertices[neighbor] != 0:
                    short_paths.append(build_full_path(g, neighbor))

            cyclic = []
            acyclic = []
            print(short_paths)
            for short_path in short_paths:
                if path_is_cyclic(short_path):
                    cyclic += short_path
                else:
                    acyclic += short_path
            # Cyclic first
            print('cyclic', cyclic)
            for c in cyclic:
                path.append(c)
                vertices[c] -= 1
            print('acyclic', acyclic)
            for c in acyclic:
                path.append(c)
                vertices[c] -= 1
            current = path[-1]
            neighbors = g.neighbors(current, mode=OUT)

        vertices[path[-1]] -= 1
        print('path', path)

        if path_is_cyclic(path):
            break

    return path


if __name__ == '__main__':
    g = Graph(directed=True)
    g.add_vertices(range(12))
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 5)
    g.add_edge(5, 2)
    g.add_edge(2, 6)
    g.add_edge(6, 7)
    g.add_edge(7, 8)
    g.add_edge(8, 9)
    g.add_edge(9, 7)
    g.add_edge(9, 10)
    g.add_edge(10, 11)

    print(g.neighbors(2, mode=OUT)[0])

    # Get nodes with 1 outer arrow and no inner
    initial_nodes = [v.index for v in g.vs if v.degree(mode=OUT) == 1 and v.degree(mode=IN) == 0]
    print('I am going to start travelling from %s nodes' % len(initial_nodes), initial_nodes)

    # List of full paths in graph (each path starts from initial node)
    # paths = [[init] for init in initial_nodes]
    for i in initial_nodes:
        print(build_full_path(g, i))

    plot_graph(g)
    plot_graph(g.linegraph())




