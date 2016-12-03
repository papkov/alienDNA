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


def assemble(graph):
    # initial = get_initial_vertices(graph)
    # print("Start points:", initial)
    # chains = []
    # for i in initial:
    #     current_vertex = [i]
    #     seq = graph.vs[i]["name"]
    #     next_vertex = graph.neighbors(i, mode=OUT)
    #     print("%s" % i, end='')
    #     while next_vertex:
    #         print(" -> %s" % next_vertex[0], end='')
    #         overlap = graph[current_vertex[0], next_vertex[0]]
    #         seq += graph.vs["name"][next_vertex[0]][overlap:]
    #
    #         current_vertex = next_vertex
    #         next_vertex = graph.neighbors(next_vertex[0], mode=OUT)
    #     chains.append(seq)

    # g.to_undirected()
    # subgraphs = g.decompose()
    # chromosomes = [assemble(g) for g in subgraphs]
    # [sub.diameter() for sub in subgraphs]

    # Drawing
    # visual = {}
    # visual["vertex_size"] = 1
    # [plot(g, target='chomosome%s.png' % i, **visual) for i, g in enumerate(subgraphs)]


    # Strings that do all the work
    diameter = graph.get_diameter()
    dna = "".join([graph.vs["name"][diameter[0]]] + [graph.vs["name"][v][graph[diameter[i], diameter[i + 1]]:] for i, v in enumerate(diameter[1:])])
    validate_assembling(dna, graph.vs["name"])
    # ["%s - %s%%" % (nucl, count_content(nucl, dna)) for nucl in set(dna)]
    return dna

def validate_assembling(strand, reads):
    for read in reads:
        if read not in strand:
            print("ERROR:", read)
            return False
    print("All reads are in strand")
    return True


def count_content(nucl, strand):
    return strand.count(nucl) / len(strand) * 100

if __name__ == '__main__':

    s1 = 'ABCDEFG'
    s2 = 'EFGHIJK'
    s3 = 'QWERTABC'

    print(overlap(s1, s2))
    print(overlap(s1, s3))
    print(overlap(s2, s3))
    print(overlap(s1, 'EFG'))

    g = build_graph([s1, s2, s3, "IJKLMN"])
    print(g)
    print(assemble(g))

    # plot(g)

    # g1 = 'BIBTSTNOBNTNBSNBNTNSISITNIBBITBNIITOOSNNTNBOINOSNNOOBTBOTTITNSONNSBSBNINNNSNBBBTNSISSTONIITBSISONBBTOBINBISOTTONBNBNIOBOTITIONBNTSBNNIOTBBSTBNNISTNNSIOI'
    # g392 = 'NOOBNTNONOBBIBBBNTNBNIBNNBIBNOBSNBTSNTSTTIBBBIOBSISIOTNBONTBNSSSTTTSTNONTSTTTBSBNIBBIBOTSNINNOISBBSOTNNTTNBBNTNTNONBONIIITIOTISITNSTTNBNIOONIOOTISNNNNSOB'
    #
    # print(overlap(g1, g392))