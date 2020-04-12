import logging
from functools import reduce
from math import floor
from typing import Union, Mapping, List, Sequence, Tuple

from .basics import CakeContainer, MatrixShape, MatrixPiece

log = logging.getLogger(__file__)


class PiecesCollection:
    def __init__(self):
        self.full: List[Tuple[object, MatrixPiece]] = []
        self.fit_width: List[Tuple[object, MatrixPiece]] = []
        self.fit_height: List[Tuple[object, MatrixPiece]] = []
        self.small: List[Tuple[object, MatrixPiece]] = []

    def __add__(self, other):
        pc = PiecesCollection()
        pc.full = self.full + other.full
        pc.fit_width = self.fit_width + other.fit_width
        pc.fit_height = self.fit_height + other.fit_height
        pc.small = self.small + other.small
        return pc

    def display(self):
        for name, data in (
                ("full", self.full),
                ("fit_width", self.fit_width),
                ("fit_height", self.fit_height),
                ("small", self.small),
        ):
            log.debug(f"Show the list of {name}")
            for mat_id, mp in data:
                log.debug(f"Matrix ID: {str(mat_id)}  Piece: {str(mp)}")


def matrix_decomposition(
        mat_id,
        mat: MatrixShape,
        container_size: MatrixShape,
        padding_size: MatrixShape
) -> PiecesCollection:
    pieces_collection = PiecesCollection()
    if mat in container_size:
        pieces_collection.small.append((mat_id, MatrixPiece(0, 0, mat.width, mat.height)))
    else:
        valid_width = container_size.width - 2 * padding_size.width
        valid_height = container_size.height - 2 * padding_size.height

        col_count = floor((mat.width - 2 * padding_size.width) * 1.0 / valid_width)
        row_count = floor((mat.height - 2 * padding_size.height) * 1.0 / valid_height)
        # Process the whole blocks
        for i in range(col_count):
            for j in range(row_count):
                pieces_collection.full.append((mat_id, MatrixPiece(
                    i * valid_width,
                    j * valid_height,
                    container_size.width,
                    container_size.height
                )))
        # Process the edges
        x_start = valid_width * col_count
        y_start = valid_height * row_count

        for i in range(col_count):
            pieces_collection.fit_width.append((mat_id, MatrixPiece(
                i * valid_width,
                y_start,
                container_size.width,
                mat.height - y_start,
            )))
        for j in range(row_count):
            pieces_collection.fit_height.append((mat_id, MatrixPiece(
                x_start,
                j * valid_height,
                mat.width - x_start,
                container_size.height,
            )))
        pieces_collection.small.append((mat_id, MatrixPiece(
            x_start,
            y_start,
            mat.width - x_start,
            mat.height - y_start,
        )))
    return pieces_collection


def arrangement_algorithm(
        matrixes: Union[Sequence[MatrixShape], Mapping[str, MatrixShape]],
        cs: MatrixShape,
        ps: MatrixShape
) -> List[CakeContainer]:
    """
    Give an arrangement for input matrixes
    :param matrixes: Padded matrix
    :param cs: container_size
    :param ps: padding size
    :return:
    """
    if isinstance(matrixes, Sequence):
        matrixes: Mapping[str, MatrixShape] = {i: v for i, v in enumerate(matrixes)}

    # Value check
    padding_size_mat = MatrixShape(ps.width * 2, ps.height * 2)
    if padding_size_mat not in cs:
        raise ValueError(f"Container's size {cs.shape} should larger than padding size {padding_size_mat.shape}")
    for mat_id, mat in matrixes.items():
        if padding_size_mat not in mat:
            raise ValueError(f"Matrix {mat_id} is too small. {mat.shape} < {padding_size_mat.shape} ")

    containers = []

    # 1st, cut large images in pieces, make them all less than container size
    pieces_collection = reduce(
        lambda a, b: a + b,
        (
            matrix_decomposition(mat_id, mat, cs, ps)
            for mat_id, mat in matrixes.items()
        )
    )

    return containers
