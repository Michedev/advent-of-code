from itertools import combinations

def parse_data(data_path: str):
    with open(data_path) as f:
        return [int(x) for x in f.read().split('\n')]

def bad_number(data: list, i: int, preamble_size: int):
    assert i >= preamble_size
    preamble = data[i-preamble_size:i]
    target = data[i]
    for p in combinations(preamble, 2):
        if sum(p) == target:
            return False
    return True

def solution1(data_path: str, preamble_size: int = 25):
    """[summary]

    >>> solution1('input_example.txt', 5)
    127

    """
    data = parse_data(data_path)
    for i in range(preamble_size, len(data)):
        if bad_number(data, i, preamble_size):
            return data[i]
    return None

def find_sum_slice(data: list, n: int):
    for i in range(len(data)):
        acc = data[i]
        for j in range(i+1, len(data)):
            acc += data[j]
            if acc == n:
                return data[i:j]
            elif acc > n:
                break
    return None

def solution2(data_path: str, preamble_size: int = 25):
    """
    >>> solution2('input_example.txt', 5)
    62    
    """
    bad_number = solution1(data_path, preamble_size)
    data = parse_data(data_path)
    subseq = find_sum_slice(data, bad_number)
    if subseq: return min(subseq) + max(subseq)


print(solution2('input.txt'))

