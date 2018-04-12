from board import Board
from display import print_board


class NegaScout():

    def __init__(self, max_depth=6, use_deepening=False, use_table=False):
        self.moves_looked_at = 0
        self.exact_hits = 0
        self.beta_hits = 0
        self.pv_searches = 0
        self.pv_searches_beta = 0

        self.transposition_table = {}
        self.max_depth = max_depth
        self.use_table = use_table
        self.use_deepening = use_deepening

    def find_best_move(self, board):
        board = board.copy()

        self.moves_looked_at = 0

        if self.use_deepening:
            for i in range(2, self.max_depth+1, 2):
                self.moves_looked_at = 0
                self.exact_hits = 0
                self.beta_hits = 0
                self.pv_searches = 0
                score, move = self._negascout(board, i, -1000000, 100000)
                print(i, score, move, self.moves_looked_at, self.exact_hits, self.beta_hits, self.pv_searches, self.pv_searches_beta)
            return score, move
        else:
            return self._negascout(board, self.max_depth, -1000000, 100000)

    def _negascout(self, board, depth, alpha, beta):
        self.moves_looked_at += 1
        if depth == 0:
            return board.current_player_score(), None

        moves = board.get_moves()
        if not moves:
            return -9999999, None
        
        best_move = None

        used_move = None
        if self.use_table and board.hash() in self.transposition_table:
            record_type, h_board, h_depth, h_alpha, h_beta, h_best_move = self.transposition_table[board.hash()]
            if not h_board == board.board:
                print("collision", board.hash())
                print(board.board)
                print(h_board)
                print("*********")

            #print(depth, alpha, beta, record_type, h_depth, h_alpha, h_beta, h_best_move)
            if record_type == 'exact' and h_best_move and depth <= h_depth:
                self.exact_hits += 1
                return alpha, best_move
            if record_type == 'beta' and h_beta > beta and depth <= h_depth:
                self.beta_hits += 1
                return beta, best_move

            if record_type == 'exact' and h_best_move:
                used_move = h_best_move
                self.pv_searches += 1
                score, _ = self._negascout(board.move(h_best_move), depth-1, -beta, -alpha)
                score *= -1
                board.undo()

                if score >= beta:
                    self.pv_searches_beta += 1
                    return beta, h_best_move

                if score > alpha:
                    alpha, best_move = score, h_best_move
                #print("inside", depth, alpha, beta, score, record_type, h_depth, h_alpha, h_beta, h_best_move)

        for move in moves:
            if used_move == move:
                continue

            score, _ = self._negascout(board.move(move), depth-1, -beta, -alpha)
            score *= -1
            board.undo()

            if score >= beta:
                self.transposition_table[board.hash()] = (
                    'beta',
                    board.board,
                    depth,
                    alpha,
                    beta,
                    best_move
                )
                return beta, move
            
            if score > alpha:
                alpha, best_move = score, move

        hash_entry = (
            'exact',
            board.board,
            depth,
            alpha,
            beta,
            best_move
        )

        self.transposition_table[board.hash()] = hash_entry
        #self.transposition_table[board.rotate_left().hash()] = hash_entry
        #self.transposition_table[board.rotate_left().rotate_left().hash()] = hash_entry
        #self.transposition_table[board.rotate_left().rotate_left().rotate_left().hash()] = hash_entry

        return alpha, best_move


if __name__ == '__main__':
    board = Board()
    board.board = [
        [ 0, 1, 1, 0, 0],
        [ 0, 1, 1,-1,-1],
        [ 1, 1, 0,-1,-1],
        [-1, 1, 0, 0,-1],
        [-1, 0,-1,-1, 0]
    ]
    board.current_player = -1

    search = NegaScout(6, use_deepening=False, use_table=False)
    print(search.find_best_move(board))
    print("Moves looked at:", search.moves_looked_at)

    search1 = NegaScout(6, use_deepening=False, use_table=True)
    print(search1.find_best_move(board))
    print("Moves looked at:", search1.moves_looked_at, search1.exact_hits, search1.pv_searches)

    search2 = NegaScout(10, use_deepening=True, use_table=True)
    print(search2.find_best_move(board))
    print("Moves looked at:", search2.moves_looked_at, search2.exact_hits, search2.pv_searches)

