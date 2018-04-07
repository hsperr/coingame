import copy

diagonals_allowed = True


class Tile():
    def __init__(self, field, x, y):
         self.field, self.x, self.y = field, x, y

    def valid(self):
        if 0 <= self.x < len(self.field[0]) and 0 <= self.y < len(self.field):
            return True
        return False

    def up(self):
        return Tile(self.field, self.x, self.y-1)
    def down(self):
        return Tile(self.field, self.x, self.y+1)
    def left(self):
        return Tile(self.field, self.x-1, self.y)
    def right(self):
        return Tile(self.field, self.x+1, self.y)

    def isplayer(self, player=None):
        if self.valid():
            if player:
                return self.field[self.y][self.x] == player

            return not self.field[self.y][self.x] == 0
        return False

    def content(self):
        if self.valid():
            return self.field[self.y][self.x]
        return 'invalid'

    def position(self):
        return (self.x, self.y)

    

class Playfield():
    def init_playfield(self):
        return [
            [ 1 ,1, 0,-1,-1],
            [ 1, 1, 0,-1,-1],
            [ 0, 0, 0, 0, 0],
            [-1,-1, 0, 1, 1],
            [-1,-1, 0, 1, 1]
        ]

    def __init__(self):
        self.playfield = self.init_playfield()
        self.history = []
        self.current_player = 1

    def copy(self):
        new_field = Playfield()
        new_field.playfield = copy.deepcopy(self.playfield)
        new_field.history =  copy.deepcopy(self.history)
        new_field.current_player = self.current_player
        return new_field

    def hash(self):
        return hash(str(self.playfield)+str(self.current_player))

    def num_moves(self):
        return len(self.history)

    def above(self, x, y):
        return (max(0, y-1), x)

    def below(self, x, y):
        return (min(len(self.playfield)-1, y+1), x)

    def left(self, x, y):
        return (y, max(0, x-1))

    def right(self, x, y):
        row = self.playfield[0]
        return (y, min(len(row)-1, x+1))

    def player_at_location(self, location):
        (x, y) = location
        return self.player_at_coordinate(x,y)

    def player_at_coordinate(self, x, y):
        return self.playfield[y][x]

    def get_moves(self):
        playfield = self.playfield
        player = self.current_player

        moves = []
        for y, row in enumerate(playfield):
            for x, field in enumerate(row):
                if not field == 0:
                    continue

                tile = Tile(self.playfield, x, y)
                for direction in (tile.up(), tile.down(), tile.left(), tile.right()):
                    if direction.valid() and direction.content() == player:
                        moves.append((direction.position(), (x,y)))

                if not diagonals_allowed:
                    continue

                for direction in (tile.up().left(), tile.up().right(), tile.down().left(), tile.down().right()):
                    if direction.valid() and direction.content() == player:
                        moves.append((direction.position(), (x,y)))
        return moves


    def undo_move(self):
        if not len(self.history):
            return

        _, self.playfield, self.current_player = self.history[-1]
        self.history = self.history[:-1]

    def make_move(self, move):
        self.playfield = self._make_move(move)

        if self.current_player < 0:
            self.current_player = 1
        else:
            self.current_player = -1

        return self

    def _make_move(self, move):
        (from_x, from_y), (to_x, to_y) = move
        new_playfield = copy.deepcopy(self.playfield)

        #self.history.append((move, self.playfield, self.current_player))
        new_playfield[from_y][from_x], new_playfield[to_y][to_x] = 0, new_playfield[from_y][from_x]

        changed = []

        if self.current_player < 0:
            other_player = 1
        else:
            other_player = -1

        tile = Tile(new_playfield, to_x, to_y)
        direction = tile.up()
        if direction.valid() and direction.isplayer(other_player):
                new_playfield[direction.y][direction.x] = self.current_player
                changed.append('up')
        
        direction = tile.left()
        if direction.valid() and direction.isplayer(other_player):
                new_playfield[direction.y][direction.x] = self.current_player
                changed.append('left')

        direction = tile.right()
        if direction.valid() and direction.isplayer(other_player):
                new_playfield[direction.y][direction.x] = self.current_player
                changed.append('right')

        direction = tile.down()
        if direction.valid() and direction.isplayer(other_player):
                new_playfield[direction.y][direction.x] = self.current_player
                changed.append('down')

        direction = tile.up().left()
        if 'up' in changed and 'left' in changed and direction.isplayer():
                new_playfield[direction.y][direction.x] = self.current_player

        direction = tile.up().right()
        if 'up' in changed and 'right' in changed and direction.isplayer():
                new_playfield[direction.y][direction.x] = self.current_player

        direction = tile.down().right()
        if 'down' in changed and 'right' in changed and direction.isplayer():
                new_playfield[direction.y][direction.x] = self.current_player

        direction = tile.down().left()
        if 'down' in changed and 'left' in changed and direction.isplayer():
                new_playfield[direction.y][direction.x] = self.current_player

        return new_playfield

    def score(self):
        return sum(sum(row) for row in self.playfield)

    def print_playfield(self):
        print("Current field (move: {}, player: {}):".format(len(self.history), self.current_player))
        print("Moves: {}".format(["{} -> {}".format(x[0][0], x[0][1]) for x in self.history]))
        for row in self.playfield:
            for field in row:
                if not field:
                    print(".", end='')
                elif field == -1:
                    print("X", end='')
                else:
                    print("O", end='')
            print('')
        print("*********")

