from collections import defaultdict

import numpy as np

from ArrayBoard import ArrayBoard

class MonteCarloTreeSearch():
    
    def find_best_move(self, board):
        original_board = board.copy()
        plays = defaultdict(int)
        wins = defaultdict(int)

        for i in range(50):
            if i and i%100==0:
                print(i)

            visited_states = set()
            board = original_board.copy()

            while True:
                moves = board.get_moves()
                if all((move, board.current_player, board.hash()) in plays for move in moves):
    
                    log_total = np.log(sum(plays.values()))
                    score, move  = max((
                        wins[(move, board.current_player, board.hash())]/plays[(move, board.current_player, board.hash())] 
                        + 1.4 * np.sqrt(log_total/plays[(move, board.current_player, board.hash())]), move
                    ) for move in moves)
                    #print("UTC move {}, score {}".format(move, score))

                    visited_states.add((move, board.current_player, board.hash()))
                    board.move(move)
                else:
                    move = moves[np.random.choice(len(moves))]
                    if not (move, board.current_player, board.hash()) in plays:
                        #print("Unknown node {}, expanding".format(move))
                        visited_states.add((move, board.current_player, board.hash()))
                        break
                    else:
                        #print("Known node {}".format(move))
                        visited_states.add((move, board.current_player, board.hash()))
                        board.move(move)
            
            winner = self._simulate(board.move(move))
            #print("Winner for {} is {}".format(move, winner))
    
            #backpropagation
            for move, player, state in visited_states:
                plays[(move, player, state)] += 1
                if player == winner:
                    wins[(move, player, state)] += 1

        moves = original_board.get_moves()
        best_move = None
        best_score = 0
        for move in moves:
            key = (move, original_board.current_player, original_board.hash())
            if not key in plays:
                continue
            score = wins[key]/plays[key]
            if score > best_score:
                best_move = move
                best_score = score
            print(move, plays[key], score)

        return best_move

    def _simulate(self, board):
        board = board.copy()
        while True:
            moves = board.get_moves()
            if not moves:
                return board.winner()

            move = moves[np.random.choice(len(moves))]
            board.move(move)

if __name__ == '__main__':
    board = ArrayBoard()
    search = MonteCarloTreeSearch()
    while True:
        move = search.find_best_move(board)
        board.move(move)
        print_board(board)
