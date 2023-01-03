import argparse
from path import Path
from collections import Counter

day = Path(__file__).parent

def parse(input_path):
    with open(input_path) as f:
        data = f.read()
    return [int(x) for x in data.split(',')]

num_days=80

def solution1(data):
    c = Counter(data)
    for _ in range(num_days):
        len_data = len(data)
        c = {k-1: v for k, v in c.items()}
        if -1 in c:
            c[8]= c[-1]
            if 6 in c:
                c[6] += c[-1]
            else:
                c[6] = c[-1]
            del c[-1]

    return sum(c.values())

def solution2(data):
    global num_days
    num_days = 256
    return solution1(data)

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