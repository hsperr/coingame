

class Board():
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = -1

    def __init__(self, allow_diagonals=False):
        self.board = [
                [1,1,0,0,-1,-1],
                [1,1,0,0,-1,-1],
                [0,0,0,0,0,0],
                [0,0,0,0,0,0],
                [-1,-1,0,0,1,1],
                [-1,-1,0,0,1,1]
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

    def get_neighbor_fields(self, x, y):
        normal_moves =  [p for p in [(x+1, y), (x-1, y), (x, y+1), (x, y-1) ] if self.valid_position(p[0], p[1])]
        diagonal_moves =  [p for p in [(x+1, y+1), (x+1, y-1), (x-1, y+1), (x-1, y-1) ] if self.valid_position(p[0], p[1])]
        if self.allow_diagonals:
            return normal_moves + diagonal_moves
        else:
            return normal_moves

    def moves(self):
        possible_moves = []
        for y, row in enumerate(self.board):
            for x, field in enumerate(row):
                if not field == self.current_player:
                    continue
                possible_moves.extend([n for n in self.get_neighbor_fields(x, y) if self.board[n[1]][n[0]] == Board.EMPTY])
        return possible_moves

                
def test_empty_board_moves():
    board = Board()
    moves  = board.moves()
    assert len(moves) == 8

    board = Board(allow_diagonals=True)
    moves  = board.moves()
    assert len(moves) == 18

def test_board_sizes():
    board = Board()
    assert board.size_x == 6
    assert board.size_y == 6

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
    assert board.get_neighbor_fields(0, 0) == [(1,0), (0,1)]
    assert board.get_neighbor_fields(1, 0) == [(2,0), (0,0), (1, 1)]
    assert board.get_neighbor_fields(2, 3) == [(3, 3), (1, 3), (2, 4), (2, 2)]

    board = Board(allow_diagonals=True)
    assert board.get_neighbor_fields(0, 0) == [(1,0), (0,1), (1,1)]
    assert board.get_neighbor_fields(2, 3) == [(3, 3), (1, 3), (2, 4), (2, 2), (3, 4), (3, 2), (1, 4), (1, 2)]


test_empty_board_moves()
test_board_sizes()
test_board_valid_position()
test_board_neighbor_fields()
            
                    
