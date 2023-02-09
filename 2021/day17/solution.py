from collections import namedtuple
from math import ceil, sqrt
from typing import Tuple

from numpy import sign
from template import TemplateSolution
from path import Path
import re

x_solution = namedtuple('x_solution', ['x_first_0', 'num_steps', 'always_zero'])
y_solution = namedtuple('y_solution', ['y_first_0', 'num_steps'])

class Solution(TemplateSolution, day=17, year=2021):

    regex_data = re.compile(r"target area: x=([-]{0,1}\d+)\.\.([-]{0,1}\d+), y=([-]{0,1}\d+)\.\.([-]{0,1}\d+)")
    is_example = False

    def data_path(self):
        return Path(__file__).parent

    def parse(self, input_file):
        """
        from the line "target area: x=150..193, y=-136..-86" using regex, in particular extracting the 4 numbers as x_a=150, x_b=193, y_a=-136, y_b=-86
        """
        with open(input_file) as f:
            line = f.read()
        data = self.regex_data.findall(line)
        data = [int(x) for x in data[0]]
        assert len(data) == 4
        if input_file.endswith('example.txt'):
            self.is_example = True
        return data
        
    def get_max_y_t(self, y_first_0: int):
        """
        Given initial velocity, return the max y value reached
        """
        if y_first_0 <= 0:
            return 0
        return y_first_0 * (y_first_0 + 1) / 2

    def is_in_bound(self, y_first_0, y_a, y_b):
        y_max = self.get_max_y_t(y_first_0)
        # change of coordinates wrt y_max
        y_a = y_a + y_max
        y_b = y_b + y_max
        if y_a > y_b:
            y_a, y_b = y_b, y_a
        c = 0
        i = 1
        while c < y_a:
            c += i
            i += 1
        return c <= y_b
    
    def is_in_bound2(self, y_first_0, y_a, y_b):
        """
        Given initial velocity, return if the max y value reached is in the target area

        """
        y_t = 0
        t = 0
        t_solutions = []
        if self.verbose:
            print('testing y_first_0 =', y_first_0)
        while y_t >= y_a:
            y_t = y_first_0 * t - (t * (t - 1)) / 2
            if y_t >= y_a and y_t <= y_b:
                t_solutions.append(t)
            t += 1
            if self.verbose:
                print('\t', 't', t, 'y_t', y_t)
        return t_solutions       

    def solution1(self, data: Tuple[int, int, int, int]):
        x_a, x_b, y_a, y_b = data
        y_max_value = 0
        for y_first_0 in range(1, max(abs(y_a), abs(y_b))):  # todo: find better range. IMO should be something like logarithmic
            if self.is_in_bound(y_first_0, y_a, y_b):
                curr_max = self.get_max_y_t(y_first_0)
                if self.verbose: 
                    print("y_first_0", y_first_0, 'is in bound')
                    print("curr_max", curr_max)
                if y_max_value < curr_max:
                    y_max_value = curr_max
        return int(y_max_value)

    def solution2(self, data: Tuple[int, int, int, int]):
        x_a, x_b, y_a, y_b = data
        y_max_value = 0
        counter_obvious_solutions = (y_b - y_a + 1) * (x_b - x_a + 1)  # obvious solutions, the number of points in the target area
        # the possible x are all the divisors of x_b - x_a + 1
        if self.verbose:
            print('=============')
            print('obvious solutions')
            for x in range(x_a, x_b + 1):
                for y in range(y_a, y_b + 1):
                    print(f'({x}, {y})')
            print('=============')
        x_solutions = set()
        for x_first_0 in range(2, x_a):
            # if can possibly reach the bound, then consider it
            reaches_bound = (x_first_0 * (x_first_0 + 1) / 2) >= x_a
            if reaches_bound:
                # simulate x trajectory and check if it is in bound of [x_a, x_b]
                x_t_solutions = self.x_is_in_bound(x_first_0, x_a, x_b)
                for x_t_solution, x_t_is_zero in x_t_solutions: 
                    x_solutions.add(x_solution(x_first_0, x_t_solution, x_t_is_zero))
        y_solutions = set()
        for y_first_0 in range(-min(abs(y_a), abs(y_b)), max(abs(y_a), abs(y_b))):
            y_t_solutions = self.is_in_bound2(y_first_0, y_a, y_b)
            for t_solution in y_t_solutions:
                y_solutions.add(y_solution(y_first_0, t_solution))
        if self.verbose:
            print('x_solutions', '\n'.join(map(repr, x_solutions)))
            print('y_solutions', '\n'.join(map(repr, y_solutions)))
        if self.verbose:
            if self.data_path().joinpath('solutions.txt').exists():
                self.data_path().joinpath('solutions.txt').remove()
        all_solutions = set()
        for x_first_0, x_steps, always_zero in x_solutions:
            for y_first_0, y_steps in y_solutions:
                if always_zero and y_steps >= x_steps:
                    if self.verbose: 
                        print(f'solution: ( {x_first_0}, {y_first_0})')
                        with open(self.data_path() / 'solutions.txt', 'a') as f:
                            f.write(f'solution: ( {x_first_0}, {y_first_0})\n')
                    all_solutions.add((x_first_0, y_first_0))
                else:
                    if x_steps == y_steps:
                        if self.verbose: 
                            print(f'solution: ( {x_first_0}, {y_first_0})')
                            with open(self.data_path() / 'solutions.txt', 'a') as f:
                                f.write(f'solution: ( {x_first_0}, {y_first_0})\n')
                        all_solutions.add((x_first_0, y_first_0))
        counter = len(all_solutions) + counter_obvious_solutions
        if not self.is_example:
            assert counter > 3744, f'counter {counter} is not greater than 3744 (Solution too low)'
            assert counter < 4037, f'counter {counter} is not less than 4037 (Solution too high)'
        return counter 

    def x_is_in_bound(self, x_first_0, x_a, x_b):
        t = 0
        x_t = 0
        x_t_solutions = []
        while x_t <= x_b:
            t += 1
            x_t = x_t + x_first_0
            if x_t >= x_a and x_t <= x_b:
                is_zero = x_first_0 == 0
                x_t_solutions.append((t, is_zero))
            if x_first_0 == 0:
                break
            x_first_0 = max(x_first_0 - 1, 0)
        is_in_bound = (x_t <= x_b)
        return x_t_solutions