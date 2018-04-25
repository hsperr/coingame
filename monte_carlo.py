from collections import defaultdict
import time

import numpy as np

from ArrayBoard import ArrayBoard

class MonteCarloTreeSearch():

    def fully_expanded(self, moves, plays, board):
      return all((move, board.current_player, board.hash()) in plays for move in moves)

    def best_uct(self, moves, wins, plays, board): 
        log_total = np.log(sum(plays.values()))

        weighted_moves = []
        for move in moves:
            positions_won = wins[(move, board.current_player, board.hash())]
            times_played = plays[(move, board.current_player, board.hash())]

            score = positions_won/times_played + 1.4 * np.sqrt(log_total/times_played)

            weighted_moves.append((score, move))

        return max(weighted_moves)
    
    def find_best_move(self, board):
        original_board = board.copy()
        plays = defaultdict(int)
        wins = defaultdict(int)

        simul_moves = []

        t0 = time.time()
        max_depth = 0

        for i in range(20001):
            if i and i%5000==0:
                print(i, sum(simul_moves), np.mean(simul_moves), time.time()-t0, max_depth)

            visited_states = set()
            board = original_board.copy()
            depth = 0

            while True:
                moves = board.get_moves()
                if not moves: 
                    break

                if self.fully_expanded(moves, plays, board):
                    score, move = self.best_uct(moves, wins, plays, board)
                    #print("UTC move {}, score {}".format(move, score))
                    visited_states.add((move, board.current_player, board.hash()))
                    depth += 1
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
                        depth += 1
            
            if moves:
                depth += 1
                num_moves, winner = self._simulate(board.move(move), rollout=False)
                depth+=num_moves
                #print("Winner for {} is {}".format(move, winner))
                simul_moves.append(num_moves)
            else:
                winner = board.winner()

            if depth > max_depth:
                max_depth = depth
    
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
            #print(move, plays[key], score)

        print("Monte Carlo Stats, num_positions: {}, num_plays: {}, max_depth {}".format(len(plays), sum(plays.values()), max_depth))
        self.moves_looked_at = sum(plays.values())
        return best_score, best_move

    def _simulate(self, board, rollout=True):
        if rollout:
            board = board.copy()
            num_moves = 0
            while True:
                #moves = board.get_moves()
                moves = board.get_moves_weighted_by_enemies()
                if not moves:
                    return num_moves, board.winner()

                total_score = sum(x[0]*50+1 for x in moves)
                score, move = moves[np.random.choice(len(moves), p=[(x[0]*50+1)/total_score for x in moves])]
                #move = moves[np.random.choice(len(moves))]
                num_moves+=1
                board.move(move)
        else:
            score = board.get_num_occupied_fields(board.current_player) - board.get_num_occupied_fields(board.other_player)
            return 0, board.current_player if score > 0 else board.other_player


if __name__ == '__main__':
    board = ArrayBoard()
    search = MonteCarloTreeSearch()
    while True:
        move = search.find_best_move(board)
        board.move(move)
        print_board(board)
