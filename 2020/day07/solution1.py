import re
from collections import namedtuple

def parse_data():
    with open('input.txt') as f:
        data = f.read()
    return [d[:-1] for d in data.split('\n')]

rule_parser = re.compile(r'(?P<rule_producer>[a-z]+ [a-z]+) bags contain (((?P<size_output1>[1-9]+) (?P<type_output1>[a-z]+ [a-z]+) bag[s]{0,1})|(?P<is_empty>no other bags))' + ''.join(['(, (?P<size_output' + f'{i+2}' + '>[1-9]+) (?P<type_output' + f'{i+2}' + '>[a-z]+ [a-z]+) bag[s]{0,1}){0,1}' for i in range(10)]))
RuleOutput = namedtuple('RuleOutput', ['size_output', 'type_output'])

def make_rules(raw_rules: list) -> dict:
    rules = {}
    for rule in raw_rules:
        parsed_rule: re.Pattern = rule_parser.match(rule)
        groups = parsed_rule.groupdict()
        key = groups['rule_producer']
        type_output1 = groups['type_output1']
        size_output1 = groups['size_output1']
        if groups['is_empty']:
            value = None
        else:
            size_output1 = int(size_output1)
            value = [RuleOutput(size_output1, type_output1)]
        for i in range(10):
            if size_output_i := groups[f'size_output{i+2}']:
                size_output_i = int(size_output_i)
                type_output_i = groups[f'type_output{i+2}']
                value.append(RuleOutput(size_output_i, type_output_i))
        rules[key] = value
    return rules

def parse_data_and_make_rules():
    return make_rules(parse_data())

def recursive_exploration(rules: dict, key: str):
    value = rules[key]
    if not value:
        return 1
    result = 0
    for (size_o, type_output) in value:
        rec_result = recursive_exploration(rules, type_output)
        result += size_o * rec_result
        if rec_result > 1:
            result += size_o
    return result

def find_target_rule(rules: dict, key: str, target: str):
    """[summary]

    Returns:
        bool: True if key can reach target through the rules
    """
    value = rules[key]
    if not value or (max_level is not None and level >= max_level):
        return False
    result = False
    for (size_o, type_output) in value:
        if type_output == target:
            return True
        result = result or find_target_rule(rules, type_output, target)
    return result


def solution1():
    start_key = 'shiny gold'
    rules = parse_data_and_make_rules()
    print(rules)
    return sum(find_target_rule(rules, r, start_key) for r in rules.keys() if r != start_key)

def solution2():
    start_key = 'shiny gold'
    rules = parse_data_and_make_rules()
    print(rules)
    return recursive_exploration(rules, start_key)

print(solution2())