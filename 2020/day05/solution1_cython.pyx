from cython.cimports.libc.math cimport floor, ceil
from libc.stdlib cimport malloc, free
from typing import List

debug = False

cdef binary_search(code: str, upper_value: str):
    cdef int min_value = 1
    cdef int max_value = 2 ** len(code)
    cdef float middle_value = 0.0
    if debug: print(code)
    for c in code:
        middle_value = (min_value + max_value) / 2
        if c == upper_value:
            min_value = int(ceil(middle_value))
        else:
            max_value = int(floor(middle_value))
        if debug: print(min_value, max_value)
    return min_value, max_value



cdef int get_seat_id(code: str):
    """
    >>> get_seat_id("BFFFBBFRRR")
    567
    >>> get_seat_id("FFFBBBFRRR")
    119
    >>> get_seat_id("BBFFBBFRLL")
    820
    >>> get_seat_id("FBFBBFFRLR")
    357
    """
    code = code.upper()
    row = min(binary_search(code[:7], 'B')) - 1
    col = max(binary_search(code[7:10], 'R')) - 1
    seat_id = row * 8 + col
    return seat_id

cpdef solution1(codes: List[str]):
    max_seat_id = 0
    for code in codes:
        seat_id = get_seat_id(code)
        if seat_id > max_seat_id:
            max_seat_id = seat_id
    return max_seat_id

cpdef solution2(codes: List[str], max_seat_id: int):
    cdef int* seats = <int *> malloc(len(codes) * sizeof(int))
    cdef bint* has_seat = <bint *> malloc(max_seat_id * sizeof(bint))
    cdef int i
    for i in range(max_seat_id):
        has_seat[i] = 0
    for i in range(len(codes)):
        seats[i] = get_seat_id(codes[i])
        has_seat[seats[i]] = 1
    for i in range(max_seat_id - 1):
        if has_seat[i] and not has_seat[i+1] and has_seat[i+2]:
            print(i+1, 'is a candidate')
    free(has_seat)
    free(seats)