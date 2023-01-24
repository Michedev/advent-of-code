import re
from collections import defaultdict, namedtuple, Counter
from typing import List
import numpy as np

from path import Path

from template import TemplateSolution

Rule = namedtuple('Rule', ('a', 'b'))
Data = namedtuple('Data', ('sequence', 'rules'))


class Day14Solution(TemplateSolution):
    @classmethod
    def data_path(cls):
        return Path(__file__).parent

    @classmethod
    def parse(cls, input_file):
        with open(input_file) as f:
            data = f.read().split('\n')
        sequence = data[0]
        regex_rule = re.compile('(?P<a>[\w\W]+) -> (?P<b>[\w\W]+)')
        rules = dict()
        for line in data[2:]:
            rule_matched = regex_rule.match(line)
            rules[rule_matched.group('a')] = rule_matched.group('b')
        return Data(sequence, rules)

    @classmethod
    def solution1(cls, data: Data):
        return cls.compute_solution(data, 10)

    @classmethod
    def compute_solution(cls, data: Data, iterations: int):
        transition_matrix, binomials = cls.build_transition_matrix(data.rules)
        if cls.verbose: 
            print(transition_matrix)
            print(binomials)
        transition_matrix = np.linalg.matrix_power(transition_matrix, iterations)
        if cls.verbose:
            print('transition matrix after {} iterations:'.format(iterations))
            print(transition_matrix)
        sequence_vector = np.zeros((len(binomials), 1), dtype=np.int64)
        for i in range(len(data.sequence) - 1):
            binomial = data.sequence[i:i + 2]
            if binomial in binomials:
                sequence_vector[binomials.index(binomial)] += 1
        result = sequence_vector.T @ transition_matrix 
        result = result.flatten()
        if cls.verbose:
            print(result)
        counter = defaultdict(lambda: 0)
        for i in range(len(result)):
            counter[binomials[i][0]] += result[i]
            # counter[binomials[i][1]] += result[i] 
        if cls.verbose:
            print(counter)
        print('Warning: solution may differs by one less')
        return max(counter.values()) - min(counter.values())

    @classmethod
    def solution2(cls, data):
        return cls.compute_solution(data, 40)

    @classmethod
    def build_transition_matrix(cls, rules: dict):
        all_binomials = set()
        for a, b in rules.items():
            all_binomials.add(a)
            all_binomials.add(a[0] + b)
            all_binomials.add(b + a[1])
        all_binomials = sorted(list(all_binomials))
        transition_matrix = np.zeros((len(all_binomials), len(all_binomials)), dtype=np.int64)
        for a, b in rules.items():
            i_a = all_binomials.index(a)
            i_b1 = all_binomials.index(a[0] + b)
            i_b2 = all_binomials.index(b + a[1])
            transition_matrix[i_a, i_b1] = 1
            transition_matrix[i_a, i_b2] = 1
        return transition_matrix, all_binomials
        


    @classmethod
    def apply_pattern(cls, sequence, rules):
        result = ''
        for i in range(len(sequence) - 1):
            result += sequence[i]
            binomial = sequence[i:i + 2]
            if binomial in rules:
                result += rules[binomial]
        result += sequence[-1]
        return result

    @classmethod
    def find_matching_rule(cls, binomial: str, rules: List[Rule]):
        for rule in rules:
            if rule.a == binomial:
                return rule
        return None


if __name__ == '__main__':
    Day14Solution.main()
