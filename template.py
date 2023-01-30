import argparse
from itertools import product

from path import Path
import abc
import numpy as np

_registry = {}

def get_solution_instance(year, day):
    return _registry[(year, day)]()

class DefaultParsing:

    
    def parse_2dmatrix_single_digit(self, input_file) -> np.array:
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

    
    def get_neighbors_2d_matrix(self, data, i, j, diagonal=True):
        directions = [(data[i + dx, j + dy], i + dx, j + dy) for dx, dy in product([-1, 0, 1], [-1, 0, 1]) if
                      not (dx == 0 and dy == 0) and (diagonal or ((abs(dx) + abs(dy)) < 2)) and
                      (data.shape[0] > (i + dx) >= 0) and (data.shape[1] > (j + dy) >= 0)]
        return directions


class TemplateSolution(DefaultParsing, DefaultAlgorithms):

    verbose = False

    def __init_subclass__(cls, year=None, day=None, **kwargs):
        super().__init_subclass__(**kwargs)
        _registry[(year, day)] = cls

    
    @abc.abstractmethod
    def data_path(self):
        """
        Data path for the day
        """
        pass

    
    @abc.abstractmethod
    def parse(self, input_file):
        """
        Parse the input file
        """
        raise NotImplementedError()

    
    @abc.abstractmethod
    def solution1(self, data):
        raise NotImplementedError()

    
    @abc.abstractmethod
    def solution2(self, data):
        raise NotImplementedError()

    @staticmethod    
    def setup_argparse():
        parser = argparse.ArgumentParser()
        parser.add_argument('-2', '--solution2', action='store_true', dest='solution2', help='Run solution to part 2')
        parser.add_argument('--custom', dest='custom', type=str, default=None,
                            help='Use a custom input file (e.g. input_test.txt)')
        parser.add_argument('-e', '--example', action='store_true', dest='example',
                            help='Use the example input file (e.g. input_example.txt)')
        parser.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                            help='Verbose output')
        parser.add_argument('-y', '--year', dest='year', type=int, required=True,
                            help='Solution year (e.g. 2021)')  # e.g. 2021
        parser.add_argument('-d', '--day', dest='day', type=int, required=True,
                            help="Solution day (e.g. 1)")  # e.g. 1

        return parser

    
    def main(self):
        parser = self.setup_argparse()
        args = parser.parse_args()
        day = self.data_path()
        if args.verbose:
            self.verbose = True
        if args.custom is not None:
            input_file = day / args.custom
        elif args.example:
            input_file = day / 'input_example.txt'
        else:
            input_file = day / 'input.txt'
        data = self.parse(input_file)
        if args.solution2:
            print(f'solution2(data) = {self.solution2(data)}')
        else:
            print(f'solution1(data) = {self.solution1(data)}')

    
    def parse_solution1(self, input_file: str):
        day = self.data_path()
        input_path = day / input_file
        data = self.parse(input_path)
        return self.solution1(data)

    
    def parse_solution2(self, input_file: str):
        day = self.data_path()
        input_path = day / input_file
        data = self.parse(input_path)
        return self.solution2(data)
