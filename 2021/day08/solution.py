import argparse
from collections import namedtuple
from typing import List

from path import Path

day = Path(__file__).parent


Signal = namedtuple('Signal', ['examples', 'code'])

def parse(input_file):
    result = []
    with open(input_file) as f:
        data = f.read()
    for line in data.split('\n'):
        examples, code = line.split('|')
        examples = examples.strip().split(' ')
        code = code.strip().split(' ')
        result.append(Signal(examples, code))
    return result

number_true_signals = {0: 'abcefg', 1: 'cf', 2: 'acdeg', 3: 'acdfg', 4: 'bcdf', 5: 'abdfg', 6: 'abdefg', 7: 'acf', 8: 'abcdefg', 9: 'abcdfg'}
signals_numbers = {v: k for k,v in number_true_signals.items()}

def decode(codes: List[str], true_patterns: dict):
    result = []
    for digit_code in codes:
        digit_code = sorted(digit_code)
        print(digit_code)
        fixed_code = ''.join(sorted([true_patterns[el] for el in digit_code]))
        digit = signals_numbers[fixed_code]
        result.append(digit)
    return result



def solution1(data: List[Signal]):
    counter = 0
    for signal in data:
        for digit_code in signal.code:
            code_len = len(digit_code)
            if code_len in [len(number_true_signals[d]) for d in [1, 4, 7, 8]]:
                counter += 1
    return counter

def find_matches(signal):
    """
    >>> data = Signal(['acedgfb', 'cdfbe', 'gcdfa', 'fbcad', 'dab', 'cefabd', 'cdfgeb', 'eafb', 'cagedb', 'ab'], None)
    >>> result = find_matches(data)
    >>> result[8]
    'acedgfb'
    >>> result[9]
    'cefabd'
    >>> result[0]
    'cagedb'

    :param signal:
    :type signal:
    :return:
    :rtype:
    """
    result = dict()
    unique_len_dict = {2: 1, 3: 7, 4: 4, 7: 8}
    for example in signal.examples:  # fill with 1, 4, 7, 8
        if len(example) in unique_len_dict:
            result[unique_len_dict[len(example)]] = example
    result[3] = find_match_length_subpattern(signal, 5, result[1])
    result[5] = find_match_length_subpattern(signal, 5, set(result[4]) - set(result[1]))
    for v in result.values():
        signal.examples.remove(v)
    result[2] = find_match_length_subpattern(signal, 5, [])
    signal.examples.remove(result[2])
    result[9] = find_match_length_subpattern(signal, 6, result[3])
    signal.examples.remove(result[9])
    result[6] = find_match_length_subpattern(signal, 6, result[5])
    signal.examples.remove(result[6])

    assert len(signal.examples) == 1, f'examples={signal.examples}, result={result}'
    result[0] = signal.examples[0]
    return result



def find_match_length_subpattern(signal, length, pattern):
    for example in signal.examples:
        if len(example) == length:
            if all(el in example for el in pattern):
                return example


def solution2(data):
    counter = 0
    for signal in data:
        digit_to_leds = find_matches(signal)
        leds_to_digit = {''.join(sorted(v)): k for k, v in digit_to_leds.items()}
        for i, digit_leds in enumerate(signal.code):
            counter += leds_to_digit[''.join(sorted(digit_leds))] * 10 ** (len(signal.code) - i - 1)
    return counter


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
