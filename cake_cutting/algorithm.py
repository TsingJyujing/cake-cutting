import logging
from functools import reduce
from math import floor
from typing import Union, Mapping, List, Sequence, Tuple

from .basics import CakeContainer, MatrixShape, MatrixPiece, PieceMapping
from .utils import SortedCollection

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
    """
    Split single
    :param mat_id:
    :param mat:
    :param container_size:
    :param padding_size:
    :return:
    """
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

        remain_height = mat.height - y_start
        if remain_height > padding_size.height * 2:
            for i in range(col_count):
                pieces_collection.fit_width.append((mat_id, MatrixPiece(
                    i * valid_width,
                    y_start,
                    container_size.width,
                    remain_height,
                )))
        remain_width = mat.width - x_start
        if remain_width > padding_size.width * 2:
            for j in range(row_count):
                pieces_collection.fit_height.append((mat_id, MatrixPiece(
                    x_start,
                    j * valid_height,
                    remain_width,
                    container_size.height,
                )))
        if remain_width > padding_size.width * 2 and remain_height > padding_size.height * 2:
            pieces_collection.small.append((mat_id, MatrixPiece(
                x_start,
                y_start,
                mat.width - x_start,
                mat.height - y_start,
            )))
    return pieces_collection


def arrangement_algorithm(
        matrixes: Union[Sequence[MatrixShape], Mapping[str, MatrixShape]],
        container_size: MatrixShape,
        padding_size: MatrixShape = None
) -> List[CakeContainer]:
    """
    Give an arrangement for input matrixes
    :param matrixes: Padded matrix
    :param container_size: container_size
    :param padding_size: padding size default (0,0) means no padding
    :return:
    """
    if isinstance(matrixes, Sequence):
        matrixes: Mapping[str, MatrixShape] = {i: v for i, v in enumerate(matrixes)}

    padding_size = padding_size if padding_size is not None else MatrixShape(0, 0)

    # Value check
    padding_size_mat = MatrixShape(padding_size.width * 2, padding_size.height * 2)
    if padding_size_mat not in container_size:
        raise ValueError(
            f"Container's size {container_size.shape} should larger than padding size {padding_size_mat.shape}")
    for mat_id, mat in matrixes.items():
        if padding_size_mat not in mat:
            raise ValueError(f"Matrix {mat_id} is too small. {mat.shape} < {padding_size_mat.shape} ")

    containers: List[CakeContainer] = []

    # cut all large images in pieces, make them all less than container size
    pieces_collection = reduce(
        lambda a, b: a + b,
        (
            matrix_decomposition(mat_id, mat, container_size, padding_size)
            for mat_id, mat in matrixes.items()
        )
    )

    # extract the piece which can obtain whole container
    for mat_id, full_piece in pieces_collection.full:
        containers.append(CakeContainer([PieceMapping(
            original_id=mat_id,
            container_loc=MatrixPiece(0, 0, container_size.width, container_size.height),
            original_loc=full_piece,
            padding=padding_size
        )]))

    # process the fit-width pieces
    sc_width = SortedCollection(pieces_collection.fit_width, key=lambda id_piece: id_piece[1].height)
    while len(sc_width) > 0:
        pieces = []
        remain_size = container_size.height
        while True:
            try:
                mat_id, piece_pop = sc_width.pop_le(remain_size)
                start_index = container_size.height - remain_size
                pieces.append(PieceMapping(
                    original_id=mat_id,
                    original_loc=piece_pop,
                    container_loc=MatrixPiece(0, start_index, container_size.width, piece_pop.height),
                ))
                remain_size -= piece_pop.height
            except ValueError as _:
                containers.append(CakeContainer(pieces))
                pieces = []
                break

    return containers
