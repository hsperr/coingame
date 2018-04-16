from ArrayBoard import Board

import random
import copy


class BitBoard(Board):

    @classmethod
    def from_array(cls, board, current_player, allow_diagonals=False):
        player1 = 0b0000000000000000000000000
        player2 = 0b0000000000000000000000000
        for y, row in enumerate(board):
            for x, field in enumerate(row):
                if field == Board.PLAYER1:
                    player1 |= 1 << BitBoard.pos_to_int(x, y, len(board))
                elif field == Board.PLAYER2:
                    player2 |= 1 << BitBoard.pos_to_int(x, y, len(board))

        size_x = len(board[0])
        size_y = len(board)

        return BitBoard(player1=player1, player2=player2, current_player=current_player, size_x=size_x, size_y=size_y,
                        allow_diagonals=allow_diagonals)

    @classmethod
    def standard_board(cls, allow_diagonals=False):
        return cls.from_array(Board.STANDARD_BOARD, Board.STANDARD_BEGINNING_PLAYER, allow_diagonals)

    def __init__(self, player1, player2, current_player, size_x, size_y, allow_diagonals=False):
        self.player1 = player1
        self.player2 = player2
        self.current_player = current_player

        self.right_border = int('1'.zfill(size_x) * size_y, 2)
        self.left_border = int(bin(1 << size_x - 1)[2:] * size_y, 2)
        self.top_border = int('1' * size_x, 2) << (size_x * (size_y - 1))
        self.bottom_border = int(('1' * size_x), 2)

        self.top_right = self.right_border | self.top_border
        self.top_left = self.left_border | self.top_border
        self.bottom_right = self.right_border | self.bottom_border
        self.bottom_left = self.left_border | self.bottom_border

        self.size_x = size_x
        self.size_y = size_y

        self.allow_diagonals = allow_diagonals
        self.history = []

    def copy(self):
        board = BitBoard(self.player1, self.player2, self.current_player, self.size_x, self.size_y, self.allow_diagonals)
        board.history = copy.deepcopy(self.history)
        return board

    @property
    def other_player(self):
        if self.current_player == Board.PLAYER1:
            return Board.PLAYER2
        else:
            return Board.PLAYER1

    @property
    def board(self):
        return bin(self.player1).split('b')[1].zfill(self.size_x * self.size_y) + bin(self.player2).split('b')[1].zfill(self.size_x * self.size_y)

    def hash(self):
        return hash(self.board + str(self.current_player))

    def invert(self, b):
        return int('1' * self.size_x * self.size_y, 2) - b

    def winner(self):
        if not self._get_moves_for(self.player1):
            return Board.PLAYER2
        elif not self._get_moves_for(self.player2):
            return Board.PLAYER1

        return Board.NO_WINNER

    def _bit_scan(self, b):
        positions = []
        for idx, bit in enumerate(bin(b)[2:].zfill(25)):
            if bit == '1':
                positions.append(self.int_to_pos(idx, self.size_x))
        return positions

    @staticmethod
    def int_to_pos(depth, row_size):
        return (depth % row_size, depth // row_size)

    @staticmethod
    def pos_to_int(x, y, row_size):
        return row_size ** 2 - (y * row_size + x) - 1

    def _pos_to_int(self, x, y):
        return BitBoard.pos_to_int(x, y, self.size_x)

    def _pretty_print(self, b):
        str_rep = bin(b).split('b')[1].zfill(self.size_x * self.size_y)
        for i in range(self.size_y):
            for j in range(self.size_x):
                print(str_rep[i * self.size_x + j], end='')
            print()
        print("****")

    def value(self, x, y):
        depth = self._pos_to_int(x, y)

        is_current_player = (1 << depth) & self.player1
        if is_current_player:
            return Board.PLAYER1

        is_other_player = (1 << depth) & self.player2
        if is_other_player:
            return Board.PLAYER2

        return Board.EMPTY

    def move(self, move):
        ((from_x, from_y), (to_x, to_y)) = move

        if not self.valid_position(from_x, from_y) or not self.valid_position(to_x, to_y):
            print('val pos', self.valid_position(from_x, from_y), self.valid_position(to_x, to_y))
            return Board.INVALID_MOVE

        if not self.value(from_x, from_y) == self.current_player:
            print('value', self.value(from_x, from_y), self.current_player)
            return Board.INVALID_MOVE

        if not self.value(to_x, to_y) == Board.EMPTY:
            print('empty', self.value(to_x, to_y) == Board.EMPTY)
            return Board.INVALID_MOVE

        if self.current_player == Board.PLAYER1:
            player = self.player1
            other_player = self.player2
        else:
            player = self.player2
            other_player = self.player1

        self.history.append((
            self.player1, self.player2, self.current_player
        ))

        player = player ^ (1 << self._pos_to_int(from_x, from_y))
        player = player ^ (1 << self._pos_to_int(to_x, to_y))

        to_pos = (1 << self._pos_to_int(to_x, to_y))

        to_pos = ((to_pos << 1) | (to_pos >> 1) | (to_pos << self.size_x) | (to_pos >> self.size_x)) & other_player

        player = player ^ to_pos
        other_player = other_player ^ to_pos

        to_pos = ((to_pos << 1) & (to_pos << self.size_x) |
                  (to_pos << 1) & (to_pos >> self.size_x) |
                  (to_pos >> 1) & (to_pos << self.size_x) |
                  (to_pos >> 1) & (to_pos >> self.size_x)) & other_player

        player = player ^ to_pos
        other_player = other_player ^ to_pos

        if self.current_player == Board.PLAYER1:
            self.player1 = player
            self.player2 = other_player
            self.current_player = Board.PLAYER2
        else:
            self.player2 = player
            self.player1 = other_player
            self.current_player = Board.PLAYER1

        return self

    def undo(self):
        self.player1, self.player2, self.current_player = self.history[-1]
        self.history = self.history[:-1]

    def get_moves(self):
        if self.current_player == Board.PLAYER1:
            return self._get_moves_for(self.player1)
        else:
            return self._get_moves_for(self.player2)

    def get_num_occupied_fields(self, player):
        if player == Board.PLAYER1:
            return len(self._bit_scan(self.player1))
        if player == Board.PLAYER2:
            return len(self._bit_scan(self.player2))

    def _get_moves_for(self, player):
        empty = self.invert(self.player1 | self.player2)

        left_moves = (player ^ (player & self.left_border)) << 1 & empty
        left_moves = [((point[0] + 1, point[1]), point) for point in self._bit_scan(left_moves)]

        right_moves = (player ^ (player & self.right_border)) >> 1 & empty
        right_moves = [((point[0] - 1, point[1]), point) for point in self._bit_scan(right_moves)]

        top_moves = (player ^ (player & self.top_border)) << self.size_x & empty
        top_moves = [((point[0], point[1] + 1), point) for point in self._bit_scan(top_moves)]

        bottom_moves = (player ^ (player & self.bottom_border)) >> self.size_x & empty
        bottom_moves = [((point[0], point[1] - 1), point) for point in self._bit_scan(bottom_moves)]

        moves = left_moves + right_moves + top_moves + bottom_moves

        if self.allow_diagonals:
            top_left = (player ^ (player & self.top_left)) << self.size_x+1 & empty
            top_left = [((point[0] + 1, point[1] + 1), point) for point in self._bit_scan(top_left)]

            top_right = (player ^ (player & self.top_right)) << self.size_x-1 & empty
            top_right = [((point[0] - 1, point[1] + 1), point) for point in self._bit_scan(top_right)]

            bottom_left = (player ^ (player & self.bottom_left)) >> self.size_x-1 & empty
            bottom_left = [((point[0] + 1, point[1] - 1), point) for point in self._bit_scan(bottom_left)]

            bottom_right = (player ^ (player & self.bottom_right)) >> self.size_x+1 & empty
            bottom_right = [((point[0] - 1, point[1] - 1), point) for point in self._bit_scan(bottom_right)]

            moves = moves + top_right + top_left + bottom_left + bottom_right

        return moves
