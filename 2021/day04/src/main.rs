struct Table<T>{
    values: Vec<Vec<T>>,
}


struct Data{
    sequence_numbers: Vec<i32>,
    boards: Vec<Table<i32>>,
    catched: Vec<Table<bool>>,
}



fn solution1(data: &mut Data) -> i32 {
    let mut result  = 0;
    for number in data.sequence_numbers{
        let mut i_board = 0;
        let mut i = 0;
        let mut j = 0;
        for board in data.boards{
            for row in board.values{
                for value in row{
                    if value == number{
                        data.catched[i_board].values[i][j] = true;
                    }
                    j += 1;
                }
                i += 1;
            }
            i_board += 1;
        }
        for 
    }
    return result
}

fn main(){
    // read file input_example.txt
    let input = std::fs::read_to_string("../input_example.txt").unwrap();
    // for line in input
    let mut i = 0;
    let mut sequence_numbers: Vec<i32> = Vec::new();
    let mut board_rows: Vec<Vec<i32>> = Vec::new();
    let mut boards_vector: Vec<Table<i32>> = Vec::new();
    let mut catched_rows: Vec<Vec<bool>> = Vec::new();
    let mut catched_vector: Vec<Table<bool>> = Vec::new();
    for line in input.lines(){
        if i == 0{
            sequence_numbers = line.split(",").map(|s| s.parse().unwrap()).collect();
        }
        else{
            if i > 1 {
                if !line.is_empty(){
                    let mut board_row: Vec<i32> = Vec::new();
                    let mut catched_row: Vec<bool> = Vec::new();
                    let mut j = 0;
                    while j < line.len() {
                        let value: i32 = line[j..j+2].parse().unwrap();
                        board_row.push(value);
                        catched_row.push(false);
                        j += 3;
                    }
                    board_rows.push(board_row);
                    catched_rows.push(catched_row);
                } else {
                    boards_vector.push(Table{values: board_rows});
                    catched_vector.push(Table{values: catched_rows});
                    board_rows = Vec::new();
                    catched_rows = Vec::new();
                }
            }
        }
        i += 1;
    }
    let data = Data{sequence_numbers: sequence_numbers, boards: boards_vector, catched: catched_vector};
    let result = solution1(&data);
    println!("result: {}", result)
    

}