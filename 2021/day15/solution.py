from dataclasses import dataclass
from path import Path
from template import TemplateSolution
import networkx as nx
import matplotlib.pyplot as plt

import sys
for folder in Path(__file__).parent.dirs():
    for folder in folder.dirs():
        if folder.name.startswith('day'):
            sys.path.append(str(folder))

@dataclass
class Data:

    graph: nx.DiGraph
    num_rows: int
    row_length: int


class Solution(TemplateSolution, year=2021, day=15):

    
    def data_path(self):
        return Path(__file__).parent

    
    def parse(self, input_file):
        print(input_file)
        self.is_example = input_file.basename() == 'input_example.txt'
        with open(input_file) as f:
            data = [[int(x) for x in line] for line in f.read().split('\n') if line]
        row_length = len(data[0])
        num_rows = len(data)
        graph = nx.DiGraph(row_length=row_length, num_rows=num_rows)
        for i, line in enumerate(data):
            for j, c in enumerate(line):
                graph.add_node((i,j), value=c)
                if i > 0:
                    graph.add_edge((i-1, j), (i, j), weight=c)
                if j > 0:
                    graph.add_edge((i, j-1), (i, j), weight=c)
                if i < num_rows - 1:
                    graph.add_edge((i+1, j), (i, j) , weight=c)
                if j < row_length - 1:
                    graph.add_edge((i, j+1), (i, j), weight=c)
        # if self.is_example:
        #     values = nx.get_node_attributes(graph,'value')
        #     labels = nx.get_edge_attributes(graph,'weight')
        #     nx.draw(graph, labels=values)
        #     nx.draw_networkx_edge_labels(graph, edge_labels=labels) # show weights along the edges
        #     plt.savefig(Path(__file__).parent / 'graph.png')
        
        return Data(graph, num_rows, row_length)

    
    def solution1(self, data: Data):
        graph = data.graph
        
        sequence = nx.algorithms.dijkstra_path(graph, (0, 0) , (data.num_rows - 1, data.row_length - 1))
        result = sum(graph.nodes[node]['value'] for node in sequence[1:])
        
        if not self.is_example:
            assert result < 494, 'result is too high: {}'.format(result)
            assert result != 469, 'result should be different from 469'
            assert result == 487, 'result should be from 487, it is {}'.format(result)
        return result

    
    def solution2(self, data: Data):
        """
        The entire cave is actually five times larger in both dimensions than you thought; the area you originally scanned is just one tile in a 5x5 tile area that forms the full map. Your original map tile repeats to the right and downward; each time the tile repeats to the right or downward, all of its risk levels are 1 higher than the tile immediately up or left of it. However, risk levels above 9 wrap back around to 1. So, if your original map had some position with a risk level of 8, then that same position on each of the 25 total tiles would be as follows:

        8 9 1 2 3
        9 1 2 3 4
        1 2 3 4 5
        2 3 4 5 6
        3 4 5 6 7

        Each single digit above corresponds to the example position with a value of 8 on the top-left tile. Because the full map is actually five times larger in both dimensions, that position appears a total of 25 times, once in each duplicated tile, with the values shown above.
        """
        graph = data.graph
        num_rows = data.num_rows
        row_length = data.row_length
        for i in range(num_rows * 5):
            start = 0 if i >= num_rows else row_length
            for j in range(start, row_length * 5):
                value = graph.nodes[(i % num_rows, j % row_length)]['value'] + i // num_rows + j // row_length
                if value > 9:
                    value = value % 9
                graph.add_node((i, j), value=value)
                if i > 0:
                    graph.add_edge((i-1, j), (i, j), weight=value)
                if j > 0:
                    graph.add_edge((i, j-1), (i, j), weight=value)
                if i < num_rows * 5 - 1:
                    graph.add_edge((i+1, j), (i, j) , weight=value)
                if j < row_length * 5 - 1:
                    graph.add_edge((i, j+1), (i, j), weight=value)
        sequence = nx.algorithms.dijkstra_path(graph, (0, 0) , (num_rows * 5 - 1, row_length * 5 - 1))
        result = sum(graph.nodes[node]['value'] for node in sequence[1:])
        return result
                

if __name__ == '__main__':
    Solution.main()
