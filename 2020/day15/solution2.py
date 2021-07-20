from solution1 import *

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input-example', '-i', type=eval, choices=[True, False], default=False, dest='input_example')
    input_example = parser.parse_args().input_example
    data = read_file(input_example)
    g = GameRunner(data, 30_000_000)
    result = g.run()
    print(result)