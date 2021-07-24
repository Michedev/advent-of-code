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

def count_around(s_t: np.ndarray, i: int, j: int, target: str, greater_than_0: bool = False):
    counter = 0
    for (d_i, d_j) in [(-1, 0), (1, 0), (0,-1), (0,1)]:
            i1, j1 = i + d_i, j + d_j
            if i1 >= 0 and j1 >= 0 and i1 < s_t.shape[0] and j1 < s_t.shape[1]:
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

def grid_step(s_t, s_t1):
    for i in range(s_t.shape[0]):
        for j in range(s_t.shape[1]):
            step(s_t, s_t1, i, j)


from pathlib import Path

def main():
    s_t = parse_data(Path(__file__).parent / 'input_example.txt')
    s_t1 = np.zeros_like(s_t, dtype=bool)
    while not (s_t == s_t1).all():
        s_t1 = np.copy(s_t)
        grid_step(s_t, s_t1)
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
    main()