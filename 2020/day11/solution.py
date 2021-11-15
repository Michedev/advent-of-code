import numpy as np

ch_map = {'.': 0, 'L': 1, '#': 2}

def parse_data(input_path: str):
    with open(input_path) as f:
        data_str = f.read().split('\n')
    w, h = len(data_str), len(data_str[0])
    data = np.zeros([w,h,3], dtype=bool)
    for i in range(len(data_str)):
        for j in range(len(data_str[0])):
            val_str = data_str[i][j]
            data[i, j, ch_map[val_str]] = True
    return data

DIRECTIONS = [(i, j) for i in range(-1, 2) for j in range(-1, 2) if not (i == j == 0)]

def count_around(s_t: np.ndarray, i: int, j: int, target: str, greater_than_0: bool = False):
    counter = 0
    for (d_i, d_j) in DIRECTIONS:
            i1, j1 = i + d_i, j + d_j
            if i1 >= 0 and j1 >= 0 and i1 < s_t.shape[0] and j1 < s_t.shape[1]:
                if s_t[i1, j1, ch_map[target]]:
                    counter += 1
                    if greater_than_0: return True
    return counter

def is_not_oob(i: int, j: int, m: np.ndarray):
    return i >= 0 and j >= 0 and i < m.shape[0] and j < m.shape[1]

def count_around_seats(s_t: np.ndarray, i: int, j: int, target: str, greater_than_0: bool = False):
    counter = 0
    for (d_i, d_j) in DIRECTIONS:
            i1, j1 = i + d_i, j + d_j
            while is_not_oob(i1, j1, s_t) and s_t[i1, j1, ch_map['.']]:
                i1 = i1 + d_i
                j1 = j1 + d_j
            if is_not_oob(i1, j1, s_t):
                if s_t[i1, j1, ch_map[target]]:
                    counter += 1
                    if greater_than_0: return True
    return counter


def step(s_t: np.ndarray, s_t1: np.ndarray, i: int, j: int):
    if s_t[i, j, ch_map['L']]:
        any_adj_occupied = count_around(s_t, i, j, '#', greater_than_0=True)
        if not any_adj_occupied:
            s_t1[i, j, ch_map['L']] = False
            s_t1[i, j, ch_map['#']] = True
            return True
    if s_t[i, j, ch_map['#']]:
        num_occupied = count_around(s_t, i, j, '#', greater_than_0=False)
        if num_occupied >= 4:
            s_t1[i, j, ch_map['L']] = True
            s_t1[i, j, ch_map['#']] = False
            return True
    return False


def step2(s_t: np.ndarray, s_t1: np.ndarray, i: int, j: int):
    if s_t[i, j, ch_map['L']]:
        any_adj_occupied = count_around_seats(s_t, i, j, '#', greater_than_0=True)
        if not any_adj_occupied:
            s_t1[i, j, ch_map['L']] = False
            s_t1[i, j, ch_map['#']] = True
            return True
    if s_t[i, j, ch_map['#']]:
        num_occupied = count_around_seats(s_t, i, j, '#', greater_than_0=False)
        if num_occupied >= 5:
            s_t1[i, j, ch_map['L']] = True
            s_t1[i, j, ch_map['#']] = False
            return True
    return False

def grid_step(s_t, s_t1, use_step2 = False):
    for i in range(s_t.shape[0]):
        for j in range(s_t.shape[1]):
            if use_step2: step2(s_t, s_t1, i, j)
            else: step(s_t, s_t1, i, j)


from pathlib import Path

def solution(input_path: str, solution2: bool = False):
    s_t = parse_data(input_path)
    s_t1 = np.zeros_like(s_t, dtype=bool)
    while not (s_t == s_t1).all():
        s_t1 = np.copy(s_t)
        grid_step(s_t, s_t1, use_step2=solution2)
        s_t, s_t1 = s_t1, s_t
    print(s_t[:, :, ch_map['#']].sum())

def test_grid_step():
    input_1 = parse_data(Path(__file__).parent / 'input_example.txt')
    exp_output = parse_data(Path(__file__).parent / 'input_example_1_step.txt')
    s_t1 = np.copy(input_1)
    grid_step(input_1, s_t1)
    for i in range(3):
        assert (s_t1[:, :, i] == exp_output[:, :, i]).all(), f'\n {s_t1[:, :, i]} \n ======= \n {exp_output[:, :, i]}'

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input', type=Path)
    parser.add_argument('-2', '--solution2', action='store_true', dest='solution2')
    args = parser.parse_args()
    solution(args.input, args.solution2)