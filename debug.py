import logging

from cake_cutting.algorithm import matrix_decomposition
from cake_cutting.basics import MatrixShape

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # matrix_decomposition("test", MatrixShape(340, 220), MatrixShape(120, 120), MatrixShape(10, 10)).display()
    matrix_decomposition("test", MatrixShape(121, 121), MatrixShape(120, 120), MatrixShape(10, 10)).display()
