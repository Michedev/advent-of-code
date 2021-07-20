from argparse import ArgumentParser

def read_file(input_example: bool):
    fname = 'input_example.txt' if input_example else 'input1.txt'
    with open(fname) as f:
        return [int(el) for el in f.read().split(",")]



class GameRunner:

    def __init__(self, data, turn_end=2020):
        self.turn_end = turn_end
        self.number_last_two_spoken = {}
        for (i, el) in enumerate(data):
            self.number_last_two_spoken[el] = [i+1, -1]
        self.last_number = data[-1]
        self.turn = len(data) + 1

    def has_been_spoken(self, number):
        return number in self.number_last_two_spoken and self.number_last_two_spoken[number][1] != -1

    def last_two_call_diff(self, number):
        t1, t2 = self.number_last_two_spoken[number]
        return t1 - t2

    def run(self):
        while self.turn <= self.turn_end:
            if not self.has_been_spoken(self.last_number):
                next_number = 0
            else:
                next_number = self.last_two_call_diff(self.last_number)
            if next_number not in self.number_last_two_spoken:
                self.number_last_two_spoken[next_number] = [self.turn, -1]
            else:
                last_turn_number = self.number_last_two_spoken[next_number][0]
                self.number_last_two_spoken[next_number] = [self.turn, last_turn_number]
            self.last_number = next_number
            self.turn += 1
        
        return self.last_number


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--input-example', '-i', type=eval, choices=[True, False], default=False, dest='input_example')
    input_example = parser.parse_args().input_example
    data = read_file(input_example)
    g = GameRunner(data)
    result = g.run()
    print(result)