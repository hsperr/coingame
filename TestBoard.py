from ArrayBoard import ArrayBoard, Board
from BitBoard import BitBoard


class BoardTestRunner():
    def test_board_empty_moves(self):
        board = self.board.standard_board()
        moves = board.get_moves()
        assert len(moves) == 8

        board = self.board.standard_board(allow_diagonals=True)
        moves = board.get_moves()
        assert len(moves) == 18

    def test_board_valid_position(self):
        board = self.board.standard_board()
        assert board.valid_position(0, 0)
        assert board.valid_position(2, 3)
        assert not board.valid_position(0, board.size_y)
        assert not board.valid_position(board.size_x, 0)
        assert not board.valid_position(board.size_x, board.size_y)
        assert board.valid_position(board.size_x - 1, 0)
        assert board.valid_position(0, board.size_y - 1)
        assert board.valid_position(board.size_x - 1, board.size_y - 1)

    def test_board_move(self):
        board = self.board.standard_board()
        assert board.move(((-1, 0), (0, 0))) == Board.INVALID_MOVE
        assert board.move(((4, 0), (3, 0))) == Board.INVALID_MOVE
        assert board.move(((1, 0), (3, 0))) == Board.INVALID_MOVE

        assert not board.move(((1, 0), (2, 0))) == Board.INVALID_MOVE
        assert board.value(1, 0) == Board.EMPTY
        assert board.value(2, 0) == Board.PLAYER1
        assert board.current_player == Board.PLAYER2

        assert board.move(((2, 0), (3, 0))) == Board.INVALID_MOVE

        assert not board.move(((3, 1), (2, 1))) == Board.INVALID_MOVE
        assert board.value(3, 1) == Board.EMPTY
        assert board.value(2, 1) == Board.PLAYER2
        assert board.value(2, 0) == Board.PLAYER2
        assert board.current_player == Board.PLAYER1

        assert not board.move(((0, 0), (1, 0))) == Board.INVALID_MOVE
        assert board.value(1, 0) == Board.PLAYER1
        assert board.value(2, 0) == Board.PLAYER1
        assert board.value(1, 1) == Board.PLAYER1
        assert board.value(2, 1) == Board.PLAYER1

        board.undo()
        assert board.value(1, 0) == Board.EMPTY
        assert board.value(2, 0) == Board.PLAYER2
        assert board.value(1, 1) == Board.PLAYER2
        assert board.value(2, 1) == Board.PLAYER2

    def test_get_moves(self):
        board = self.board.standard_board()
        assert sorted(board.get_moves()) == sorted(
            [((3, 3), (2, 3)), ((3, 4), (2, 4)), ((1, 0), (2, 0)), ((1, 1), (2, 1)), ((3, 3), (3, 2)), ((4, 3), (4, 2)),
             ((0, 1), (0, 2)), ((1, 1), (1, 2))])

        board = self.board.standard_board(allow_diagonals=True)
        assert sorted(board.get_moves()) == sorted(
            [((3, 3), (2, 3)), ((3, 4), (2, 4)), ((1, 0), (2, 0)), ((1, 1), (2, 1)), ((3, 3), (3, 2)), ((4, 3), (4, 2)),
             ((0, 1), (0, 2)), ((1, 1), (1, 2)), ((1, 1), (2, 0)), ((3, 3), (4, 2)), ((3, 3), (2, 2)), ((4, 3), (3, 2)),
             ((3, 4), (2, 3)), ((1, 1), (0, 2)), ((3, 3), (2, 4)), ((1, 0), (2, 1)), ((0, 1), (1, 2)),
             ((1, 1), (2, 2))])

    def test_position(self):
        board = self.board.from_array(
            board=[
                [0, 1, 1, 0, 0],
                [0, 1, 1, -1, -1],
                [1, 1, 0, -1, -1],
                [-1, 1, 0, 0, -1],
                [-1, 0, -1, -1, 0]
            ],
            current_player=-1,
            allow_diagonals=True
        )

        assert sorted(board.get_moves()) == sorted(
            [((3, 2), (2, 2)), ((4, 3), (3, 3)), ((2, 4), (1, 4)), ((0, 4), (1, 4)), ((3, 4), (4, 4)), ((3, 1), (3, 0)),
             ((4, 1), (4, 0)), ((2, 4), (2, 3)), ((3, 4), (3, 3)), ((3, 2), (3, 3)), ((4, 3), (4, 4)), ((3, 1), (4, 0)),
             ((2, 4), (3, 3)), ((4, 1), (3, 0)), ((3, 4), (2, 3)), ((3, 1), (2, 2)), ((3, 2), (2, 3)), ((4, 2), (3, 3)),
             ((0, 3), (1, 4))])

        board = self.board.from_array(
            board=[
                [0, 1, 1, 0, 0],
                [0, 1, 1, -1, -1],
                [1, 1, 0, -1, -1],
                [-1, 1, 0, 0, -1],
                [-1, 0, -1, -1, 0]
            ],
            current_player=1,
            allow_diagonals=True
        )

        print(board.get_moves())
        assert sorted(board.get_moves()) == sorted(
            [((1, 0), (0, 0)), ((1, 0), (0, 1)), ((2, 0), (3, 0)), ((1, 1), (0, 1)), ((1, 1), (2, 2)), ((1, 1), (0, 0)),
             ((2, 1), (2, 2)), ((2, 1), (3, 0)), ((0, 2), (0, 1)), ((1, 2), (2, 2)), ((1, 2), (2, 3)), ((1, 2), (0, 1)),
             ((1, 3), (2, 3)), ((1, 3), (1, 4)), ((1, 3), (2, 2))])


    def test_board_winner(self):
        board = self.board.standard_board()
        assert Board.NO_WINNER == board.winner()
        assert board.current_player == Board.PLAYER1

        board = self.board.from_array([
            [-1, 1, 1],
            [-1, 1, 0],
            [-1, 1, 1]
        ],
            Board.PLAYER1,
            allow_diagonals=False
        )
        assert Board.PLAYER1 == board.winner()

        board.current_player = Board.PLAYER2
        assert Board.PLAYER1 == board.winner()


