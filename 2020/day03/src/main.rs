use ndarray::Array2;
use std::fs;

fn parse_input(repeat: usize) -> Array2<u8> {
    let text: String = fs::read_to_string("input_example.txt").unwrap().repeat(repeat);
    let lines: Vec<&str> = text.lines().into_iter().collect();
    let num_lines = lines.len();
    let num_chars = lines[0].len();
    let mut data: Array2<u8> = Array2::zeros((num_lines, num_chars));
    for (i, line) in lines.into_iter().enumerate() {
        if line.is_empty() {
            continue;
        }
        for (j, value) in line.trim().chars().enumerate() {
            data[[i, j]] = (value == '#') as u8;
        }
    }
    data
}

fn run_1(grid: &Array2<u8>) -> usize {
    let mut x = 0;
    let mut y = 0;
    let mut trees = 0;
    let grid_shape = grid.shape();
    let num_rows = grid_shape[0];
    let num_cols = grid_shape[1];
    while x < num_rows {
        trees += grid[[x, y]] as usize;
        x += 1;
        y = (y + 3) % num_cols;
    }
    return trees;
}

fn main() {
    println!("Hello, world!");
    let data = parse_input(100);
    let result = run_1(&data);
    println!("Result: {}", result);
}
