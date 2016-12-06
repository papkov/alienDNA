from igraph import plot


def plot_graph(graph, file=""):
    graph = graph.as_undirected()
    visual = dict()
    color_dict = {0: "pink", 1: "red", 2: "black", 3: "green", 4: "blue"}
    size_dict = {0: 7, 1: 7, 2: 1, 3: 7, 4: 7}
    visual['vertex_color'] = [color_dict[degree] for degree in graph.degree()]
    visual["vertex_size"] = [size_dict[degree] for degree in graph.degree()]
    if file:
        return plot(graph, **visual, target=file)
    return plot(graph, **visual)


def plot_graphs(graphs, common_name):
    return [plot_graph(g, file='%s%s.svg' % (common_name, i)) for i, g in enumerate(graphs)]


def plot_simplified(graph):
    g = graph.copy()

