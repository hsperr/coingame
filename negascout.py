from board import Board

class NegaScout():

    def find_best_move(self, board):
        board = board.copy()
        self.moves_looked_at = 0

        return self._negascout(board, 6, -1000000, 100000)

    def _negascout(self, board, depth, alpha, beta):
        if depth == 0:
            #print(depth, board.current_player_score(), None)
            self.moves_looked_at += 1
            return board.current_player_score(), None

        moves = board.get_moves()
        if not moves:
            #print(depth, -999999, None)
            self.moves_looked_at += 1
            return -9999999, None
        
        best_move = None
        #print(depth, len(moves))
        for move in moves:
            #print(depth, move, alpha, beta)
            score, _ = self._negascout(board.move(move), depth-1, -beta, -alpha)
            score *= -1
            board.undo()

            #print(depth, move, score, alpha, beta)
            #print("*****")

            if score >= beta:
                return beta, move
            
            if score > alpha:
                alpha, best_move = score, move

        #print(depth, 'best', alpha, best_move)
        return alpha, best_move


if __name__ == '__main__':
    board = Board()
    search = NegaScout()

    print(search.find_best_move(board))
    print("Moves looked at:", search.moves_looked_at)

