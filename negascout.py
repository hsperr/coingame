from display import print_board
import random
import time

class NegaScout():

    def __init__(self, max_depth=6, use_deepening=True, use_table=True, use_move_ordering=False, use_principal_variation=False):
        self.moves_looked_at = 0
        self.exact_hits = 0
        self.beta_hits = 0
        self.pv_searches = 0
        self.pv_searches_beta = 0

        self.transposition_table = {}
        self.max_depth = max_depth
        self.use_table = use_table
        self.use_deepening = use_deepening
        self.use_move_ordering = use_move_ordering
        self.use_principal_variation = use_principal_variation

        print("""
        Initializing Negascout:
        Max Depth: {max_depth}
        Use HashTable: {use_table}
        Use Iterative Deepening: {use_deepening}
        Use Move Ordering: {use_move_ordering}
        Use Principal Variation: {use_principal_variation}
        """.format(max_depth=max_depth, use_table=use_table, use_deepening=use_deepening, use_move_ordering=use_move_ordering, use_principal_variation=use_principal_variation))



    def find_best_move(self, board):
        self.transposition_table = {}
        board = board.copy()

        self.moves_looked_at = 0

        if self.use_deepening:
            t0 = time.time()
            print("Start Iterative Deepening")
            for i in range(2, self.max_depth+1, 2):
                self.moves_looked_at = 0
                self.exact_hits = 0
                self.beta_hits = 0
                self.pv_searches = 0
                score, move = self._negascout(board, i, -1000000, 1000000)
                print(i, score, move, self.moves_looked_at, self.exact_hits, self.beta_hits, self.pv_searches, self.pv_searches_beta, len(self.transposition_table), time.time()-t0)

            return score, move
        else:
            return self._negascout(board, self.max_depth, -1000000, 1000000)


    @staticmethod
    def _current_player_score(board):
        return board.get_num_occupied_fields(board.current_player)-board.get_num_occupied_fields(board.other_player)

    @staticmethod
    def _current_player_score_moves(board):
        return NegaScout._current_player_score(board) + len(board._get_moves_for(board.current_player)) - len(board._get_moves_for(board.other_player))

    def _negascout(self, board, depth, alpha, beta):
        self.moves_looked_at += 1
        if depth == 0:
            return NegaScout._current_player_score(board), None

        if self.use_move_ordering:
            moves = [x[1] for x in sorted(board.get_moves_weighted_by_enemies(), key=lambda x: -x[0])]
        else:
            moves = board.get_moves()
            random.shuffle(moves)

        #only one move so we exit early
        if len(moves) == 1:
            return 0, moves[0]

        if not moves:
            if board._is_draw():
                return 0, None
            else:
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

            if record_type == 'exact' and h_best_move and depth <= h_depth:
                #print(depth, 'exact', alpha, h_best_move)
                self.exact_hits += 1
                return h_alpha, h_best_move
            if record_type == 'beta' and h_beta > beta and depth <= h_depth:
                #print(depth, 'beta', h_best_move)
                self.beta_hits += 1
                return h_beta, h_best_move

            if record_type == 'exact' and h_best_move and self.use_principal_variation:
                #print(depth, 'pv_search', h_best_move)
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

            #print_board(board)
            #board._pretty_print(board.player1)
            #board._pretty_print(board.player2)
            #print(depth, move, alpha, beta)
            if self.use_principal_variation and used_move:
                score, _ = self._negascout(board.move(move), depth-1, -alpha-1, -alpha)
                if alpha < score < beta:
                    score, _ = self._negascout(board, depth-1, -beta, -score)
            else:
                score, _ = self._negascout(board.move(move), depth-1, -beta, -alpha)

            score *= -1
            board.undo()
            #print(depth, move, alpha, beta, score)

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

        if alpha == 1000000:
            print_board(board)
            print('depth', 'exact_save', alpha, beta, best_move)
            asd

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

def self_play():
    board = BitBoard.standard_board()
    search1 = NegaScout(8, use_deepening=True, use_table=True)
    search2 = NegaScout(8, use_deepening=True, use_table=True)
    moves = board.get_moves()

    while moves:
        if board.current_player == BitBoard.PLAYER1:
            score, move = search1.find_best_move(board)
        else:
            score, move = search2.find_best_move(board)

        print(move, score)
        print("Moves looked at:", search2.moves_looked_at, search2.exact_hits, search2.pv_searches)

        board.move(move)
        print_board(board)
        moves = board.get_moves()

if __name__ == '__main__':
    from ArrayBoard import ArrayBoard
    from BitBoard import BitBoard

    #board._pretty_print(board.player1)
    #board._pretty_print(board.player2)
    board = BitBoard.from_string(
        '''
        XX.OO
        OO.XX
        O...X
        OOX.X
        .O..X
       ''', 'X', allow_diagonals=True)
    print_board(board)
    print(board.get_moves())
    search = NegaScout(8, use_deepening=True, use_table=True)
    print(search.find_best_move(board))
    search = NegaScout(10, use_deepening=True, use_table=True, use_move_ordering=True)
    print(search.find_best_move(board))
    search = NegaScout(8, use_deepening=True, use_table=True, use_move_ordering=True, use_principal_variation=True)
    print(search.find_best_move(board))
    #print(board.move(((2, 3), (1, 2))))
    print_board(board)
