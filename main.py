from BoardGame import Board, get_board_tiles
import numpy as np


def solve(board: Board, tiles_used: list = None, tiles: np.array = None, depth: int = 0):
    print(f"depth: {depth}")
    tiles_used = [] if tiles_used is None else tiles_used
    tiles = get_board_tiles() if tiles is None else tiles
    next_coord = None
    for y, row in enumerate(board):
        for x, field in enumerate(row):
            if not field:
                next_coord = np.array([y-4, x-4], dtype=int)
                break
    if next_coord is None:
        # return []
        print(f"tiles used: {tiles_used}")
        return board
    for tile_idx, unused_tile in enumerate(tiles):
        if tile_idx not in tiles_used:
            for tile_center in range(5):
                for orientation in range(3):
                    sub_tiles = unused_tile.get_tiles(tile_center, orientation) + next_coord
                    if board.check_tile_fits(sub_tiles):
                        new_board = board.update_board(sub_tiles, tile_idx)
                        result = solve(new_board, tiles_used + [tile_idx], tiles, depth+1)
                        if result is not None:
                            # return result + [(tile_idx, tile_center, orientation, next_coord)]
                            return result

    return None


def main():
    board = Board()
    print(board)
    print(solve(board)._idx_board)


if __name__ == '__main__':
    main()
