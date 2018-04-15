from ArrayBoard import ArrayBoard, print_board

from monte_carlo import MonteCarloTreeSearch
from negascout import NegaScout


board = ArrayBoard(allow_diagonals=True)
#board.current_player = -1
#board.board = [
#       [ 0, 1, 1, 0, 0],
#       [ 0, 1, 1,-1,-1],
#       [ 1, 1, 0,-1,-1],
#       [-1, 1, 0, 0,-1],
#       [-1, 0,-1,-1, 0],
#]
print_board(board)
search = MonteCarloTreeSearch()
search2 = NegaScout()

while True:
    if board.current_player == ArrayBoard.PLAYER1:
        score, move = search2.find_best_move(board)
        print("Negascout score: {}, moves_searched: {}".format(score, search2.moves_looked_at))
    else:
        score, move = search2.find_best_move(board)
        print("Negascout score: {}, moves_searched: {}".format(score, search2.moves_looked_at))

    board.move(move)
    print_board(board)
