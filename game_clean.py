

class Board():
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = -1

    def __init__(self, allow_diagonals=False):
        self.board = [
                [ 1, 1, 0,-1,-1],
                [ 1, 1, 0,-1,-1],
                [ 0, 0, 0, 0, 0],
                [-1,-1, 0, 1, 1],
                [-1,-1, 0, 1, 1]
        ]
        self.current_player = Board.PLAYER1
        self.history = []
        self.allow_diagonals = allow_diagonals

    def valid_position(self, x, y):
        return 0 <= x < self.size_x and 0 <= y < self.size_y

    @property
    def size_x(self):
        return len(self.board[0])

    @property
    def size_y(self):
        return len(self.board)

    def get_normal_neighbors(self, x, y):
        return  [p for p in [(x+1, y), (x-1, y), (x, y+1), (x, y-1) ] if self.valid_position(p[0], p[1])]

    def get_diagonal_neighbors(self, x, y):
        return [p for p in [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1) ] if self.valid_position(p[0], p[1])]

    def get_all_neighbors(self, x, y):
        if self.allow_diagonals:
            return self.get_normal_neighbors(x, y) + self.get_diagonal_neighbors(x, y)
        else:
            return self.get_normal_neighbors(x, y)

    def get_moves(self):
        possible_moves = []
        for y, row in enumerate(self.board):
            for x, field in enumerate(row):
                if not field == self.current_player:
                    continue
                possible_moves.extend([((x,y), n) for n in self.get_all_neighbors(x, y) if self.board[n[1]][n[0]] == Board.EMPTY])
        return possible_moves

    def _value(self, x, y):
        return self.board[y][x]

    def empty(self, x, y):
        self.board[y][x] = Board.EMPTY

    def set_player_at(self, x, y, player):
        self.board[y][x] = player

    def move(self, move):
        (from_x, from_y), (to_x, to_y) = move
        if not self.valid_position(from_x, from_y) or not self.valid_position(to_x, to_y):
            return "Invalid move"

        if not self._value(from_x, from_y) == self.current_player:
            return "Invalid move"

        if not self._value(to_x, to_y) == Board.EMPTY:
            return "Invalid move"

        to_neighbors = self.get_all_neighbors(to_x, to_y)
        if not (from_x, from_y) in to_neighbors:
            return "Invalid move"

        changes = []
        self.set_player_at(to_x, to_y, self.current_player)
        self.empty(from_x, from_y)

        to_neighbors = self.get_normal_neighbors(to_x, to_y)
        print(to_neighbors)
        for n_x, n_y in to_neighbors:
            if self._value(n_x, n_y) and not self._value(n_x, n_y) == self.current_player:
                self.set_player_at(n_x, n_y, self.current_player)
                changes.append((n_x, n_y))

        to_neighbors = self.get_diagonal_neighbors(to_x, to_y)
        for diag_x, diag_y in to_neighbors:
            if self._value(diag_x, diag_y) and not self._value(diag_x, diag_y) == self.current_player:
                diag_n = self.get_normal_neighbors(diag_x, diag_y)
                if len(set(changes).intersection(diag_n)) == 2:
                    self.set_player_at(diag_x, diag_y, self.current_player)
                    changes.append((diag_x, diag_y))

        if self.current_player == Board.PLAYER1:
            self.current_player = Board.PLAYER2
        else:
            self.current_player = Board.PLAYER1

        self.history.append((move, changes))

        return self

    def print_board(self):
        print("Current move: {}, Turn for: {}".format(len(self.history), "X" if self.current_player==Board.PLAYER1 else "O"))
        for row in self.board:
            for field in row:
                if field == Board.PLAYER1:
                    print("X", end='')
                elif field == Board.PLAYER2:
                    print("O", end='')
                else:
                    print(".", end='')
            print('')
        print('****************')

                
def test_empty_board_moves():
    board = Board()
    moves  = board.get_moves()
    assert len(moves) == 8

    board = Board(allow_diagonals=True)
    moves  = board.get_moves()
    assert len(moves) == 18

def test_board_valid_position():
    board = Board()
    assert board.valid_position(0, 0)
    assert board.valid_position(2, 3)
    assert not board.valid_position(0, board.size_y)
    assert not board.valid_position(board.size_x, 0)
    assert not board.valid_position(board.size_x, board.size_y)
    assert board.valid_position(board.size_x-1, 0)
    assert board.valid_position(0, board.size_y-1)
    assert board.valid_position(board.size_x-1, board.size_y-1)

def test_board_neighbor_fields():
    board = Board()
    assert board.get_normal_neighbors(0, 0) == [(1,0), (0,1)]
    assert board.get_normal_neighbors(1, 0) == [(2,0), (0,0), (1, 1)]
    assert board.get_normal_neighbors(2, 3) == [(3, 3), (1, 3), (2, 4), (2, 2)]

    board = Board(allow_diagonals=True)
    assert board.get_all_neighbors(0, 0) == [(1,0), (0,1), (1,1)]
    assert board.get_all_neighbors(2, 3) == [(3, 3), (1, 3), (2, 4), (2, 2), (3, 4), (3, 2), (1, 4), (1, 2)]

def test_board_move():
    board = Board()
    board.print_board()
    assert board.move(((-1,0), (0,0))) == "Invalid move"
    assert board.move(((4,0), (3,0))) == "Invalid move"
    assert board.move(((1,0), (3,0))) == "Invalid move"

    assert not board.move(((1,0), (2,0))) == "Invalid move"
    assert board._value(1,0) == Board.EMPTY
    assert board._value(2,0) == Board.PLAYER1
    assert board.current_player == Board.PLAYER2

    assert board.move(((2,0), (3,0))) == "Invalid move"
    board.print_board()

    assert not board.move(((3,1), (2,1))) == "Invalid move"
    board.print_board()
    assert board._value(3,1) == Board.EMPTY
    assert board._value(2,1) == Board.PLAYER2
    assert board._value(2,0) == Board.PLAYER2
    assert board.current_player == Board.PLAYER1

    assert not board.move(((0,0), (1,0))) == "Invalid move"
    board.print_board()
    assert board._value(1,0) == Board.PLAYER1
    assert board._value(2,0) == Board.PLAYER1
    assert board._value(1,1) == Board.PLAYER1
    assert board._value(2,1) == Board.PLAYER1

test_empty_board_moves()
test_board_valid_position()
test_board_neighbor_fields()
test_board_move()
            
                    
