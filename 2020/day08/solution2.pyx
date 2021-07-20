from libc.stdlib cimport malloc, free

cdef class CodeRunner:

    cdef str input_path
    cdef int acc, curr_line, num_lines
    cdef int * num_exec_lines
    cdef list lines

    def __cinit__(self, str input_path = 'input.txt'):
        self.lines = self.parse_input(input_path)
        self.num_lines = len(self.lines)
        self.init_context_vars()

    def init_context_vars(self):
        free(self.num_exec_lines)
        self.num_exec_lines = <int *> malloc(self.num_lines * sizeof(int))
        for i in range(self.num_lines): self.num_exec_lines[i] = 0
        self.acc = 0
        self.curr_line = 0

    def parse_input(self, input_path):
        with open(input_path, 'r') as f:
            data = [x.split(' ') for x in f.read().split('\n')]
        data = [(l[0], int(l[1])) for l in data]
        return data

    cdef step_code(self):
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

    cpdef run_before_second_time(self):
        while self.num_exec_lines[self.curr_line] != 1:
            self.step_code()

    def get_acc(self):
        return self.acc

    def init_run_code(self):
        self.init_context_vars()
        while self.num_exec_lines[self.curr_line] < 2 and self.curr_line < self.num_lines:
            self.step_code()
        if self.curr_line >= len(self.lines):
            return True
        if self.num_exec_lines[self.curr_line] == 2:
            return False
        raise RuntimeError()

    cdef list code_alterations(self):
        candidates = []
        cdef i = 0
        for (op_name, op_value) in self.lines:
            if op_name == 'nop':
                candidates.append((i, 'jmp'))
            elif op_name == 'jmp':
                candidates.append((i, 'nop'))
            i += 1
        return candidates

    cpdef solution2(self):
        alterations = self.code_alterations()
        orig_lines = self.lines[:]
        for i_line, new_opname in alterations:
            self.lines = orig_lines[:]
            self.lines[i_line] = (new_opname, self.lines[i_line][1])
            if self.init_run_code():
                return self.acc
        
