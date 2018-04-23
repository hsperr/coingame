from ArrayBoard import Board, ArrayBoard
from BitBoard import BitBoard

from monte_carlo import MonteCarloTreeSearch
from monte_carlo_parallel import find_best_move
from negascout import NegaScout

from display import print_board


board = BitBoard.standard_board()
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
search2 = NegaScout(max_depth=8)

while True:
    if board.current_player == Board.PLAYER1:
        score, move = find_best_move(board)
        print("MCMC score: {}, moves_searched: {}".format(score, search2.moves_looked_at))
    else:
        score, move = search2.find_best_move(board)
        print("Negascout score: {}, moves_searched: {}".format(score, search2.moves_looked_at))

    board.move(move)
    print_board(board)
