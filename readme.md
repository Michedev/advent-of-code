# How to run

Use the run command in the following way:

    ./run -y 2021 -d 15  # run solution 1 of 2021/day15

    ./run -y 2021 -d 15 --example  # run solution 1 of 2021/day15 with input example

    ./run -y 2021 -d 15 -2 # run solution 2 of 2021/day15

    ./run -y 2021 -d 15 -2 --example # run solution 2 of 2021/day15 with input example

## Usage

    usage: run [-h] [-i INPUT] [-2] [--custom CUSTOM] [-e] [-v] -y YEAR -d DAY

    options:
    -h, --help            show this help message and exit
    -i INPUT, --input INPUT
    -2, --solution2
    --custom CUSTOM
    -e, --example
    -v, --verbose
    -y YEAR, --year YEAR
    -d DAY, --day DAY

## Define a new solution

1. Create a new python file under `20XX/dayYY` (e.g. 2022/day23) folder
2. Create text files called `input.txt` and `input_example.txt` under `20XX/dayYY` folder. The first one will be used as input for the solution and the second one will be used as input for the example defined in the problem statement.
3. import _TemplateSolution_ from `template.py` and create a new class that inherits from it

TODO:

- [x] Describe project architecture
- [x] Describe how to run tests
