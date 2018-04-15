from collections import defaultdict
import multiprocessing

import numpy as np

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
    return best_move


def run(board):
    plays = defaultdict(int)
    wins = defaultdict(int)

    original_board = board.copy()

    for i in range(100):
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
        
        winner = _simulate(board.move(move))
        #print("Winner for {} is {}".format(move, winner))

        #backpropagation
        for move, player, state in visited_states:
            plays[(move, player, state)] += 1
            if player == winner:
                wins[(move, player, state)] += 1


    return wins, plays


def _simulate(board):
    board = board.copy()
    while True:
        moves = board.get_moves()
        if not moves:
            return board.winner()

        move = moves[np.random.choice(len(moves))]
        board.move(move)



pool = multiprocessing.Pool(10)
if __name__ == '__main__':
    board = ArrayBoard()
    find_best_move(board)


