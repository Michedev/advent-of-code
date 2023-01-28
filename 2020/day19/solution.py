import re
import sys
from random import shuffle
from typing import List

from path import Path

rule_dict = dict()


class BaseRule:
    syntax_rule = re.compile('(?P<key>\d+):\s*"(?P<matchstr>.+)"')

    def __init__(self, rule):
        m = self.syntax_rule.match(rule)
        assert m is not None
        self.key = int(m.group('key'))
        self.matching_str = m.group('matchstr')

    def validate(self, s):
        return s.startswith(self.matching_str), len(self.matching_str)


class ProxyRule:
    syntax_rule = re.compile(r'(?P<key>\d+): ([\d\s]+)(\s*\|\s*([\d\s]+))*')
    num_regex = re.compile(r'([\d\s]+)(?!:)')

    def __init__(self, rule: str):
        m = self.syntax_rule.match(rule)
        assert m is not None
        self.key = int(m.group('key'))
        self.or_rules = self._get_rules(rule)

    
    def _get_rules(self, rule):
        """
        >>> ProxyRule._get_rules("43: 485 43 | 4 234 94 2939 23 | 49 4")
        [[485, 43], [4, 234, 94, 2939, 23], [49, 4]]
        >>> ProxyRule._get_rules("4: 24 56 53 90")
        [[24, 56, 53, 90]]
        """
        result = []
        i_start = rule.index(':')
        for m in self.num_regex.finditer(rule, i_start):
            and_rule = []
            for x in m.group(1).strip().split(' '):
                and_rule.append(int(x))
            result.append(and_rule)
        return result

    def validate(self, s):
        i = 0
        for or_rules in self.or_rules:
            all_true = True
            tmp_len = 0
            for i_and_rule in or_rules:
                is_valid, len_substr = rule_dict[i_and_rule].validate(s[i:])
                tmp_len += len_substr
                i += len_substr
                if not is_valid:
                    all_true = False
                    i -= tmp_len
                    break
            if all_true:
                return True, i
        return False, 0


class ProxyRuleRecursive(ProxyRule):

    def __init__(self, rule: str):
        super().__init__(rule)

    def validate(self, s, depth: int = 0):
        if depth > 10_000: return False, 0
        i = 0
        shuffle(self.or_rules)
        for and_rule in self.or_rules:
            all_true = True
            match_len = 0
            for i_rule in and_rule:
                r = rule_dict[i_rule]
                if isinstance(r, BaseRule):
                    is_valid, len_substr = r.validate(s[i:])
                else:
                    is_valid, len_substr = r.validate(s[i:], depth + 1)
                match_len += len_substr
                i += len_substr
                if not is_valid:
                    all_true = False
                    i -= match_len
                    break
            if all_true:
                if depth == 0:
                    if i >= len(s):
                        return True, i
                    else:
                        return False, 0
                else:
                    return True, i
        return False, 0


def parse_rules(rule_list: List[str], add_recursive=False):
    for rule in rule_list:
        if BaseRule.syntax_rule.match(rule):
            r = BaseRule(rule)
        elif ProxyRule.syntax_rule.match(rule):
            r = ProxyRuleRecursive(rule)
        else:
            raise ValueError(f'{rule = } not recognized')
        rule_dict[r.key] = r
    if add_recursive:
        rule_dict[8].or_rules.append([42, 8])
        rule_dict[11].or_rules.append([42, 11, 31])

def parse_input(input_file, add_recursive=False):
    with open(input_file) as f:
        lines = f.read().split('\n')
    rule_lines = []
    input_lines = []
    rule_zone = True
    for l in lines:
        if not l:
            rule_zone = False
        elif rule_zone:
            rule_lines.append(l)
        else:
            input_lines.append(l)
    parse_rules(rule_lines, add_recursive)
    return input_lines


def solution1(input_path: str):
    input_lines = parse_input(input_path)
    result = sum(rule_dict[0].validate(l)[0] for l in input_lines)
    assert result != 28, 'wrong result by website'
    return result


def test_simple_case():
    valid_seq = "abc"
    rules = '''0: 1 2
1: 3 | 3 4
2: "c"
3: "a"
4: "b"'''.split('\n')
    parse_rules(rules, add_recursive=False)
    assert any(rule_dict[0].validate(valid_seq)[0] for _ in range(1_000)), f'"{valid_seq}" is not valid'



def test_solution2():
    valid_sequences = """bbabbbbaabaabba
    babbbbaabbbbbabbbbbbaabaaabaaa
    aaabbbbbbaaaabaababaabababbabaaabbababababaaa
    bbbbbbbaaaabbbbaaabbabaaa
    bbbababbbbaaaaaaaabbababaaababaabab
    ababaaaaaabaaab
    ababaaaaabbbaba
    baabbaaaabbaaaababbaababb
    abbbbabbbbaaaababbbbbbaaaababb
    aaaaabbaabaaaaababaa
    aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
    aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""".replace(' ' * 4, '').split('\n')
    rules = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1""".split('\n')
    parse_rules(rules, add_recursive=True)
    for seq in valid_sequences:
        assert any(rule_dict[0].validate(seq)[0] for _ in range(1_000)), f'"{seq}" is not valid'


def solution2(input_path: str):
    input_lines = parse_input(input_path, add_recursive=True)
    result = sum(any(rule_dict[0].validate(l)[0] for _ in range(1_000)) for l in input_lines)
    # assert result <= 564, 'wrong result by website'
    # assert result > 282, 'wrong result by website'
    return result


if __name__ == '__main__':
    p = Path(__file__).parent / 'input.txt'
    solution1(p)
