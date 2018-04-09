from board import Board

def print_board(board):
    print("Current move: {}, Turn for: {}".format(len(board.history), "X" if board.current_player==Board.PLAYER1 else "O"))
    for row in board.board:
        for field in row:
            if field == Board.PLAYER1:
                print("X", end='')
            elif field == Board.PLAYER2:
                print("O", end='')
            else:
                print(".", end='')
        print('')
    print('****************')


