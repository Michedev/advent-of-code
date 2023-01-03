import argparse
from path import Path
import re
import numpy as np
from collections import namedtuple, Counter

Point = namedtuple('Point', ['x', 'y'])
day5 = Path(__file__).parent
line_re = re.compile(r'(?P<x1>\d+),\s*(?P<y1>\d+)\s*->\s*(?P<x2>\d+),\s*(?P<y2>\d+)')

def setup_argparse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=Path)
    parser.add_argument('-2', '--solution2', action='store_true', dest='solution2')
    parser.add_argument('-e', '--example', action='store_true', dest='example')
    return parser

def parse(input_path):
    with open(input_path) as f:
        text = f.read().split('\n')
    result = []
    for line in text:
        matched_line = line_re.match(line)
        x1 = int(matched_line.group('x1'))
        y1 = int(matched_line.group('y1'))
        x2 = int(matched_line.group('x2'))
        y2 = int(matched_line.group('y2'))
        if (abs(x1) + abs(y1)) > (abs(x2) + abs(y2)):
            x1, y1, x2, y2 = x2, y2, x1, y1
        result.append((Point(x1,y1), Point(x2,y2)))
    return result

def solution1(data):
    data = [(p1, p2, p1.x == p2.x, p1.y == p2.y) for (p1, p2) in data if p1.x == p2.x or p1.y == p2.y]
    c = dict()
    for p1, p2, same_x, same_y in data:
        if same_x:
            data_range = p2.y - p1.y
        else:
            data_range = p2.x - p1.x
        for i in range(data_range+1):
            if same_x:
                k = Point(p1.x, p1.y + i)
                old_value = c.get(k, 0)
                c[k] = old_value + 1
            else:
                k = Point(p1.x + i, p1.y)
                old_value = c.get(k, 0)
                c[k] = old_value + 1
    print(c)
    result = sum(freq >= 2 for freq in c.values())
    return result

def is_diagonal(p1, p2):
    return abs(p1.x - p2.x) == abs(p2.y - p1.y)

import numpy as np


def solution2(data):
    data = [(p1, p2, p1.x == p2.x, p1.y == p2.y, is_diagonal(p1, p2)) for (p1, p2) in data if p1.x == p2.x or p1.y == p2.y or is_diagonal(p1, p2)]
    c = dict()
    for p1, p2, same_x, same_y, diagonal in data:
        if same_x:
            data_range = p2.y - p1.y
        elif same_y:
            data_range = p2.x - p1.x
        else:
            data_range = abs(p2.x - p1.x)
            dx, dy = np.sign(p2.x - p1.x), np.sign(p2.y - p1.y)
        for i in range(data_range+1):
            if same_x:
                k = Point(p1.x, p1.y + i)
                old_value = c.get(k, 0)
                c[k] = old_value + 1
            elif same_y:
                k = Point(p1.x + i, p1.y)
                old_value = c.get(k, 0)
                c[k] = old_value + 1
            else:
                k = Point(p1.x + i * dx, p1.y + i * dy)
                old_value = c.get(k, 0)
                c[k] = old_value + 1
    result = sum(freq >= 2 for freq in c.values())
    return result

def main():
    parser = setup_argparse()
    args = parser.parse_args()
    if args.example:
        input_file = day5 / 'input_example.txt'
    else:
        input_file = day5 / 'input.txt'
    data = parse(input_file)
    if args.solution2:
        print(f'solution1(data) = {solution2(data)}')
    else:
        print(f'solution1(data) = {solution1(data)}')


if __name__ == '__main__':
    main()