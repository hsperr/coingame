from collections import defaultdict
import multiprocessing

import numpy as np
import time

from ArrayBoard import ArrayBoard

def find_best_move(board):
    wins = defaultdict(int)
    plays = defaultdict(int)

    for (p_wins, p_plays) in pool.map(run,[board]*10):
        for k, v in p_wins.items():
            wins[k]+=v

        for k, v in p_plays.items():
            plays[k]+=v

    moves = board.get_moves()

    log_total = np.log(sum(plays.values()))
    best_move, best_score = None, 0

    for move in moves:
        key = (move, board.current_player, board.hash())
        if not key in plays:
            continue

        winrate = wins[key]/plays[key]
        score = winrate + 1.0 * np.sqrt(log_total/plays[key])
        if score > best_score:
            best_move = move
            best_score = score

        print(move, plays[key], wins[key], winrate, score)

    print("Best move", best_move)
    return best_score, best_move

def fully_expanded(moves, plays, board):
  return all((move, board.current_player, board.hash()) in plays for move in moves)

def best_uct(moves, wins, plays, board): 
    log_total = np.log(sum(plays.values()))

    weighted_moves = []
    for move in moves:
        positions_won = wins[(move, board.current_player, board.hash())]
        times_played = plays[(move, board.current_player, board.hash())]

        score = positions_won/times_played + 1.4 * np.sqrt(log_total/times_played)

        weighted_moves.append((score, move))

    return max(weighted_moves)

def run(board):
    original_board = board.copy()
    plays = defaultdict(int)
    wins = defaultdict(int)

    simul_moves = []

    t0 = time.time()
    print(int(t0*100000)% 4294967000)
    np.random.seed(int(t0*100000)% 4294967000)

    for i in range(501):
        if i and i%500==0:
            print(i, sum(simul_moves), np.mean(simul_moves), time.time()-t0)

        visited_states = set()
        board = original_board.copy()

        while True:
            moves = board.get_moves()
            if not moves: 
                break

            if fully_expanded(moves, plays, board):
                score, move = best_uct(moves, wins, plays, board)
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
        
        num_moves, winner = _simulate(board.move(move))
        #print("Winner for {} is {}".format(move, winner))
        simul_moves.append(num_moves)

        #backpropagation
        for move, player, state in visited_states:
            plays[(move, player, state)] += 1
            if player == winner:
                wins[(move, player, state)] += 1

    print("Monte Carlo Stats, num_positions: {}, num_plays: {}".format(len(plays), sum(plays.values())))
    return wins, plays

def _simulate(board):
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

pool = multiprocessing.Pool(10)
if __name__ == '__main__':
    board = ArrayBoard()
    find_best_move(board)


