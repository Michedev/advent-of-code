import re
from operator import add, mul

from path import Path
verbose = False

class Parser:

    def __init__(self, expression: str):
        self.expression = expression
        self.regex_op = re.compile(r'\s*([+*])\s*')
        self.regex_value = re.compile(r'\s*(\d+)\s*')
        self.regex_par = re.compile(r'\((.+)\)')

    
    def parse_input(self, input_path):
        with open(input_path) as f:
            data = f.read().split('\n')
        return [cls(x) for x in data if x]

    def find_par_expr(self, expr: str, i: int):
        assert expr[i] == '('
        open_pars = 1
        i_init = i + 1
        i = i + 1
        while open_pars > 0:
            if expr[i] == '(':
                open_pars += 1
            elif expr[i] == ')':
                open_pars -= 1
            i += 1
        return expr[i_init:i - 1]

    def eval_expr(self, expr=None):
        if not expr: expr = self.expression
        i = 0
        l_value, r_value, operator = None, None, None
        while i < len(expr) or operator is not None:
            if l_value is None or operator is not None and r_value is None:
                delta, l_value, r_value = self.match_value(expr, i, l_value, r_value)
                if verbose: print(f'{delta = }, {l_value = }, {r_value = }')
                i += delta
            elif operator is None:
                delta, operator = self.match_operator(expr, i)
                if verbose: print('operator =', operator)
                i += delta
            else:
                assert all(x is not None for x in (l_value, r_value, operator))
                result = operator(l_value, r_value)
                if verbose: print(f'{l_value} {operator} {r_value} = {result}', )
                l_value = result
                if verbose: print('set l_value =', l_value)
                operator = r_value = None

            if verbose and i < len(expr): print('Now you are here (|):', expr[:i - 1], '|', expr[i], '|', expr[i + 1:])
        return l_value

    def match_value(self, expr, i, l_value, r_value):
        val_match = self.regex_value.match(expr, i)
        par_match = self.regex_par.match(expr, i)
        assert not (val_match is None and par_match is None)
        if val_match is None:
            par_expr = self.find_par_expr(expr, i)
            if verbose: print('starting evaluating', par_expr)
            l_value, r_value = self.match_par(par_expr, l_value, r_value)
            if verbose: print('finish eval', par_expr)
            return len(par_expr) + 2, l_value, r_value
        elif par_match is None:
            l_value, r_value = self.match_num(val_match, l_value, r_value)
            span = val_match.span()
            return span[1] - span[0], l_value, r_value
        else:
            match = min(par_match, val_match, key=lambda m: m.span()[0])
            if match == val_match:
                l_value, r_value = self.match_num(match, l_value, r_value)
            elif match == par_match:
                par_expr = self.find_par_expr(expr, i)
                l_value, r_value = self.match_par(par_expr, l_value, r_value)
            else:
                raise ValueError()
            span = match.span()
            return span[1] - span[0], l_value, r_value

    def match_par(self, par_expr, l_value, r_value):
        new_value = self.eval_expr(par_expr)
        l_value, r_value = self.set_new_value_(new_value, l_value, r_value)
        return l_value, r_value

    def set_new_value_(self, new_value, l_value, r_value):
        if l_value is None:
            l_value = new_value
        else:
            r_value = new_value
        return l_value, r_value

    def match_num(self, match, l_value, r_value):
        num = int(match.group(0))
        l_value, r_value = self.set_new_value_(num, l_value, r_value)
        return l_value, r_value

    def match_operator(self, expr, i):
        m = self.regex_op.match(expr, i)
        operator = m.group(0).strip()
        if operator == '+':
            operator = add
        else:
            operator = mul
        span = m.span()
        return span[1] - span[0], operator


class Parser2(Parser):

    def __init__(self, expression: str):
        super().__init__(expression)
        self.regex_par = re.compile(r'\(([\d\s\*\+]+)\)')
        self.sum_op_regex = re.compile('\s*(\d+)\s*\+\s*(\d+)\s*')
        self.mul_op_regex = re.compile('\s*(\d+)\s*\*\s*(\d+)\s*')

    def eval_expr(self, expr=None):
        expr = expr or self.expression
        while (m := self.regex_par.search(expr)) is not None:
            sub_expr = m.group(1)
            result = self.eval_expr(sub_expr)
            expr = expr.replace(f'({sub_expr})', str(result))
        while (m := self.sum_op_regex.search(expr)) is not None:
            num1, num2 = int(m.group(1)), int(m.group(2))
            expr = expr.replace(m.group(0), str(num1 + num2))
        while (m := self.mul_op_regex.search(expr)) is not None:
            num1, num2 = int(m.group(1)), int(m.group(2))
            expr = expr.replace(m.group(0), str(num1 * num2))
        return int(expr.strip())


def test_expressions():
    p = Parser('2 * 3 + (4 * 5)')
    assert p.eval_expr() == 26
    p.expression = '5 + (8 * 3 + 9 + 3 * 4 * 3)'
    assert p.eval_expr() == 437
    p.expression = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
    assert p.eval_expr() == 12240
    p.expression = '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'
    assert p.eval_expr() == 13632

def test2_expressions():
    p = Parser2('1 + (2 * 3) + (4 * (5 + 6))')
    assert p.eval_expr() == 51
    p.expression = '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'
    assert p.eval_expr() == 669060

if __name__ == '__main__':
    input_path = Path(__file__).parent / 'input.txt'
    parsers = Parser2.parse_input(input_path)
    result = sum(p.eval_expr() for p in parsers)
    print(result)
