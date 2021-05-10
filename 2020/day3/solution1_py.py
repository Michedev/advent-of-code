import numpy as np

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

def run_1(grid):
    my_x = 0
    my_y = 0
    num_rows = grid.shape[0]
    num_cols = grid.shape[1]
    num_trees = 0
    while my_x < num_rows:
        if grid[my_x, my_y]:
            num_trees += 1
        # step
        my_x += 1
        my_y = (my_y + 3) % (num_cols - 1)
    return num_trees


def main(repeat=1):
    grid = parse_input(repeat)
    num_trees = run_1(grid)

    return num_trees


if __name__ == '__main__':
    main()
