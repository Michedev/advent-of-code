import argparse
from itertools import product

from path import Path
import abc
import numpy as np

class DefaultParsing:

    @classmethod
    def parse_2dmatrix_single_digit(cls, input_file) -> np.array:
        """
        >>> data = DefaultParsing.parse_2dmatrix_single_digit('input_test.txt')
        >>> np.all(data == np.array([[1,2],[3,4]]))
        True
        """
        with open(input_file) as f:
            data = f.read().split('\n')
        data = [[int(x) for x in row] for row in data]
        return np.array(data)


class DefaultAlgorithms:

    @classmethod
    def get_neighbors_2d_matrix(cls, data, i, j, diagonal=True):
        directions = [(data[i + dx, j + dy], i + dx, j + dy) for dx, dy in product([-1, 0, 1], [-1, 0, 1]) if
                      not (dx == 0 and dy == 0) and (diagonal or ((abs(dx) + abs(dy)) < 2)) and
                      (data.shape[0] > (i + dx) >= 0) and (data.shape[1] > (j + dy) >= 0)]
        return directions


class TemplateSolution(abc.ABC, DefaultParsing, DefaultAlgorithms):

    @classmethod
    @abc.abstractmethod
    def data_path(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def parse(cls, input_file):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def solution1(cls, data):
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def solution2(cls, data):
        raise NotImplementedError()

    @classmethod
    def setup_argparse(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input', dest='input', type=Path)
        parser.add_argument('-2', '--solution2', action='store_true', dest='solution2')
        parser.add_argument('--custom', dest='custom', type=str, default=None)
        parser.add_argument('-e', '--example', action='store_true', dest='example')
        return parser

    @classmethod
    def main(cls):
        parser = cls.setup_argparse()
        args = parser.parse_args()
        day = cls.data_path()
        if args.custom is not None:
            input_file = day / args.custom
        elif args.example:
            input_file = day / 'input_example.txt'
        else:
            input_file = day / 'input.txt'
        data = cls.parse(input_file)
        if args.solution2:
            print(f'solution2(data) = {cls.solution2(data)}')
        else:
            print(f'solution1(data) = {cls.solution1(data)}')


if __name__ == '__main__':
    TemplateSolution.main()
