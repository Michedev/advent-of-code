import networkx as nx
import unittest
import doctest
from charger_chain import ChargerChain


if __name__ == "__main__":
    c = ChargerChain('input.txt')
    # s1, s2 = c.find_chain()
    # print('solution1 is', s1 * s2)
    print('solution2 is', c.num_combinations())