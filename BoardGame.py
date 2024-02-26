import numpy as np
from copy import deepcopy


class BoardTile:
    def __init__(self, tiles: np.array):
        tiles.dtype = int
        orientation1 = tiles
        third_coord = np.sum(orientation1, axis=1) * -1
        orientation2 = np.empty(orientation1.shape, dtype=int)
        orientation3 = np.empty(orientation1.shape, dtype=int)
        for idx, ((a, b), c) in enumerate(zip(orientation1, third_coord)):
            orientation2[idx, 0] = c
            orientation2[idx, 1] = a
            orientation3[idx, 0] = b
            orientation3[idx, 1] = c
        self.tiles = [orientation1, orientation2, orientation3]

    def get_tiles(self, tile_center: int, orientation: int) -> np.array:
        if tile_center > 5 or tile_center < 0:
            raise ValueError(f"Expected 0 <= tile_center <= 4, but got {tile_center} instead")
        if orientation > 3 or orientation < 0:
            raise ValueError(f"Expected 0 <= orientation <= 2, but got {orientation} instead")
        tiles = self.tiles[orientation]
        return tiles - tiles[tile_center]


def get_board_tiles():
    return [
        BoardTile(np.array([[0, 0], [1, 0], [2, 0], [1, -1], [1, -2]], dtype=int)),
        BoardTile(np.array([[0, 0], [1, 0], [0, 1], [1, 1], [1, 2]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [0, 2], [1, 2], [2, 2]], dtype=int)),
        BoardTile(np.array([[0, 0], [1, -1], [1, 0], [2, 0], [2, 1]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [1, 1], [2, 0], [2, 1]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [1, 1], [2, 1], [1, 2]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [0, 2], [1, 1], [1, 2]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [0, 2], [0, 3], [1, 3]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [0, 2], [0, 3], [1, 0]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [0, 2], [1, 0], [2, -1]], dtype=int)),
        BoardTile(np.array([[0, 0], [1, 0], [1, 1], [1, 2], [2, -1]], dtype=int)),
        BoardTile(np.array([[0, 0], [0, 1], [1, 1], [1, 2], [1, 3]], dtype=int))
    ]


def get_coords(*args):
    y, x = None, None
    if len(args) == 1:
        if isinstance(args[0], int):
            y = args[0] + 4
        elif isinstance(args[0], np.ndarray):
            y, x = args[0][0] + 4, args[0][1] + 4
        else:
            y, x = next(args[0]) + 4, next(args[0]) + 4
    else:
        y, x = args[0] + 4, args[1] + 4

    return y, x


class Board:
    def __init__(self):
        self._board = np.zeros((9, 9), dtype=bool)
        self._board[4, 4] = True
        for i in range(9):
            for j in range(i, 9):
                if np.abs(i+j-8) > 4:
                    self._board[i, j] = True
                    self._board[j, i] = True
        self._idx_board = np.ones((9, 9), dtype=int) * -1

    def __getitem__(self, *args):
        y, x = get_coords(*args)
        if y < 0 or y >= self._board.shape[0]:
            return True

        if x is not None:
            if x < 0 or x >= self._board.shape[1]:
                return True
            return self._board[y, x]
        return self._board[y]

    def __setitem__(self, *args):
        v = args[-1]
        y, x = get_coords(*(args[:-1]))
        if x is None:
            self._board[y] = v[0]
            self._idx_board[y] = v[1]
        else:
            self._board[y, x] = v[0]
            self._idx_board[y, x] = v[1]

    def __iter__(self):
        return self._board.__iter__()

    def __str__(self):
        return self._board.__str__()

    def check_tile_fits(self, tiles: np.array) -> bool:
        for tile in tiles:
            if self[tile]:
                return False
        return True

    def update_board(self, tiles: np.array, tile_idx: int):
        new_board = deepcopy(self)
        for tile in tiles:
            new_board[tile] = (True, tile_idx)
        return new_board
