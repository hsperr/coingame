import copy

class Board():
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = -1

    DRAW = 'Draw'
    NO_WINNER = "No Winner"
    INVALID_MOVE = "Invalid Move"

    STANDARD_BOARD = [
        [ PLAYER1, PLAYER1, EMPTY, PLAYER2, PLAYER2],
        [ PLAYER1, PLAYER1, EMPTY, PLAYER2, PLAYER2],
        [  EMPTY,   EMPTY,  EMPTY,  EMPTY,   EMPTY],
        [ PLAYER2, PLAYER2, EMPTY, PLAYER1, PLAYER1],
        [ PLAYER2, PLAYER2, EMPTY, PLAYER1, PLAYER1]
    ]
    STANDARD_BEGINNING_PLAYER = PLAYER1

    @classmethod
    def from_string(cls, board, current_player, allow_diagonals=False):
        result = []
        board = board.strip()
        for line in board.split('\n'):
            line = line.strip()
            line_res = []
            for entry in line:
                if entry == 'X':
                    line_res.append(Board.PLAYER1)
                elif entry == 'O':
                    line_res.append(Board.PLAYER2)
                else:
                    line_res.append(Board.EMPTY)
            result.append(line_res)
        return cls.from_array(result, Board.PLAYER1 if current_player=='X' else Board.PLAYER2, allow_diagonals)

    def valid_position(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y


class ArrayBoard(Board):
    def __init__(self, board, current_player, allow_diagonals=False):
        self.board = copy.deepcopy(board)
        self.current_player = current_player
        if self.current_player == ArrayBoard.PLAYER1:
            self.other_player = ArrayBoard.PLAYER2
        else:
            self.other_player = ArrayBoard.PLAYER1

        self.history = []
        self.allow_diagonals = allow_diagonals

    @classmethod
    def from_array(cls, board, current_player, allow_diagonals=False):
        return cls(board, current_player, allow_diagonals=allow_diagonals)

    @classmethod
    def standard_board(cls, allow_diagonals=False):
        return cls(ArrayBoard.STANDARD_BOARD, ArrayBoard.STANDARD_BEGINNING_PLAYER, allow_diagonals=allow_diagonals)


    @property
    def size_x(self):
        return len(self.board[0])

    @property
    def size_y(self):
        return len(self.board)

    def _get_normal_neighbors(self, x, y):
        return [p for p in [(x+1, y), (x-1, y), (x, y+1), (x, y-1) ] if self.valid_position(p[0], p[1])]

    def _get_diagonal_neighbors(self, x, y):
        return [p for p in [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1) ] if self.valid_position(p[0], p[1])]

    def _get_all_neighbors(self, x, y):
        if self.allow_diagonals:
            return self._get_normal_neighbors(x, y) + self._get_diagonal_neighbors(x, y)
        else:
            return self._get_normal_neighbors(x, y)

    def get_moves(self):
        possible_moves = []
        for y, row in enumerate(self.board):
            for x, field in enumerate(row):
                if not field == self.current_player:
                    continue
                possible_moves.extend([((x,y), n) for n in self._get_all_neighbors(x, y) if self.board[n[1]][n[0]] == ArrayBoard.EMPTY])
        return possible_moves

    def value(self, x, y):
        return self.board[y][x]

    def copy(self):
        import copy
        board_copy = ArrayBoard.standard_board()
        board_copy.board = copy.deepcopy(self.board)
        board_copy.current_player = self.current_player
        board_copy.history = copy.deepcopy(self.history)
        board_copy.allow_diagonals = self.allow_diagonals

        return board_copy

    def empty(self, x, y):
        self.board[y][x] = ArrayBoard.EMPTY

    def set_player_at(self, x, y, player):
        self.board[y][x] = player

    def move(self, move):
        (from_x, from_y), (to_x, to_y) = move
        if not self.valid_position(from_x, from_y) or not self.valid_position(to_x, to_y):
            return ArrayBoard.INVALID_MOVE

        if not self.value(from_x, from_y) == self.current_player:
            return ArrayBoard.INVALID_MOVE

        if not self.value(to_x, to_y) == ArrayBoard.EMPTY:
            return ArrayBoard.INVALID_MOVE

        to_neighbors = self._get_all_neighbors(to_x, to_y)
        if not (from_x, from_y) in to_neighbors:
            return ArrayBoard.INVALID_MOVE

        changes = []
        self.set_player_at(to_x, to_y, self.current_player)
        self.empty(from_x, from_y)

        to_neighbors = self._get_normal_neighbors(to_x, to_y)
        for n_x, n_y in to_neighbors:
            if self.value(n_x, n_y) and not self.value(n_x, n_y) == self.current_player:
                self.set_player_at(n_x, n_y, self.current_player)
                changes.append((n_x, n_y))

        to_neighbors = self._get_diagonal_neighbors(to_x, to_y)
        for diag_x, diag_y in to_neighbors:
            if self.value(diag_x, diag_y) and not self.value(diag_x, diag_y) == self.current_player:
                diag_n = self._get_normal_neighbors(diag_x, diag_y)
                if len(set(changes).intersection(diag_n)) == 2:
                    self.set_player_at(diag_x, diag_y, self.current_player)
                    changes.append((diag_x, diag_y))

        self.history.append((move, changes))

        self.switch_player()

        return self

    def switch_player(self):
        if self.current_player == ArrayBoard.PLAYER1:
            self.current_player = ArrayBoard.PLAYER2
            self.other_player = ArrayBoard.PLAYER1
        else:
            self.current_player = ArrayBoard.PLAYER1
            self.other_player = ArrayBoard.PLAYER2

    def undo(self):
        ((to_x, to_y), (from_x, from_y)), changes = self.history.pop()

        for x, y in changes:
            self.set_player_at(x, y, self.current_player)

        self.switch_player()
        self.set_player_at(to_x, to_y, self.current_player)
        self.empty(from_x, from_y)

    def winner(self):
        moves = self.get_moves()
        if not moves:
            return ArrayBoard.PLAYER1 if self.current_player == ArrayBoard.PLAYER2 else ArrayBoard.PLAYER2

        self.switch_player()
        moves = self.get_moves()
        self.switch_player()
        if not moves:
            return ArrayBoard.PLAYER1 if not self.current_player == ArrayBoard.PLAYER2 else ArrayBoard.PLAYER2

        return ArrayBoard.NO_WINNER

    def get_num_occupied_fields(self, player):
        return sum(1 for row in self.board for field in row if field == player)

    def hash(self):
        return hash(str(self.board)+str(self.current_player))

    def rotate_left(self):
        new_board = self.copy()
        new_board.board = [list(x) for x in list(zip(*reversed(self.board)))]
        return new_board


