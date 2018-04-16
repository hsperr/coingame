from ArrayBoard import ArrayBoard

def print_board(board):
    print("Current move: {move_number}, Turn for: {current_player}".format(
        move_number = len(board.history),
        current_player = "X" if board.current_player == ArrayBoard.PLAYER1 else "O"
    ))

    for y in range(board.size_y):
        for x in range(board.size_x):
            field = board.value(x, y)
            if field == ArrayBoard.PLAYER1:
                print("X", end='')
            elif field == ArrayBoard.PLAYER2:
                print("O", end='')
            else:
                print(".", end='')

        print('')
    print('****************')
