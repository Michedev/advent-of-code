from path import Path
from template import TemplateSolution
import networkx as nx
import matplotlib.pyplot as plt

class Solution(TemplateSolution):

    @classmethod
    def data_path(cls):
        return Path(__file__).parent

    @classmethod
    def parse(cls, input_file):
        print(input_file)
        cls.is_example = input_file.basename() == 'input_example.txt'
        with open(input_file) as f:
            data = [[int(x) for x in line] for line in f.read().split('\n') if line]
        graph = nx.DiGraph()
        id_node = 0
        row_length = len(data[0])
        num_rows = len(data)
        for i, line in enumerate(data):
            for j, c in enumerate(line):
                graph.add_node(id_node, value=c)
                if i > 0:
                    graph.add_edge(id_node - row_length, id_node, weight=c)
                if j > 0:
                    graph.add_edge(id_node - 1, id_node, weight=c)
                if i < num_rows - 1:
                    graph.add_edge(id_node + row_length, id_node , weight=c)
                if j < row_length - 1:
                    graph.add_edge(id_node + 1, id_node, weight=c)
                id_node += 1
        if cls.is_example:
            values = nx.get_node_attributes(graph,'value')
            labels = nx.get_edge_attributes(graph,'weight')
            nx.draw(graph, pos={node: (node % row_length, node // row_length) for node in graph.nodes}, labels=values)
            nx.draw_networkx_edge_labels(graph, pos={node: (node % row_length, node // row_length) for node in graph.nodes}, edge_labels=labels) # show weights along the edges
            plt.savefig(Path(__file__).parent / 'graph.png')
        
        return graph

    @classmethod
    def solution1(cls, graph):
        sequence = nx.algorithms.dijkstra_path(graph, 0 , len(graph.nodes) - 1)
        result = sum(graph.nodes[node]['value'] for node in sequence[1:])
        
        if not cls.is_example:
            assert result < 494, 'result is too high: {}'.format(result)
            assert result != 469, 'result should be different from 469'
            assert result == 487, 'result should be from 487, it is {}'.format(result)
        return result

    @classmethod
    def solution2(cls, data):
        raise NotImplementedError()

if __name__ == '__main__':
    Solution.main()
