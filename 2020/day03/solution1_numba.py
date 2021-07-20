import numpy as np
from numba import jit, prange, njit


def parse_input(repeat: int):
    with open('input_example.txt', 'r') as f:
        txt = f.readlines()
    txt *= repeat
    line_length = len(txt[0])
    num_lines = len(txt)
    trees_grid = np.zeros((num_lines, line_length), dtype=np.bool)

    for i, row in enumerate(txt):
        for j, chr in enumerate(row):
            if chr == '#':
                trees_grid[i, j] = True
    return trees_grid


@njit('int64(b1[:,:])', parallel=True)
def run_1(grid: np.ndarray):
    num_rows = grid.shape[0]
    num_cols = grid.shape[1]
    num_trees = 0
    for i in prange(num_rows):
        my_x = (i * 3) % (num_cols - 1)
        my_y = i
        if grid[my_y, my_x]:
            num_trees += 1
    return num_trees


def main(repeat=1):
    grid = parse_input(repeat)
    num_trees = run_1(grid)

    return num_trees


if __name__ == '__main__':
    main()
