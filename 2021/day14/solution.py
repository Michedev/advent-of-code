import re
from collections import namedtuple, Counter
from typing import List

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
        sequence = data.sequence[:]
        for _ in range(10):
            sequence = cls.apply_pattern(sequence, data.rules)
        counter_chars = Counter(sequence)
        result = max(counter_chars.values()) - min(counter_chars.values())
        return result

    @classmethod
    def solution2(cls, data):
        sequence = data.sequence[:]
        for i in range(40):
            print('step', i+1)
            sequence = cls.apply_pattern(sequence, data.rules)
        counter_chars = Counter(sequence)
        result = max(counter_chars.values()) - min(counter_chars.values())
        return result

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
