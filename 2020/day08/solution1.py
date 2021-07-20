from solution2 import CodeRunner as CodeRunnerCython

class CodeRunner:

    def __init__(self, input_path: str = 'input.txt'):
        self.lines = self.parse_input(input_path)
        self.init_context_vars()

    def init_context_vars(self):
        self.num_exec_lines = [0] * len(self.lines)
        self.acc = 0
        self.curr_line = 0

    def parse_input(self, input_path):
        with open(input_path, 'r') as f:
            data = [x.split(' ') for x in f.read().split('\n')]
        data = [(l[0], int(l[1])) for l in data]
        return data

    def step_code(self):
        op_name, op_value = self.lines[self.curr_line]
        self.num_exec_lines[self.curr_line] += 1
        go_next_line = True
        if op_name == 'acc':
            self.acc += op_value
        elif op_name == 'jmp':
            go_next_line = False
            self.curr_line += op_value
        elif op_name == 'nop':
            pass
        else:
            raise ValueError(f'{op_name = } not recognized')
        if go_next_line: self.curr_line += 1

    def run_before_second_time(self):
        while self.num_exec_lines[self.curr_line] != 1:
            self.step_code()

    def init_run_code(self):
        self.init_context_vars()
        while self.num_exec_lines[self.curr_line] < 1 and self.curr_line < len(self.lines):
            self.step_code()
        if self.num_exec_lines[self.curr_line] == 1:
            return False
        elif self.curr_line >= len(self.lines):
            return True
        raise RuntimeError()

import timeit

input_path = 'input.txt'
c = CodeRunner(input_path)
start = timeit.default_timer()
c.run_before_second_time()
end = timeit.default_timer()
print('python time', end - start)
print(c.acc)

c = CodeRunnerCython(input_path)
start = timeit.default_timer()
c.run_before_second_time()
end = timeit.default_timer()
print('cython time', end - start)
print(c.get_acc())


print(c.solution2())