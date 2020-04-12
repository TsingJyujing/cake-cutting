from typing import List


class MatrixShape:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width

    @property
    def shape(self):
        return (
            self.width, self.height
        )

    def __contains__(self, item):
        if isinstance(item, MatrixShape):
            return item.width < self.width and item.height < self.height
        else:
            raise Exception(f"Unknown type: {str(type(item))}")


class MatrixPiece:
    def __init__(self, left: int, top: int, width: int, height: int):
        self.height = height
        self.width = width
        self.left = left
        self.top = top

    @property
    def location(self):
        return (
            self.left,
            self.top,
            self.left + self.width,
            self.top + self.height,
        )

    @property
    def shape(self):
        return (
            self.width, self.height
        )

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    def __str__(self):
        return f"[{self.left}:{self.right},{self.top}:{self.bottom}]"


class PieceMapping:
    def __init__(self, original_id, container_loc: MatrixPiece, original_loc: MatrixPiece, padding: int = 0):
        self.padding = padding
        self.original_loc = original_loc
        self.container_loc = container_loc
        self.original_id = original_id
        if original_loc.shape != container_loc.shape:
            raise ValueError(f"Can't mapping from size {original_loc.shape} to size {container_loc.shape}!")

    def __str__(self):
        return f"{self.original_id}:{str(self.original_loc)}->{str(self.container_loc)}"


class CakeContainer:
    def __init__(self, pieces: List[PieceMapping]):
        self.pieces = pieces