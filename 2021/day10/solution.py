import argparse
from path import Path

day = Path(__file__).parent

opening_chars = '([{<'
closing_chars = ')]}>'


def parse(input_file):
    with open(input_file) as f:
        return f.read().split('\n')


def find_errors(line):
    stack = []
    penalty_wrong_closing = {')': 3, ']': 57, '}': 1197, '>': 25137}
    total = 0
    for c in line:
        if c in opening_chars:
            stack.append((c, opening_chars.index(c)))
        else:
            _, i_opening_c = stack.pop()
            exp_closing_c = closing_chars[i_opening_c]
            if not exp_closing_c == c:
                penalty = penalty_wrong_closing[c]
                print('penalty', penalty)
                return penalty
    return total


def is_incomplete(line):
    num_opening = 0
    num_closing = 0
    stack = []
    for c in line:
        if c in opening_chars: num_opening += 1
        if c in closing_chars: num_closing += 1
        if c in opening_chars:
            stack.append((c, opening_chars.index(c)))
        else:
            _, i_opening_c = stack.pop()
            exp_closing_c = closing_chars[i_opening_c]
            if not exp_closing_c == c:
                return False
    incomplete = num_opening != num_closing
    return incomplete


def get_score(incomplete_line: str) -> int:
    stack = []
    total = 0
    for c in incomplete_line:
        if c in opening_chars:
            stack.append((c, opening_chars.index(c)))
        else:
            _, i_opening_c = stack.pop()
            exp_closing_c = closing_chars[i_opening_c]
            if exp_closing_c != c:
                print(exp_closing_c, '!=', c)
    total = 0
    for _ in range(len(stack)):
        opening_c, i_opening_c = stack.pop()
        total = (total * 5) + (i_opening_c + 1)
    return total


def solution1(data):
    return sum(find_errors(line) for line in data)


def solution2(data):
    incomplete_lines = [line for line in data if is_incomplete(line)]
    scores = [get_score(line) for line in incomplete_lines]
    scores = sorted(scores)
    return scores[len(scores) // 2]


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
