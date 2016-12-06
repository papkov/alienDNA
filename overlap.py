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
    maxlength = 0
    index = 0
    for i, string in enumerate(string_list):
        if s == string:
            continue

        length = overlap(s, string, minoverlap)
        if length > maxlength:
            maxlength = length
            index = i

    return index, maxlength


def build_graph(reads, minoverlap):
    graph = Graph(n=len(reads), directed=True)
    graph.vs["name"] = reads
    graph.es["weight"] = -1
    for i in range(len(reads)):
        j, overlap_length = maximal_overlap(reads[i], reads, minoverlap)
        print("Read %s overlaps read %s on %s position" % (i, j, overlap_length))
        if overlap_length == 0:
            continue
        graph.add_edge(i, j)
        graph[i, j] = overlap_length

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