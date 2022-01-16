import re
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np
from path import Path
from collections import namedtuple

from template import TemplateSolution

Data = namedtuple('Data', ['points', 'splits'])


class Day13Solution(TemplateSolution):
    @classmethod
    def data_path(cls):
        return Path(__file__).parent

    @classmethod
    def parse(cls, input_file):
        with open(input_file) as f:
            data = f.read().split('\n')
        i = 0
        points = set()
        while data[i]:
            x, y = data[i].split(',')
            points.add((int(x), int(y)))
            i += 1
        i += 1
        regex_split = re.compile(r'fold along (?P<axis>[xy])=(?P<position>\d+)')
        splits = []
        while i < len(data):
            row_match = regex_split.match(data[i])
            axis = row_match.group('axis')
            assert axis in ('x', 'y'), axis
            axis = 0 if axis == 'x' else 1
            position = int(row_match.group('position'))
            splits.append((axis, position))
            i += 1
        return Data(points, splits)

    @classmethod
    def fold(cls, points: set, axis: int, pos: int):
        assert axis in (0, 1)
        above_points = set()
        below_points = set()
        for p in points:
            if p[axis] > pos:
                below_points.add(p)
            else:
                above_points.add(p)
        for x, y in below_points:
            if axis == 0:
                mapped_point = ((2 * pos) - x, y)
            else:
                mapped_point = (x, (2 * pos) - y)
            above_points.add(mapped_point)
        return above_points

    @classmethod
    def solution1(cls, data: Data):
        points = data.points
        for axis, pos in data.splits:
            points = cls.fold(points, axis, pos)
            return len(points)

    @classmethod
    def solution2(cls, data: Data):
        points = data.points.copy()
        for axis, pos in data.splits:
            points = cls.fold(points, axis, pos)
        x_size: int = max(x for x, y in points) + 1
        y_size: int = max(y for x, y in points) + 1
        matrix = np.zeros((x_size, y_size), dtype=bool)
        for x, y in points:
            matrix[x, y] = True
        matrix = np.transpose(matrix, (1, 0))
        plt.imshow(matrix)
        plt.savefig(cls.data_path() / 'solution2.png')
        plt.close()
        result = '\n'
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if matrix[i, j]:
                    result += '#'
                else:
                    result += '.'
            result += '\n'
        return result


if __name__ == '__main__':
    Day13Solution.main()
