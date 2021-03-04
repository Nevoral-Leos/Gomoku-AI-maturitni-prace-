from random import choice
from math import inf
from Web.Classes import Board, Branch, Level, Tree
import copy

def Kontrola(board, souradnice_x, souradnice_y):
    for o in range(5):
        if board[souradnice_x][souradnice_y+o] == board[souradnice_x][souradnice_y-1+o] and board[souradnice_x][souradnice_y+o] == board[souradnice_x][souradnice_y-2+o] and board[souradnice_x][souradnice_y+o] == board[souradnice_x][souradnice_y-3+o] and board[souradnice_x][souradnice_y+o] == board[souradnice_x][souradnice_y-4+o] and board[souradnice_x][souradnice_y] == board[souradnice_x][souradnice_y+o]:
            return True
        elif board[souradnice_x+o][souradnice_y] == board[souradnice_x-1+o][souradnice_y] and board[souradnice_x+o][souradnice_y] == board[souradnice_x-2+o][souradnice_y] and board[souradnice_x+o][souradnice_y] == board[souradnice_x-3+o][souradnice_y] and board[souradnice_x+o][souradnice_y] == board[souradnice_x-4+o][souradnice_y] and board[souradnice_x][souradnice_y] == board[souradnice_x+o][souradnice_y]:
            return True
        elif board[souradnice_x+o][souradnice_y-o] == board[souradnice_x-1+o][souradnice_y+1-o] and board[souradnice_x+o][souradnice_y-o] == board[souradnice_x-2+o][souradnice_y+2-o] and board[souradnice_x+o][souradnice_y-o] == board[souradnice_x-3+o][souradnice_y+3-o] and board[souradnice_x+o][souradnice_y-o] == board[souradnice_x-4+o][souradnice_y+4-o] and board[souradnice_x][souradnice_y] == board[souradnice_x+o][souradnice_y-o]:
            return True
        elif board[souradnice_x+o][souradnice_y+o] == board[souradnice_x-1+o][souradnice_y-1+o] and board[souradnice_x+o][souradnice_y+o] == board[souradnice_x-2+o][souradnice_y-2+o] and board[souradnice_x+o][souradnice_y+o] == board[souradnice_x-3+o][souradnice_y-3+o] and board[souradnice_x+o][souradnice_y+o] == board[souradnice_x-4+o][souradnice_y-4+o] and board[souradnice_x][souradnice_y] == board[souradnice_x+o][souradnice_y+o]:
            return True
    return False

def Pick_first_player():
    moznosti = [0, 1]
    player = choice(moznosti)
    if(player == 1):
        return True
    else: return False


def Create_tree(deska, hrac, score, depth, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty):
    max_moves = 4
    player = hrac
    value = score
    tree = Tree()
    Deska1 = Board(deska, value, hrac, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty)
    Větev = Branch(Deska1)
    x = 1
    for i in range(depth):
        level = Level()
        tree.add_level(level)
        if (x == 1):
            tree.get_level(tree.get_numb_level()-1).add_branch(Větev)
            cycle1_length = tree.get_level(tree.get_numb_level()-1).get_numb_branch()
        else: cycle1_length = tree.get_level(tree.get_numb_level()-2).get_numb_branch()
        pocet_board = 0
        for j in range(cycle1_length):
            if (x == 1): 
                cycle2_length = 1 
            else: cycle2_length = tree.get_level(tree.get_numb_level()-2).get_branch(j).get_len()
            for z in range(cycle2_length):
                if (x != 1 and tree.get_level(tree.get_numb_level()-2).get_branch(j).get_rozvoj(z) == 1):
                    Větev = Branch(tree.get_level(tree.get_numb_level()-2).get_branch(j).get_board_obj(z))
                    tree.get_level(tree.get_numb_level()-1).add_branch(Větev)
                elif (x != 1 and tree.get_level(tree.get_numb_level()-2).get_branch(j).get_rozvoj(z) == 0):
                    continue
                moves = []
                new_hranice_topx, new_hranice_bottomx, new_hranice_lefty, new_hranice_righty = tree.get_level(tree.get_numb_level()-1).get_branch(j).get_motherboard_borders()
                new_deska = copy.deepcopy(tree.get_level(tree.get_numb_level()-1).get_branch(j).get_motherboard_board())
                new_score = tree.get_level(tree.get_numb_level()-1).get_branch(j).get_motherboard_score()
                for o in range(new_hranice_topx, new_hranice_bottomx+1):
                    for p in range(new_hranice_lefty, new_hranice_righty+1):
                        if (new_deska[o][p] != None and new_deska[o][p] != "X" and new_deska[o][p] != "O"):
                            move = {"x": o, "y": p, "value": int(new_deska[o][p])}
                            moves.append(move)
                for k in range (len(moves)-1):
                    for l in range (len(moves)-1):
                        if (moves[l]["value"] < moves[l + 1]["value"]):
                            moves[l], moves[l + 1] = moves[l + 1], moves[l]
                for f in range (max_moves):
                    Objekt_Deska = Board(new_deska, new_score, player, new_hranice_topx, new_hranice_bottomx, new_hranice_lefty, new_hranice_righty)
                    Objekt_Deska.get_move(moves[f]["x"], moves[f]["y"])
                    if (Objekt_Deska.get_score() >= 81):
                        if (Kontrola(Objekt_Deska.get_board(), moves[f]["x"], moves[f]["y"])):
                            if(player == "X"):
                                Objekt_Deska.set_score(inf)
                            if(player == "O"):
                                Objekt_Deska.set_score(-inf)
                    if (x == 1):
                        tree.get_level(0).get_branch(0).add_board(Objekt_Deska)
                    else: tree.get_level(tree.get_numb_level()-1).get_branch(pocet_board).add_board(Objekt_Deska)
                pocet_board += 1
                x += 1
        player = "O" if player == "X" else "X"
    return tree

def Hranice_X(souradnice_x, topx, bottomx):
    if (souradnice_x > 4 and souradnice_x <= topx): 
        topx = souradnice_x - 1
    elif (souradnice_x == 4): 
        topx = souradnice_x
    if(souradnice_x < 18 and souradnice_x >= bottomx):
        bottomx = souradnice_x + 1
    elif(souradnice_x == 18):
        bottomx = souradnice_x
    return topx, bottomx

def Hranice_Y(souradnice_y, lefty, righty):
    if (souradnice_y > 4 and souradnice_y <= lefty): 
        lefty = souradnice_y - 1
    elif (souradnice_y == 4): 
        lefty = souradnice_y
    if (souradnice_y < 18 and souradnice_y >= righty):
        righty = souradnice_y + 1
    elif (souradnice_y == 18):
        righty = souradnice_y
    return lefty, righty

def AI(deska, hrac, skore, depth, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty, x, souradnice_x, souradnice_y):
    if (x == 1):
        podmínka = True
        while (podmínka):
            moznosti = [-1, 0, 1]
            value_x = choice(moznosti)
            value_y = choice(moznosti)
            if (value_x == 0 and value_y == 0):
                pass
            else:
                return souradnice_x + value_x, souradnice_y + value_y

    tree = Create_tree(deska, hrac, skore, depth, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty)
    if (depth % 2) == 0:
        hrac = "O" if hrac == "X" else "X"
    for i in range (depth):
        print ("\n")
        for j in range (tree.get_level(depth - 1 - i).get_numb_branch()):
            print (tree.get_level(depth - 1 - i).get_branch(j).get_score(0), tree.get_level(depth - 1 - i).get_branch(j).get_score(1), tree.get_level(depth - 1 - i).get_branch(j).get_score(2), tree.get_level(depth - 1 - i).get_branch(j).get_score(3))
            if (hrac == "O"):
                tree.get_level(depth - 1 - i).get_branch(j).set_motherboard_score(inf)
                for k in range (tree.get_level(depth - 1 - i).get_branch(j).get_len()):
                    if (tree.get_level(depth - 1 - i).get_branch(j).get_score(k) < tree.get_level(depth - 1 - i).get_branch(j).get_motherboard_score()):
                         tree.get_level(depth - 1 - i).get_branch(j).set_motherboard_score(tree.get_level(depth - 1 - i).get_branch(j).get_score(k))
            elif (hrac == "X"):
                tree.get_level(depth - 1 - i).get_branch(j).set_motherboard_score(-inf)
                for k in range (tree.get_level(depth - 1 - i).get_branch(j).get_len()):
                    if (tree.get_level(depth - 1 - i).get_branch(j).get_score(k) > tree.get_level(depth - 1 - i).get_branch(j).get_motherboard_score()):
                         tree.get_level(depth - 1 - i).get_branch(j).set_motherboard_score(tree.get_level(depth - 1 - i).get_branch(j).get_score(k))
        hrac = "O" if hrac == "X" else "X"
    best_move = tree.get_level(0).get_branch(0).get_board_obj(0)
    for i in range (tree.get_level(0).get_branch(0).get_len()-1):
        if hrac == "O":
            if (best_move.get_score() < tree.get_level(0).get_branch(0).get_score(i)):
                best_move = tree.get_level(0).get_branch(0).get_board_obj(i)
        if hrac == "X":
            if (best_move.get_score() > tree.get_level(0).get_branch(0).get_score(i)):
                best_move = tree.get_level(0).get_branch(0).get_board_obj(i)
    best_x, best_y = best_move.get_xy()
    return best_x, best_y

def Heuristika(deska, souradnice_x, souradnice_y):
    pocet_volnych, pocet_vrade, blocked = pocet_pozic(deska, souradnice_x, souradnice_y)
    for i in range (-1, 2):
        if (deska[souradnice_x+i][souradnice_y-1] != "X" and deska[souradnice_x+i][souradnice_y-1] != "O" ):
            if (deska[souradnice_x+i][souradnice_y-1] == None):
                deska[souradnice_x+i][souradnice_y-1] = str(pocet_volnych)
            else: deska[souradnice_x+i][souradnice_y-1] = str(int(deska[souradnice_x+i][souradnice_y-1])+pocet_volnych)
        if (deska[souradnice_x+i][souradnice_y] != "X" and deska[souradnice_x+i][souradnice_y] != "O" ):
            if (deska[souradnice_x+i][souradnice_y] == None):
                deska[souradnice_x+i][souradnice_y] = str(pocet_volnych)
            else: deska[souradnice_x+i][souradnice_y] = str(int(deska[souradnice_x+i][souradnice_y])+pocet_volnych)
        if (deska[souradnice_x+i][souradnice_y+1] != "X" and deska[souradnice_x+i][souradnice_y+1] != "O" ):
            if (deska[souradnice_x+i][souradnice_y+1] == None):
                deska[souradnice_x+i][souradnice_y+1] = str(pocet_volnych)
            else: deska[souradnice_x+i][souradnice_y+1] = str(int(deska[souradnice_x+i][souradnice_y+1])+pocet_volnych)
    length = len(pocet_vrade)
    if (length > 1):
        for x in pocet_vrade:
            for y in pocet_vrade:
                if x != y:
                    if x["vektor"] == [-1, -1] and y["vektor"] == [1, 1]:
                        x["pocet_vrade"] + y["pocet_vrade"] + 1
                        if len(x["otevreno"]) > 0 and len(y["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                        elif len(x["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        elif len(y["otevreno"]) > 0:
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        pocet_vrade.pop(pocet_vrade.index(x))
                        pocet_vrade.pop(pocet_vrade.index(y))
                        length -= 2
                     
                    if x["vektor"] == [0, -1] and y["vektor"] == [0, 1]:
                        x["pocet_vrade"] + y["pocet_vrade"] + 1
                        if len(x["otevreno"]) > 0 and len(y["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                        elif len(x["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        elif len(y["otevreno"]) > 0:
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        pocet_vrade.pop(pocet_vrade.index(x))
                        pocet_vrade.pop(pocet_vrade.index(y))
                        length -= 2
                     
                    if x["vektor"] == [-1, 0] and y["vektor"] == [1, 0]:
                        x["pocet_vrade"] + y["pocet_vrade"] + 1
                        if len(x["otevreno"]) > 0 and len(y["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                        elif len(x["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        elif len(y["otevreno"]) > 0:
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        pocet_vrade.pop(pocet_vrade.index(x))
                        pocet_vrade.pop(pocet_vrade.index(y))
                        length -= 2

                    if x["vektor"] == [1, -1] and y["vektor"] == [-1, 1]:
                        x["pocet_vrade"] + y["pocet_vrade"] + 1
                        if len(x["otevreno"]) > 0 and len(y["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                        elif len(x["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        elif len(y["otevreno"]) > 0:
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        pocet_vrade.pop(pocet_vrade.index(x))
                        pocet_vrade.pop(pocet_vrade.index(y))
                        length -= 2
    if (length != 0):
        for x in pocet_vrade:
            vec = otočit_vektor(copy.deepcopy(x["vektor"]))
            if(len(x["otevreno"]) > 0):
                if deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O":
                    deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] +1) *2)
                    deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"] +1) *2)
                else: deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] +1))
            elif deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O":
                deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"] +1))

    if (len(blocked) != 0):
        for x in blocked:
            if (deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]] != None):
                deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]] = str(int(deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]]) - 3**x["pocet_vrade"])
            else: deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]] = str(- 3**x["pocet_vrade"])
                     
def otočit_vektor(vektor):
    vektor_new = []
    vektor_new.append(vektor[0] * -1)
    vektor_new.append(vektor[1] * -1)
    return vektor_new


def pocet_pozic(deska, souradnice_x, souradnice_y):
    pocet = 0
    inline = []
    blocked = []
    for i in range (-1, 2):
        vektor = []
        if (deska[souradnice_x+i][souradnice_y-1] != "X" and deska[souradnice_x+i][souradnice_y-1] != "O" ):
            pocet += 1
        elif (deska[souradnice_x][souradnice_y] == deska[souradnice_x+i][souradnice_y-1]):
            vektor.append(i)
            vektor.append(-1)
            pocet_vrade, otevrena = how_many_more(deska, souradnice_x, souradnice_y, vektor)
            dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "otevreno": otevrena}
            inline.append(dictionary)
            vektor = []
        elif (deska[souradnice_x][souradnice_y] != deska[souradnice_x+i][souradnice_y-1]):
            vektor.append(i)
            vektor.append(-1)
            pocet_vrade, blocked_vec = how_many_blocked(deska, souradnice_x, souradnice_y, vektor)
            if (len(blocked_vec) > 0):
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "blocked": blocked_vec}
                blocked.append(dictionary)
            vektor = []
        if (deska[souradnice_x+i][souradnice_y] != "X" and deska[souradnice_x+i][souradnice_y] != "O" ):
            pocet += 1
        elif(deska[souradnice_x][souradnice_y] == deska[souradnice_x+i][souradnice_y] and i != 0):
            vektor.append(i)
            vektor.append(0)
            pocet_vrade, otevrena = how_many_more(deska, souradnice_x, souradnice_y, vektor)
            dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "otevreno": otevrena}
            inline.append(dictionary)
            vektor = []
        elif(deska[souradnice_x][souradnice_y] != deska[souradnice_x+i][souradnice_y] and i != 0):
            vektor.append(i)
            vektor.append(-1)
            pocet_vrade, blocked_vec = how_many_blocked(deska, souradnice_x, souradnice_y, vektor)
            if (len(blocked_vec) > 0):
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "blocked": blocked_vec}
                blocked.append(dictionary)
            vektor = []
        if (deska[souradnice_x+i][souradnice_y+1] != "X" and deska[souradnice_x+i][souradnice_y+1] != "O" ):
            pocet += 1
        elif(deska[souradnice_x][souradnice_y] == deska[souradnice_x+i][souradnice_y+1]):
            vektor.append(i)
            vektor.append(1)
            pocet_vrade, otevrena = how_many_more(deska, souradnice_x, souradnice_y, vektor)
            dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "otevreno": otevrena}
            inline.append(dictionary)
            vektor = []
        elif(deska[souradnice_x][souradnice_y] != deska[souradnice_x+i][souradnice_y+1]):
            vektor.append(i)
            vektor.append(-1)
            pocet_vrade, blocked_vec = how_many_blocked(deska, souradnice_x, souradnice_y, vektor)
            if (len(blocked_vec) > 0):
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "blocked": blocked_vec}
                blocked.append(dictionary)
            vektor = []
    return pocet, inline, blocked

def how_many_more(deska, souradnice_x, souradnice_y, vektor):
    more = 1
    list = []
    for i in range (2, 5):
        if (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] == deska[souradnice_x][souradnice_y]):
            more += 1
        elif (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "X" and deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "O"):
            list.append(vektor[0] * i)
            list.append(vektor[1] * i)
            return more, list
        else: return more, list
    return more, list

def how_many_blocked(deska, souradnice_x, souradnice_y, vektor):
    more = 1
    list = []
    for i in range (2, 5):
        if (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] == deska[souradnice_x + vektor[0]][souradnice_y + vektor[1]]):
            more += 1
        elif (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "X" and deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "O"):
            list.append(vektor[0] * i)
            list.append(vektor[1] * i)
            return more, list
        else: return more, list
    return more, list