class TestArrayBoard(BoardTestRunner):
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests)."""
        cls.board = ArrayBoard

    def test_board_neighbor_fields(self):
        board = self.board.standard_board()
        assert board._get_normal_neighbors(0, 0) == [(1, 0), (0, 1)]
        assert board._get_normal_neighbors(1, 0) == [(2, 0), (0, 0), (1, 1)]
        assert board._get_normal_neighbors(2, 3) == [(3, 3), (1, 3), (2, 4), (2, 2)]

        board = self.board.standard_board(allow_diagonals=True)
        assert board._get_all_neighbors(0, 0) == [(1, 0), (0, 1), (1, 1)]
        assert board._get_all_neighbors(2, 3) == [(3, 3), (1, 3), (2, 4), (2, 2), (3, 4), (3, 2), (1, 4), (1, 2)]

    def test_board_copy(self):
        board = ArrayBoard.standard_board()
        board_copy = board.copy()

        assert not board.move(((1, 0), (2, 0))) == ArrayBoard.INVALID_MOVE
        assert board.value(1, 0) == ArrayBoard.EMPTY
        assert board.value(2, 0) == ArrayBoard.PLAYER1
        assert board.current_player == ArrayBoard.PLAYER2

        assert board_copy.value(1, 0) == ArrayBoard.PLAYER1
        assert board_copy.value(2, 0) == ArrayBoard.EMPTY
        assert board_copy.current_player == ArrayBoard.PLAYER1

    def test_board_rotate_left(self):
        board = ArrayBoard(board=[
            [1, 0, 0, -1, 0],
            [0, 0, 1, 0, 0],
            [0, 5, 0, 0, 0],
            [0, 0, 0, 3, 0],
            [-1, 0, 0, 0, 1]
        ],
            current_player=1
        )
        left = board.rotate_left()

        assert not board.board == left.board
        assert not board.hash() == left.hash()
        assert board.current_player == left.current_player

        left = left.rotate_left()
        assert not board.hash() == left.hash()

        left = left.rotate_left()
        assert not board.hash() == left.hash()

        left = left.rotate_left()
        assert board.hash() == left.hash()

class TestBitboard(BoardTestRunner):
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests)."""
        cls.board = BitBoard


    def test_bit_scan(self):
        bitBoard = self.board.standard_board()
        assert bitBoard._bit_scan(0b1100011000000000001100011) == [(0, 0), (1, 0), (0, 1), (1, 1), (3, 3), (4, 3), (3, 4), (4, 4)]

