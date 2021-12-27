import argparse
from itertools import product

from path import Path
import numpy as np

day = Path(__file__).parent


def parse(input_file):
    """
    >>> data = parse('input_test.txt')
    >>> np.all(data == np.array([[1,2],[3,4]]))
    True

    :param input_file:
    :type input_file:
    :return:
    :rtype:
    """
    with open(input_file) as f:
        data = f.read().split('\n')
    data = [[int(x) for x in row] for row in data]
    return np.array(data)


def next_position(explored):
    for i in range(explored.shape[0]):
        for j in range(explored.shape[1]):
            if not explored[i, j]:
                return i, j


def find_min(data, i, j):
    directions = [(data[i + dx, j + dy], i + dx, j + dy) for dx, dy in product([-1, 0, 1], [-1, 0, 1]) if
                  not (dx == 0 and dy == 0) and ((abs(dx) + abs(dy)) < 2) and
                  (data.shape[0] > (i + dx) >= 0) and (data.shape[1] > (j + dy) >= 0)]
    best = min(directions, key=lambda p: p[0])
    if data[i, j] <= best[0]:
        return [(i, j)]
    else:
        return find_min(data, best[1], best[2]) + [(i, j)]


def solution1(data):
    explored = np.zeros_like(data, dtype=bool)
    mins = []
    while not np.all(explored):
        i, j = next_position(explored)
        pos_history = find_min(data, i, j)
        for pos in pos_history:
            explored[pos[0], pos[1]] = True
        min_pos = pos_history[0]
        mins.append(min_pos)
    print(mins)
    mins = list(set(mins))
    mins = [data[i, j] for i, j in mins]
    solution = sum(mins) + len(mins)
    assert solution < 1797, solution
    return solution

def solution2(data):
    raise NotImplementedError()


def setup_argparse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=Path)
    parser.add_argument('-2', '--solution2', action='store_true', dest='solution2')
    parser.add_argument('--custom', dest='custom', type=str, default=None)
    parser.add_argument('-e', '--example', action='store_true', dest='example')
    return parser


def main():
    parser = setup_argparse()
    args = parser.parse_args()
    if args.custom is not None:
        input_file = day / args.custom
    elif args.example:
        input_file = day / 'input_example.txt'
    else:
        input_file = day / 'input.txt'
    data = parse(input_file)
    if args.solution2:
        print(f'solution2(data) = {solution2(data)}')
    else:
        print(f'solution1(data) = {solution1(data)}')


if __name__ == '__main__':
    main()
