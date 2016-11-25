from overlap import *

with open('data/test.dna', 'r') as f:
    print(assemble(f.readlines()))