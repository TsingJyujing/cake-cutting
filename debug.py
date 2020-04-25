import logging

from cake_cutting.algorithm import matrix_decomposition, arrangement_algorithm
from cake_cutting.basics import MatrixShape

log = logging.getLogger("DEBUG_PROG")

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # matrix_decomposition("test", MatrixShape(340, 220), MatrixShape(120, 120), MatrixShape(10, 10)).display()
    matrix_decomposition("test", MatrixShape(121, 121), MatrixShape(120, 120), MatrixShape(10, 10)).display()
    for i, cc in enumerate(
            arrangement_algorithm(
                [
                    MatrixShape(121, 121),
                    MatrixShape(121, 121),
                    MatrixShape(121, 121),
                    MatrixShape(121, 121),
                    MatrixShape(121, 121),
                    MatrixShape(121, 121),
                ],
                container_size=MatrixShape(120, 120),
                padding_size=MatrixShape(10, 10)
            )
    ):
        log.debug("CakeContainer {}".format(i))
        cc.display()
