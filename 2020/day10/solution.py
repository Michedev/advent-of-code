import networkx as nx
import unittest
import doctest
from charger_chain import ChargerChain

def draw_graph(g):
    import matplotlib.pyplot as plt
    import numpy as np
    l = nx.random_layout(g)
    delta = 0.15
    for n in list(l.keys()):
       l[n] = np.array([delta * n, 0.0])
    nx.draw_networkx(g, l)
    nx.draw_networkx_edges(g, l, edgelist=[e for e in g.edges if abs(e[1] - e[0]) > 1], connectionstyle="arc3,rad=0.3")
    plt.savefig('graph.png')
    plt.close()


if __name__ == "__main__":
    c = ChargerChain('input.txt')
    # s1, s2 = c.find_chain()
    # print('solution1 is', s1 * s2)
    print('solution2 is', c.num_combinations())