import time

import numpy as np
import matplotlib.pyplot as plt
import solution1
import solution1_numba
import pandas as pd
import solution1_py
import solution1_nim
import timeit

times = []

for i in range(1, 800, 20):
    for _ in range(5):
        row = dict()
        start = timeit.default_timer()
        cython_sol = solution1.main(i)
        end = timeit.default_timer()
        row['cython'] = end - start
        print('cython', end - start)
        print('cython solution', cython_sol)

        start = timeit.default_timer()
        psol = solution1_py.main(i)
        end = timeit.default_timer()
        row['python'] = end - start
        print('python solution', psol)
        print('python', end - start)


        start = timeit.default_timer()
        solution1_numba.main(i)
        end = timeit.default_timer()
        row['numba'] = end - start
        print('numba', end - start)

        start = timeit.default_timer()
        start = timeit.default_timer()
        solution = solution1_nim.main(i)
        end = timeit.default_timer()
        print('nim solution', solution)
        row['nim'] = end - start
        print('nim', end - start)


        row['size'] = 12 * i
        times.append(row)

data = pd.DataFrame(times)
time_cols = data.columns.drop('size').tolist()
data = data.pivot_table(time_cols, 'size', aggfunc='mean').reset_index()
print(data)
data.plot.line('size', time_cols)
plt.savefig('benchmark_output.png')
plt.show()