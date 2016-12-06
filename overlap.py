from igraph import *


def overlap(s1, s2, minoverlap):
    position = minoverlap
    while position < len(s2):
        position = s1.find(s2[:minoverlap], position)
        if position == -1:
            return 0
        elif s2.startswith(s1[position:]):
            return len(s1) - position
        position += 1
    return 0


def maximal_overlap(s, string_list, minoverlap):
    overlaps = []

    for i, string in enumerate(string_list):
        if s == string:
            continue

        length = overlap(s, string, minoverlap)
        if length != 0:
            overlaps.append((i, length))

    return overlaps


def build_graph(reads, minoverlap):
    graph = Graph(n=len(reads), directed=True)
    graph.vs["name"] = reads
    graph.es["weight"] = -1
    for i in range(len(reads)):
        overlaps = maximal_overlap(reads[i], reads, minoverlap)
        for o in overlaps:
            print("Read %s overlaps read %s on %s position" % (i, o[0], o[1]))
            if o[1] == 0:
                continue
            graph.add_edge(i, o[0])
            graph[i, o[0]] = o[1]

    print("Graph was built")
    return graph


def get_initial_vertices(graph):
    degrees = graph.degree(mode=IN)
    initial = []
    for i, d in enumerate(degrees):
        if d == 0:
            initial.append(i)
    return initial


def assemble_by_path(graph, path):
    reads = graph.vs['name']
    reads_without_overlaps = [reads[path[0]]]
    o_sum = 0
    # Check if path is reversed
    for i in range(1, len(path)):
        try:
            graph.get_eid(path[i-1], path[i])
        except InternalError:
            print('Path is reversed!')
            path = path[::-1]
            break

    for i in range(1, len(path)):
        current = path[i]
        previous = path[i-1]
        # If there is no such edge, it will raise exception
        try:
            edge = graph.get_eid(previous, current)
        except InternalError:
            edge = graph.get_eid(current, previous)

        overlap = int(graph.es[edge]['weight'])
        # if i < 10:
        #     print(i, previous, current, edge, overlap)
        reads_without_overlaps.append(reads[current][overlap:])

        o_sum += overlap
        if overlap < 30:
            print("Small overlap detected: node %s - %s nucleotides" % (current, overlap))
    print('Overlap sum: %s' % o_sum)
    dna = "".join(reads_without_overlaps)
    return dna


def validate_assembling(strand, reads, path):
    missing_reads = []
    for v in path:
        if reads[v] not in strand:
            # print("ERROR:", v, reads[v])
            missing_reads.append(v)
    if not missing_reads:
        print("All reads are in strand")
        return True
    else:
        print("There are %s missing reads" % len(missing_reads), missing_reads)


def count_content(nucl, strand):
    return strand.count(nucl) / len(strand) * 100


def get_initial_nodes(graph):
    # Check nodes' degree in graph. If each degree is equal to 2, graph is cyclic
    return [(i, d) for i, d in enumerate(graph.degree()) if d != 2]


def is_cyclic(graph):
    return get_initial_nodes(graph) == []


def get_cyclic_path(graph):
    path = [graph.vs[0].index]
    while True:
        neighbours = graph.vs[path[-1]].neighbors()
        for n in neighbours:
            if n.index not in path:
                next_node = n.index
                break
        # If all neighbours are in path already
        else:
            return path
        path.append(next_node)


def convert_path(path_in_subgraph, subgraph, mother_graph):
    names = [subgraph.vs[v]['name'] for v in path_in_subgraph]
    vertices_ind = [v.index for v in subgraph.vs]

    # Check if path if full
    missing = list(set(vertices_ind) - set(path_in_subgraph))
    if missing:
        print('Path does not content %s vertices:' % len(missing), missing)
    return [mother_graph.vs.find(name=name_).index for name_ in names]


def simplify(graph):
    g = graph.copy()
    redundant_vertices = set()
    for v in g.vs.select(_degree_ne=2):
        # print(j, len(redundant_vertices))
        print(v.index)
        if v.index in redundant_vertices:
            continue

        this_v = v
        next_v = this_v.neighbors(mode=OUT)
        # print(next_v)
        while len(next_v) == 1:
            # if next_v[0].index in redundant_vertices:
            #     break

            try:
                edge = g.get_eid(this_v.index, next_v[0].index)
            except InternalError:
                print('There is no edge %s -> %s' % (this_v.index, next_v[0].index))
                break

            overlap = int(g.es[edge]['weight'])
            v['name'] += next_v[0]['name'][overlap:]

            if this_v.index != v.index:
                redundant_vertices.add(this_v.index)
            this_v = next_v[0]
            next_v = this_v.neighbors(mode=OUT)

        # There was more than one step
        # if v.neighbors(mode=OUT)[0].index != this_v.index:
        # g.add_edge(v.index, this_v.index)
        # g.vs[v.index]['name'] = temp_strand
        # print('%s redundant vertices will be removed' % len(redundant_vertices))

        # Remove redundant vertices
    print('%s redundant vertices will be removed' % len(redundant_vertices))
    g.delete_vertices(list(redundant_vertices))
    print(len(g.vs.select(_degree_eq=2)))
    return g


def find_closest_important_node(g, start):
    path = []
    if start not in g.vs.index:
        print('There is no such node')
        return path
    this_node = start
    next_node = g.neighbors(mode=IN)
    while len(next_node) == 1:
        if this_node != start:
            path.append(this_node)
    return path


# if __name__ == '__main__':
#
#     s1 = 'ABCDEFG'
#     s2 = 'EFGHIJK'
#     s3 = 'QWERTABC'
#
#     print(overlap(s1, s2))
#     print(overlap(s1, s3))
#     print(overlap(s2, s3))
#     print(overlap(s1, 'EFG'))
#
#     g = build_graph([s1, s2, s3, "IJKLMN"])
#     print(g)
#     # print(assemble(g))
#
#     # plot(g)
#
#     # g1 = 'BIBTSTNOBNTNBSNBNTNSISITNIBBITBNIITOOSNNTNBOINOSNNOOBTBOTTITNSONNSBSBNINNNSNBBBTNSISSTONIITBSISONBBTOBINBISOTTONBNBNIOBOTITIONBNTSBNNIOTBBSTBNNISTNNSIOI'
#     # g392 = 'NOOBNTNONOBBIBBBNTNBNIBNNBIBNOBSNBTSNTSTTIBBBIOBSISIOTNBONTBNSSSTTTSTNONTSTTTBSBNIBBIBOTSNINNOISBBSOTNNTTNBBNTNTNONBONIIITIOTISITNSTTNBNIOONIOOTISNNNNSOB'
#     #
#     # print(overlap(g1, g392))