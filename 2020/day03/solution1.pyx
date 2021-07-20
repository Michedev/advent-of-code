import Cython
import numpy as np
cimport numpy as np

@Cython.boundscheck(False) # compiler directive
@Cython.wraparound(False) # compiler directive
cdef np.ndarray[np.uint8_t, ndim=2] parse_input(int repeat):
    with open('input_example.txt', 'r') as f:
        txt: list = f.readlines()
    txt *= repeat
    cdef:
        int line_length = len(txt[0])
        int num_lines = len(txt)
        np.ndarray[np.uint8_t, ndim=2] trees_grid = np.zeros((num_lines, line_length), dtype=np.uint8)

    for i, row in enumerate(txt):
        for j, chr in enumerate(row):
            if chr == '#':
                trees_grid[i, j] = True
    return trees_grid

@Cython.boundscheck(False) # compiler directive
@Cython.wraparound(False) # compiler directive
cdef int run_1(np.ndarray[np.uint8_t, ndim=2] grid):
    cdef:
        int my_x = 0
        int my_y = 0
        int num_rows = grid.shape[0]
        int num_cols = grid.shape[1]
        int num_trees = 0
    for i in range(num_rows):
        my_x = (i * 3) % (num_cols - 1)
        my_y = i
        if grid[my_y, my_x]:
            num_trees += 1
        #step
    return num_trees

cpdef int main(int repeat=1):
    cdef:
        np.ndarray grid = parse_input(repeat)
        int num_trees = run_1(grid)

    return num_trees

if __name__ == '__main__':
    main()



