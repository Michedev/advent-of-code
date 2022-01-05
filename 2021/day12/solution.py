from collections import defaultdict

from path import Path

from template import TemplateSolution


class Day12Solution(TemplateSolution):
    @classmethod
    def data_path(cls):
        return Path(__file__).parent

    @classmethod
    def parse(cls, input_file):
        with open(input_file) as f:
            data = f.read()
        data = [line.split('-') for line in data.split('\n')]
        data_reversed = [(b, a) for a, b in data]
        return data + data_reversed

    @classmethod
    def single_step(cls, data, counter, start: str):
        result = 0
        counter[start] += 1
        paths = [b for a, b in data if a == start and (b.isupper() or counter[b] < 1) and b != 'start']
        for dest in paths:
            if dest == 'end':
                result += 1
            else:
                result += cls.single_step(data, counter, dest)
        counter[start] -= 1
        return result

    @classmethod
    def single_step2(cls, data, counter, start: str, small_twice=False):
        result = 0
        counter[start] += 1
        if start.islower() and counter[start] == 2:
            small_twice = True
        paths = [b for a, b in data if a == start and (b.isupper() or (counter[b] < 2 and not small_twice) or (
                    counter[b] < 1 and small_twice)) and b != 'start']
        for dest in paths:
            if dest == 'end':
                result += 1
            else:
                result += cls.single_step2(data, counter, dest, small_twice)
        counter[start] -= 1
        return result

    @classmethod
    def solution1(cls, data):
        counter = defaultdict(lambda: 0)
        return cls.single_step(data, counter, 'start')

    @classmethod
    def solution2(cls, data):
        counter = defaultdict(lambda: 0)
        return cls.single_step2(data, counter, 'start')


def test_input_example_solution1():
    assert Day12Solution.parse_solution1('input_example.txt') == 10


def test_input_example2_solution1():
    assert Day12Solution.parse_solution1('input_example2.txt') == 19


def test_input_example3_solution1():
    assert Day12Solution.parse_solution1('input_example3.txt') == 226

def test_input_example_solution2():
    assert Day12Solution.parse_solution2('input_example.txt') == 36


def test_input_example2_solution2():
    assert Day12Solution.parse_solution2('input_example2.txt') == 103


def test_input_example3_solution2():
    assert Day12Solution.parse_solution2('input_example3.txt') == 3509



if __name__ == '__main__':
    Day12Solution.main()
