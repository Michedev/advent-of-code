import argparse
import importlib
import sys

from path import Path


def setup_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', type=int, required=True, dest='day')
    parser.add_argument('-f', type=str, dest='filename', default='input.txt')
    parser.add_argument('-2', action='store_true', dest='solution2')

    return parser


def main_argparse():
    parser = setup_argparse()
    args = parser.parse_args()
    run_path = Path(__file__).parent / ('day' + ("%02d" % (args.day,)))
    sys.path.insert(0, run_path)
    solution_module = importlib.import_module('solution')
    if args.solution2:
        result = solution_module.solution2(run_path / args.filename)
    else:
        result = solution_module.solution1(run_path / args.filename)
    print('solution', ('2' if args.solution2 else '1'), 'result is', result)

if __name__ == '__main__':
    main_argparse()