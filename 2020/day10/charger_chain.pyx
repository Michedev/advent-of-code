import networkx as nx

from libc.stdlib cimport malloc, free


cdef class ChargerChain:

    """
    >>> c1 = ChargerChain('input_example.txt')
    >>> c1.find_chain()
    (7, 5)
    >>> c2 = ChargerChain('input_example2.txt')
    >>> c2.find_chain()
    (22, 10)
    >>> c = ChargerChain([0, 1, 2, 3, 6])
    >>> list(c._build_graph().edges)
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 6)]
    >>> c.num_combinations()
    4
    >>> c1.num_combinations()
    8
    >>> c2.num_combinations()
    19208
    """

    cdef list data

    def __cinit__(self, data_path: str | list):
        if isinstance(data_path, str):
            self.data = self._parse_data(data_path)
        elif isinstance(data_path, list):
            self.data = data_path
        else:
            raise TypeError('data_path must be a list or a str')

    def _parse_data(self, dpath: str):
        with open(dpath) as f:
            data = sorted([int(x) for x in f.read().split('\n')] + [0])
            data.append(data[-1] + 3)
            return data

    def _build_graph(self):
        """
        Return a graph of input number where the edge u -> v exists iff |v - u| <= 3
        >>> c = ChargerChain([1, 2, 3, 5])

        >>> edges = list(c._build_graph().edges)
        >>> edges
        [(1, 2), (1, 3), (2, 3), (2, 5), (3, 5)]
        """
        g = nx.DiGraph()
        for i in range(len(self.data)-1):
            g.add_edge(self.data[i], self.data[i+1])
            for j in range(i+2, i+4):
                if j < len(self.data) and (self.data[j] - self.data[i]) <= 3:
                    g.add_edge(self.data[i], self.data[j])
        return g

    def find_chain(self):
        diff1 = diff3 = 0
        for i in range(len(self.data)-1):
            d, d_next = self.data[i], self.data[i+1]
            if (d_next - d) == 1:
                diff1 += 1
            elif (d_next - d) == 3:
                diff3 += 1
        return diff1, diff3

    L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL