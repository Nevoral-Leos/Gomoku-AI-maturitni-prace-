import copy

class Game():
    def __init__(self):
        self.player = "X"
        self.score = 0
        self.hranice_topx = 19
        self.hranice_bottomx = 4
        self.hranice_lefty = 19
        self.hranice_righty = 4
        self.win = False
        self.pocet_tahu = 0

    def get_pocet_tahu(self):
        return self.pocet_tahu

    def reset(self):
        self.player = "X"
        self.score = 0
        self.hranice_topx = 19
        self.hranice_bottomx = 4
        self.hranice_lefty = 19
        self.hranice_righty = 4
        self.win = False
        self.pocet_tahu = 0

    def nove_hranice(self, last_x, last_y):
        if (last_x > 4 and last_x <= self.hranice_topx): 
            self.hranice_topx = last_x - 1
        elif (last_x == 4):
            self.hranice_topx = last_x
        if (last_x < 18 and last_x >= self.hranice_bottomx): 
            self.hranice_bottomx = last_x + 1
        elif (last_x == 18):
            self.hranice_bottomx = last_x
        if (last_y > 4 and last_y <= self.hranice_lefty): 
            self.hranice_lefty = last_y - 1
        elif (last_y == 4): 
            self.hranice_lefty = last_y
        if (last_y < 18 and last_y >= self.hranice_righty): 
            self.hranice_righty = last_y + 1
        elif (last_y == 18): 
            self.hranice_righty = last_y

    def get_hranice(self):
        return self.hranice_topx, self.hranice_bottomx, self.hranice_lefty, self.hranice_righty

    def get_player(self):
        return self.player

    def change_player(self):
        self.player = "O" if self.player == "X" else "X"
        self.pocet_tahu += 1

    def get_board(self):
        return self.board

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def set_win(self):
        self.win = True

    def get_win(self):
        return self.win

class Board():
    def __init__(self, board, score, player, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty):
        self.board = copy.deepcopy(board)
        self.score = score
        self.player = player
        self.hranice_topx = hranice_topx
        self.hranice_bottomx = hranice_bottomx
        self.hranice_lefty = hranice_lefty
        self.hranice_righty = hranice_righty
        self.tahx = 0
        self.tahy = 0
        self.rozvoj = 1

    def get_board_borders(self):
        return self.hranice_topx, self.hranice_bottomx, self.hranice_lefty, self.hranice_righty
    
    def get_board(self):
        return self.board

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_player(self):
        return self.player

    def get_rozvoj(self):
        return self.rozvoj

    def get_xy(self):
        return self.tahx, self.tahy

    def get_move(self, i, j):
        if self.board[i][j] != "X" or self.board[i][j] != "O":
            if (self.player == "O"):
                self.score -= int(self.board[i][j])
            else: 
                self.score += int(self.board[i][j])
            self.board[i][j] = self.player
            Heuristika(self.board, i, j)
            self.tahx = i
            self.tahy = j
            self.hranice_topx, self.hranice_bottomx = Hranice_X(i, self.hranice_topx, self.hranice_bottomx)
            self.hranice_lefty, self.hranice_righty = Hranice_Y(j, self.hranice_lefty, self.hranice_righty)

class Branch():
    def __init__(self, motherboard):
        self.results = []
        self.motherboard = motherboard

    def add_board(self, objekt):
        self.results.append(objekt)

    def delete_board(self, i):
        self.results.pop(i)

    def get_len(self):
        return len(self.results)

    def get_board_obj(self, i):
        return self.results[i]

    def get_board(self, i):      
        return self.results[i].get_board()

    def get_board_borders(self):
        return self.motherboard.get_board_borders()

    def get_score(self, i):
        return self.results[i].get_score()

    def get_rozvoj(self, i):
         return self.results[i].get_rozvoj()

    def get_motherboard_board(self):
        return self.motherboard.get_board()

    def get_motherboard_borders(self):
        return self.motherboard.get_board_borders()

    def get_motherboard_score(self):
        return self.motherboard.get_score()

    def set_motherboard_score(self, score):
        self.motherboard.set_score(score)

class Level():
    def __init__(self):
        self.branches = []

    def get_numb_branch(self):
        return len(self.branches)

    def add_branch(self, Branch):
        self.branches.append(Branch)
    
    def delete_branch(self, i):
        self.branches.pop(i)
    
    def get_branch(self, i):
        return self.branches[i]

class Tree():
    def __init__(self):
        self.tree = []
    
    def get_numb_level(self):
        return len(self.tree)

    def add_level(self, Level):
        self.tree.append(Level)
    
    def delete_level(self, i):
        self.tree.pop(i)
    
    def get_level(self, i):
        return self.tree[i]

from Web.Mechaniky import *
