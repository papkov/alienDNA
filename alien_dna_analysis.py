from overlap import *

with open('data/test.dna', 'r') as f:
    # Prepare your data
    reads = [line.strip() for line in f.readlines()]
    g = build_graph(reads)
    print(g.summary())
    # plot(g)
    alien = assemble(g)

    print(alien)

    with open('output/assembled_test_1.dna', 'w') as out:
        out.writelines(alien)