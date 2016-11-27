from igraph import *

def overlap(s1, s2):
    """
    :param s1: first string
    :param s2: second string
    :return: string which two input strings are substrings of or the longest string if there is no overlap

    >>> overlap('ABCDEFG', 'EFGHIJK')
    ABCDEFGHIJK
    >>> overlap('ABCDEFG', 'QWERTABC')
    QWERTABCDEFG
    >>> overlap('EFGHIJK', 'QWERTABC')
    None
    """
    maxoverlap = 0
    # forward = False
    # # Swap strings: s1 should be the shortest one
    # if s1 > s2:
    #     s1, s2 = s2, s1

    # TODO: reverse directions
    # Backward
    # for i in range(1, len(s1)):
    #     # print(s1[:i], s2[-i:])
    #     if s1[:i] == s2[-i:] and i > maxoverlap:
    #         maxoverlap = i
    #         forward = False
    # Forward
    for i in range(1, len(s1)):
        # print(s2[:i], s1[-i:])
        if i == len(s2):
            break
        if s2[:i] == s1[-i:] and i > maxoverlap:
            maxoverlap = i
            # forward = True

    # If there is no overlap
    return maxoverlap


def maximal_overlap(s, string_list):
    maxlength = 0
    index = 0
    for i, string in enumerate(string_list):
        if s == string:
            continue

        length = overlap(s, string)
        if length > maxlength:
            maxlength = length
            index = i

    return index, maxlength


def build_graph(reads):
    graph = Graph(n=len(reads), directed=True)
    graph.vs["name"] = reads
    graph.es["weight"] = -1
    for i in range(len(reads)):
        j, overlap_length = maximal_overlap(reads[i], reads)
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


def assemble(graph):
    initial = get_initial_vertices(graph)
    print("Start points:", initial)
    chains = []
    for i in initial:
        current_vertex = [i]
        seq = graph.vs[i]["name"]
        next_vertex = graph.neighbors(i, mode=OUT)
        print("%s" % i, end='')
        while next_vertex:
            print(" -> %s" % next_vertex[0], end='')
            overlap = graph[current_vertex[0], next_vertex[0]]
            seq += graph.vs["name"][next_vertex[0]][overlap:]

            current_vertex = next_vertex
            next_vertex = graph.neighbors(next_vertex[0], mode=OUT)
        chains.append(seq)
    return chains

if __name__ == '__main__':

    s1 = 'ABCDEFG'
    s2 = 'EFGHIJK'
    s3 = 'QWERTABC'

    print(overlap(s1, s2))
    print(overlap(s1, s3))
    print(overlap(s2, s3))
    print(overlap(s1, 'EFG'))

    g = build_graph([s1, s2, s3])
    print(g)
    print(assemble(g))

    # plot(g)

    # g1 = 'BIBTSTNOBNTNBSNBNTNSISITNIBBITBNIITOOSNNTNBOINOSNNOOBTBOTTITNSONNSBSBNINNNSNBBBTNSISSTONIITBSISONBBTOBINBISOTTONBNBNIOBOTITIONBNTSBNNIOTBBSTBNNISTNNSIOI'
    # g392 = 'NOOBNTNONOBBIBBBNTNBNIBNNBIBNOBSNBTSNTSTTIBBBIOBSISIOTNBONTBNSSSTTTSTNONTSTTTBSBNIBBIBOTSNINNOISBBSOTNNTTNBBNTNTNONBONIIITIOTISITNSTTNBNIOONIOOTISNNNNSOB'
    #
    # print(overlap(g1, g392))