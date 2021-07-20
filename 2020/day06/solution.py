from path import Path
from argparse import ArgumentParser

argparse = ArgumentParser()
argparse.add_argument('-e', '--use-example', action='store_true', dest='use_example')
args = argparse.parse_args()

input_path = Path(__file__).parent 
if args.use_example:
    input_path = input_path / 'input_example.txt'
else:
    input_path = input_path / 'input.txt'

def parse_input():
    with open(input_path) as f:
        lines = f.read().split('\n\n')
    lines = [l.split('\n') for l in lines]
    return lines


def solution1():
    data = parse_input()
    return sum(len(set(''.join(g))) for g in data)

def solution2():
    data = parse_input()
    result = 0
    for group in data:
        all_answers = set(group[0])
        for person in group:
            all_answers.intersection_update(person)
        result += len(all_answers)
    return result


print(solution2())