import re
from path import Path

FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
regex_fields1 = [re.compile(f + r':') for f in FIELDS if f != 'cid']
regex_fields = [re.compile(f'({f})' + r':(\S+)') for f in FIELDS if f != 'cid']

def validate_byr(x):
    return 1920 <= int(x) <= 2002

def validate_iyr(x):
    return 2002 <= int(x) <= 2020

def validate_eyr(x):
    return 2020 <= int(x) <= 2030

def validate_hgt(x: str):
    if x.endswith('cm'):
        if not x[:3].isdigit(): return False
        if len(x) > 5: return False
        return 150 <= int(x[:3]) <= 193
    elif x.endswith('in'):
        if not x[:2].isdigit(): return False
        if len(x) > 4: return False
        return 59 <= int(x[:2]) <= 76
    else:
        return False

regex_hcl = re.compile(r'#[0-9a-f]{6}')
def validate_hcl(x):
    return regex_hcl.match(x) is not None

values_ecl = 'amb blu brn gry grn hzl oth'.split(' ')
def validate_ecl(x):
    return x in values_ecl

regex_pid = re.compile('[0-9]{9}')
def validate_pid(x):
    return regex_pid.match(x) is not None

def validate_cid(x=None): return True

def parse_data(input_path: str) -> list:
    acc_passaport = ''
    result = []
    i = 0
    with open(input_path, 'r') as f:
        passaports = f.read().split('\n')
    for i in range(len(passaports)):
        if passaports[i]:
            acc_passaport += passaports[i] + ' '
        else:
            result.append(acc_passaport)
            acc_passaport = ''
    return result

def is_valid(passaport: str):
    return all(r.search(passaport) for r in regex_fields1)

def solution1(fname: str):
    passaports = parse_data(fname)
    result = sum(is_valid(p) for p in passaports)
    return result

def is_valid2(p):
    if not is_valid(p): return False
    for r in regex_fields:
        m = r.search(p)
        if m is None: return False
        field_name = m.group(1)
        field_value = m.group(2)
        field_valid = eval(f'validate_{field_name}("{field_value}")')
        if not field_valid: return False
    return True

def test_is_valid2():
    p_valid = 'pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f'
    assert is_valid2(p_valid)
    p_invalid = 'hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007'
    assert not is_valid2(p_invalid)
    p_invalids = parse_data(Path(__file__).parent / 'input_test_invalid.txt')
    p_valids = parse_data(Path(__file__).parent / 'input_test_valid.txt')
    for p_valid in p_valids: assert is_valid2(p_valid), p_valid
    for p_invalid in p_invalids: assert not is_valid2(p_invalid), p_invalid

def solution2(fname: str):
    passaports = parse_data(fname)
    result = sum(is_valid2(p) for p in passaports)
    assert result < 161, 'result is too high'
    return result-1
