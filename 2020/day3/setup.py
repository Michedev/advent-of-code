from distutils.core import setup
from path import Path

import numpy
from Cython.Build import cythonize

setup(
    name="day3",
    ext_modules=cythonize("solution1.pyx"),
    include_dirs=[numpy.get_include()],
    options={'build_ext':{'inplace':True}},
)

ROOT = Path(__file__).parent
(ROOT / 'build').rmtree_p()
(ROOT / 'solution1.c').remove_p()