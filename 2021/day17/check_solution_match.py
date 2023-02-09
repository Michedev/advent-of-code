"""
Script to check if my solution matches the example solution.
"""


example_solution = """
23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7"""



def parse_pair(pair):
    x, y = pair.strip().split(',')
    return int(x), int(y)

example_solution = [parse_pair(p) for p in example_solution.replace('  ', ' ').replace('  ', ' ').split() if p]

import re

from path import Path

my_sol_tuple_re = re.compile(r'solution: \( ([-]{0,1}\d+), ([-]{0,1}\d+)\)')

my_code_non_obv_solutions = ""
with open(Path(__file__).parent / 'solutions.txt') as f:
    my_code_non_obv_solutions = f.read()
non_obv_solutions = []
for line in my_code_non_obv_solutions.split('\n'):
    if line:
        print(line)
        if m := my_sol_tuple_re.match(line):
            x, y = m.group(1), m.group(2)
            x, y = int(x), int(y)
            non_obv_solutions.append((x, y))
obv_solutions = [(x, y) for x in range(20, 31) for y in range(-10, -4)]
my_code_all_solutions = non_obv_solutions + obv_solutions


my_code_all_solutions = set(my_code_all_solutions)
example_solution = set(example_solution)
print('num of example solutions:', len(example_solution))
print('=' * 80)
for sol in my_code_all_solutions:
    if sol not in example_solution:
        print(f'Not in example: {sol}')
print('-' * 20)
for sol in example_solution:
    if sol not in my_code_all_solutions:
        print(f'Not in my code: {sol}')