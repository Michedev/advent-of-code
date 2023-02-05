from typing import Tuple
from template import TemplateSolution
from path import Path
import re

class Solution(TemplateSolution, day=17, year=2021):

    regex_data = re.compile(r"target area: x=([-]{0,1}\d+)\.\.([-]{0,1}\d+), y=([-]{0,1}\d+)\.\.([-]{0,1}\d+)")

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
        counter = 0
        for y_first_0 in range(1, max(abs(y_a), abs(y_b))):
            if self.is_in_bound(y_first_0, y_a, y_b):
                counter += 1
        return counter