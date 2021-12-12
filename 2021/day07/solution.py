import argparse
from path import Path
import numpy as np

day = Path(__file__).parent

def solution1(data: np.array):
    return np.abs(data - np.median(data)).sum()

def solution2(data: np.array):
    data_mean = data.mean()
    result = min(distance_solution2(data, np.floor(data_mean)),
                 distance_solution2(data, np.ceil(data_mean)))
    assert result < 98363819
    return result

def distance_solution2(data, mean_value):
    diffs = np.abs(data - mean_value)
    return (diffs * (diffs + 1) / 2).sum().astype('int')


def setup_argparse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=Path)
    parser.add_argument('-2', '--solution2', action='store_true', dest='solution2')
    parser.add_argument('--custom', dest='custom', type=str, default=None)
    parser.add_argument('-e', '--example', action='store_true', dest='example')
    return parser


def parse(input_file):
    with open(input_file) as f:
        data = f.read()
    return np.array([int(x) for x in data.split(',')])


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