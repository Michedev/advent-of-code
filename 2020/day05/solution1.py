from math import ceil, floor
from typing import List

debug = False

def binary_search(code: str, upper_value: str) -> tuple :
    min_value = 0
    max_value = 2 ** len(code) - 1
    if debug: print(code)
    for c in code:
        middle_value = (min_value + max_value) / 2
        if c == upper_value:
            min_value = ceil(middle_value)
        else:
            max_value = floor(middle_value)
        if debug: print(min_value, max_value)
    assert min_value == max_value
    return min_value



def get_seat_id(code: str) -> int:
    """
    >>> get_seat_id("BFFFBBFRRR")
    567
    >>> get_seat_id("FFFBBBFRRR")
    119
    >>> get_seat_id("BBFFBBFRLL")
    820
    >>> get_seat_id("FBFBBFFRLR")
    357
    >>> get_seat_id("FBFBBBFRLR")
    373
    """
    code = code.upper()
    row = binary_search(code[:7], 'B')
    col = binary_search(code[7:10], 'R')
    if debug: print(row, col)
    seat_id = (row * 8) + col
    return seat_id

def solution1(codes: List[str]):
    max_seat_id = max(get_seat_id(code) for code in codes)
    return max_seat_id


from path import Path

input_path = Path(__file__).parent / 'input.txt'

def parse_data():
    with open(input_path) as f:
        return f.readlines()

from solution1_cython import solution1 as sol1_cython
from solution1_cython import solution2 as sol2_cython
import time

def main():
    data = parse_data()
    print('data parsed')
    s = time.perf_counter()
    solution = sol1_cython(data)
    sol2_cython(data, solution)

if __name__ == '__main__':
    main()