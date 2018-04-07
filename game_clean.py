

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


test_empty_board_moves()
            
                    