from collections import defaultdict
import random


def search(playfield, depth, alpha, beta, positions, hashtable):
    if depth == 0:
        positions[0] += 1
        return playfield.current_player*playfield.score(), None

    moves = playfield.get_moves()
    if not moves:
        positions[0] += 1
        return playfield.current_player*100000, None

    #print(depth, len(moves))
    #if depth == 1:
    #    playfield.print_playfield()

    best_move = None


    playfield_hash = playfield.hash()

    for move in moves:
        score, _ = search(playfield.make_move(move), depth-1, -beta, -alpha, positions, hashtable)
        score *= -1
        playfield.undo_move()
        #print(depth, move, score)

        #print(depth, move, alpha, beta, score)
        if score>alpha:
            best_move = move
            alpha = score

        if alpha >= beta:
            break

    hashtable[playfield_hash] = (depth, alpha, best_move, copy.deepcopy(playfield.playfield), playfield.current_player)
    #print(depth, alpha, beta, score)
    return alpha, best_move

import numpy as np
def monte_carlo(playfield):
    moves2score = defaultdict(lambda: defaultdict(int))
    boardmove2score = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for i in range(10000):
        try:
            if i and i%100==0:
                print(i)
            current_move = None
            monte_carlo_field = playfield.copy()
            localboardmove2score = defaultdict(lambda: defaultdict(int))
            while True:
                moves = monte_carlo_field.get_moves()
                if not moves:
                    break

                w = [max(1,boardmove2score[monte_carlo_field.hash()][m][monte_carlo_field.current_player]) for m in moves]
                w = [x/sum(w) for x in w]
                move = np.random.choice(len(moves), p=w)
                move = moves[move]

                localboardmove2score[monte_carlo_field.hash()][move] += 1

                if not current_move:
                    current_move = move

                monte_carlo_field.make_move(move)
            
            for board, m in localboardmove2score.items():
                for move, score in m.items():
                    boardmove2score[board][move][monte_carlo_field.current_player] += 1

            moves2score[current_move][monte_carlo_field.current_player]+=1
        except:
            break
    return moves2score

def perf():
    moves_taken = 0
    for i in range(10):
        hashtable = defaultdict(int)
        playfield = Playfield()

        while True:
            moves = playfield.get_moves()
            if not len(moves):
                playfield.print_playfield()
                print("Player {} has no moves".format(playfield.current_player))
                break
            
            move = random.choice(moves)
            playfield.make_move(move)

            hashtable[hash(str(playfield.playfield))] +=1
            if hashtable[hash(str(playfield.playfield))] > 5:
                print("Its a tie")
                break
            
        moves_taken += playfield.num_moves()
    print(moves_taken/10)

#perf()
def main():
    print("Searching")
    playfield = Playfield()
    while True:
        hashtable = {}
        playfield.print_playfield()
        for depth in range(2, 12, 2):
            positions = [0]
            score, move = search(playfield, depth, -1000000, 1000000, positions, hashtable)

            print("Search score:", score, move) 
            print("Positions searched: {}".format(positions))
        break

        playfield.make_move(move)
        playfield.print_playfield()

playfield = Playfield()


for move, data in monte_carlo(playfield).items():
    print(move, data[1], data[-1], data[1]/(data[1]+data[-1]))
