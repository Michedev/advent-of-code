import argparse
from itertools import product
import matplotlib.pyplot as plt
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
    directions = get_neightbors(data, i, j)
    best = min(directions, key=lambda p: p[0])
    if data[i, j] <= best[0]:
        return [(i, j)]
    else:
        return find_min(data, best[1], best[2]) + [(i, j)]


def get_neightbors(data, i, j):
    directions = [(data[i + dx, j + dy], i + dx, j + dy) for dx, dy in product([-1, 0, 1], [-1, 0, 1]) if
                  not (dx == 0 and dy == 0) and ((abs(dx) + abs(dy)) < 2) and
                  (data.shape[0] > (i + dx) >= 0) and (data.shape[1] > (j + dy) >= 0)]
    return directions


def solution1(data):
    min_points = np.zeros_like(data, dtype=bool)
    for i in range(min_points.shape[0]):
        for j in range(min_points.shape[1]):
            neightbors = get_neightbors(data, i, j)
            best = min(neightbors, key=lambda p: p[0])
            if data[i, j] < best[0]:
                min_points[i, j] = True
    print(data * min_points.astype('int'))
    solution = ((data + 1) * min_points.astype('int')).sum()
    assert solution < 1797, solution
    return solution


def next_basin(data, i, j, seq=None):
    result = []
    if seq is None:
        seq = set()
    seq.add((i,j))
    neightbors = get_neightbors(data, i, j)
    for v, i_n, j_n in neightbors:
        if v != 9 and (i_n, j_n) not in seq:
            result += next_basin(data, i_n, j_n, seq)
    result.append((i,j))
    return result

def solution2(data):
    explored = data == 9
    plt.imshow(explored)
    plt.savefig(Path(__file__).parent / 'map.png')
    plt.close()
    basins = []
    while not np.all(explored):
        i, j = next_position(explored)
        basin_map = np.zeros_like(data, dtype=bool)
        basin = next_basin(data, i, j)
        for (i1, j1) in basin:
            explored[i1, j1] = True
            basin_map[i1, j1] = True
        basins.append(basin_map)
    basins = np.stack(basins, axis=0).astype('int').sum(axis=1).sum(axis=1)
    top_basins = np.sort(basins)[-3:]
    print(top_basins)
    solution = np.product(top_basins)
    return solution


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
        solution = solution2(data)
        if not args.example and args.custom is None:
            assert solution > 539448, solution
        print(f'solution2(data) = {solution}')
    else:
        print(f'solution1(data) = {solution1(data)}')


if __name__ == '__main__':
    main()
