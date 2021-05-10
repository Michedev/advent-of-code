import sequtils
import strutils
import nimpy

proc read_input(t: int): seq[seq[bool]] =
    var lines = readFile("input_example.txt").string.split("\n")
    lines = lines.cycle(t)
    result = newSeq[seq[bool]](lines.len)
    for i, row in lines:
        var last: seq[bool] = new_seq[bool](row.len)
        for j, cell in row:
            last[j] = (cell == '#')
        result[i] = last

proc solution1(grid: seq[seq[bool]]): int =
    var
        my_x = 0
        my_y = 0
        num_trees = 0
    let
        num_rows = grid.len
        num_cols = grid[0].len
    while my_x < num_rows:
        if grid[my_x][my_y]:
            inc num_trees
        # step
        inc my_x
        my_y = (my_y + 3) mod num_cols
    return num_trees

proc main*(t: int): int {.exportpy.} =
    let grid = read_input(t)
    let num_trees = solution1(grid)
    return num_trees