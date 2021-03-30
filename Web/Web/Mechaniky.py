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


def Create_tree(deska, hrac, score, depth, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty):
    max_moves = 5
    player = hrac
    value = score
    tree = Tree()
    Deska1 = Board(deska, value, hrac, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty)
    Vetev = Branch(Deska1)
    x = 1
    for level_id in range(depth):
        level = Level()
        tree.add_level(level)
        if (x == 1):
            tree.get_level(level_id).add_branch(Vetev)
            cycle1_length = tree.get_smth(level_id, 0, 0, "branch_count")
        else: cycle1_length = tree.get_smth(level_id - 1, 0, 0, "branch_count")
        pocet_branch = 0
        for branch_id in range(cycle1_length):
            if (x == 1): 
                cycle2_length = 1 
            else: cycle2_length = tree.get_smth(level_id - 1, branch_id, 0, "element_count")
            for element_id in range(cycle2_length):
                if (x != 1 and tree.get_smth(level_id - 1, branch_id, element_id, "rozvoj") == 1):
                    Větev = Branch(tree.get_smth(level_id - 1, branch_id, element_id, "board_obj"))
                    tree.get_level(level_id).add_branch(Větev)
                elif (x != 1 and tree.get_smth(level_id - 1, branch_id, element_id, "rozvoj") == 0):
                    continue
                moves = []
                new_hranice_topx, new_hranice_bottomx, new_hranice_lefty, new_hranice_righty = tree.get_smth(level_id, branch_id, 0, "motherboard_borders")
                new_deska = copy.deepcopy(tree.get_smth(level_id, branch_id, 0, "motherboard_board"))
                new_score = tree.get_smth(level_id, branch_id, 0, "motherboard_score")
                for x in range(new_hranice_topx, new_hranice_bottomx+1):
                    for y in range(new_hranice_lefty, new_hranice_righty+1):
                        if (new_deska[x][y] != None and new_deska[x][y] != "X" and new_deska[x][y] != "O"):
                            move = {"x": x, "y": y, "value": int(new_deska[x][y])}
                            moves.append(move)
                for k in range (len(moves)-1):
                    for l in range (len(moves)-1):
                        if (moves[l]["value"] < moves[l + 1]["value"]):
                            moves[l], moves[l + 1] = moves[l + 1], moves[l]
                for f in range (max_moves):
                    Objekt_Deska = Board(new_deska, new_score, player, new_hranice_topx, new_hranice_bottomx, new_hranice_lefty, new_hranice_righty)
                    if int(new_deska[moves[f]["x"]][moves[f]["y"]]) >= 81:
                        Objekt_Deska.get_move(moves[f]["x"], moves[f]["y"])
                        if (Kontrola(Objekt_Deska.get_board(), moves[f]["x"], moves[f]["y"])):
                            if(player == "X"):
                                Objekt_Deska.set_score(inf)
                                Objekt_Deska.set_rozvoj()
                            if(player == "O"):
                                Objekt_Deska.set_score(-inf)
                                Objekt_Deska.set_rozvoj()
                    else: Objekt_Deska.get_move(moves[f]["x"], moves[f]["y"])
                    if (x == 1):
                        tree.get_smth(0, 0, 0, "branch").add_board(Objekt_Deska)
                    else: tree.get_smth(level_id, pocet_branch, 0, "branch").add_board(Objekt_Deska)
                pocet_branch += 1
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

def AI(deska, hrac, score, depth, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty, pocet_tahu, souradnice_x, souradnice_y):
    if (pocet_tahu == 1):
        podmínka = True
        while (podmínka):
            moznosti = [-1, 0, 1]
            value_x = choice(moznosti)
            value_y = choice(moznosti)
            if (value_x == 0 and value_y == 0):
                pass
            else:
                return souradnice_x + value_x, souradnice_y + value_y

    tree = Create_tree(deska, hrac, score, depth, hranice_topx, hranice_bottomx, hranice_lefty, hranice_righty)
    if (depth % 2) == 0:
        hrac = "O" if hrac == "X" else "X"
    for i in range (depth):
        depth_id = depth - 1 - i
        for branch_id in range (tree.get_smth(depth_id, 0, 0, "branch_count")):
            if (hrac == "O"):
                tree.set_smth(depth_id, branch_id, 0, "motherboard_score", inf)
                for element_id in range (tree.get_smth(depth_id, branch_id, 0, "element_count")):
                    el_score = tree.get_smth(depth_id, branch_id, element_id, "score")
                    mb_score = tree.get_smth(depth_id, branch_id, 0, "motherboard_score")
                    if (el_score < mb_score):
                         tree.set_smth(depth_id, branch_id, 0, "motherboard_score", el_score)
            elif (hrac == "X"):
                tree.set_smth(depth_id, branch_id, 0, "motherboard_score", -inf)
                for element_id in range (tree.get_smth(depth_id, branch_id, 0, "element_count")):
                    el_score = tree.get_smth(depth_id, branch_id, element_id, "score")
                    mb_score = tree.get_smth(depth_id, branch_id, 0, "motherboard_score")
                    if (el_score > mb_score):
                          tree.set_smth(depth_id, branch_id, 0, "motherboard_score", el_score)
        hrac = "O" if hrac == "X" else "X"
    best_move = tree.get_smth(0, 0, 0, "board_obj")
    hrac = "O" if hrac == "X" else "X"
    rozsah = tree.get_smth(0, 0, 0, "element_count")
    for element_id in range (rozsah):
        if hrac == "O":
            if (best_move.get_score() > tree.get_smth(0, 0, element_id, "score")):
                best_move = tree.get_smth(0, 0, element_id, "board_obj")
        if hrac == "X":
            if (best_move.get_score() < tree.get_smth(0, 0, element_id, "score")):
                best_move = tree.get_smth(0, 0, element_id, "board_obj")
    best_x, best_y = best_move.get_xy()
    return best_x, best_y

def Heuristika(deska, souradnice_x, souradnice_y):
    pocet_volnych, pocet_vrade, blocked, ob1 = pocet_pozic(deska, souradnice_x, souradnice_y)
    skore_toadd = 0
    for i in range (-1, 2):
        if (deska[souradnice_x+i][souradnice_y-1] != "X" and deska[souradnice_x+i][souradnice_y-1] != "O" ):
            skore_toadd += pocet_volnych
            if (deska[souradnice_x+i][souradnice_y-1] == None):
                deska[souradnice_x+i][souradnice_y-1] = str(pocet_volnych)
            else: deska[souradnice_x+i][souradnice_y-1] = str(int(deska[souradnice_x+i][souradnice_y-1])+pocet_volnych)
        if (deska[souradnice_x+i][souradnice_y] != "X" and deska[souradnice_x+i][souradnice_y] != "O" ):
            skore_toadd += pocet_volnych
            if (deska[souradnice_x+i][souradnice_y] == None):
                deska[souradnice_x+i][souradnice_y] = str(pocet_volnych)
            else: deska[souradnice_x+i][souradnice_y] = str(int(deska[souradnice_x+i][souradnice_y])+pocet_volnych)
        if (deska[souradnice_x+i][souradnice_y+1] != "X" and deska[souradnice_x+i][souradnice_y+1] != "O" ):
            skore_toadd += pocet_volnych
            if (deska[souradnice_x+i][souradnice_y+1] == None):
                deska[souradnice_x+i][souradnice_y+1] = str(pocet_volnych)
            else: deska[souradnice_x+i][souradnice_y+1] = str(int(deska[souradnice_x+i][souradnice_y+1])+pocet_volnych)
    length = len(pocet_vrade)
    if (length > 1):
        for x in pocet_vrade:
            for y in pocet_vrade:
                if x != y:
                    if (x["vektor"] == [-1, -1] and y["vektor"] == [1, 1]) or (x["vektor"] == [0, -1] and y["vektor"] == [0, 1]) or (x["vektor"] == [-1, 0] and y["vektor"] == [1, 0]) or (x["vektor"] == [1, -1] and y["vektor"] == [-1, 1]):
                        x["pocet_vrade"] + y["pocet_vrade"] + 1
                        if len(x["otevreno"]) > 0 and len(y["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"] + y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) - 3**(x["pocet_vrade"] + y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                            skore_toadd += (- 3**(x["pocet_vrade"] + y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2 - 3**(x["pocet_vrade"] + y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) *2)
                        elif len(x["otevreno"]) > 0:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"] + y["pocet_vrade"]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                            skore_toadd += (- 3**(x["pocet_vrade"] + y["pocet_vrade"]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        elif len(y["otevreno"]) > 0:
                            deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]] = str(int(deska[souradnice_x + y["otevreno"][0]][souradnice_y + y["otevreno"][1]]) - 3**(x["pocet_vrade"] + y["pocet_vrade"]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                            skore_toadd += (- 3**(x["pocet_vrade"] + y["pocet_vrade"]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        pocet_vrade.pop(pocet_vrade.index(x))
                        pocet_vrade.pop(pocet_vrade.index(y))
                        length -= 2 

    if (length > 0 and len(ob1) > 0):
        for x in pocet_vrade:
            for y in ob1:
                if (x["vektor"] == [-1, -1] and y["vektor"] == [1, 1]) or (x["vektor"] == [1, 1] and y["vektor"] == [-1, -1]) or (x["vektor"] == [0, -1] and y["vektor"] == [0, 1]) or (x["vektor"] == [0, 1] and y["vektor"] == [0, -1]) or (x["vektor"] == [-1, 0] and y["vektor"] == [1, 0]) or (x["vektor"] == [1, 0] and y["vektor"] == [-1, 0]) or (x["vektor"] == [1, -1] and y["vektor"] == [-1, 1]) or (x["vektor"] == [-1, 1] and y["vektor"] == [1, -1]):
                    if (len(x["otevreno"]) > 0 and len(y["open"]) > 1):
                        deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) * 2)
                        deska[souradnice_x + y["open"][0]][souradnice_y + y["open"][1]] = str(int(deska[souradnice_x + y["open"][0]][souradnice_y + y["open"][1]]) - 3**(y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) * 2)
                        deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]] = str(int(deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]]) - 3**(y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) * 2)
                    elif (len(x["otevreno"]) > 0):
                        deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]] = str(int(deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]]) - 3**(y["pocet_vrade"]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                    elif (len(y["open"]) > 1):
                        deska[souradnice_x + y["open"][0]][souradnice_y + y["open"][1]] = str(int(deska[souradnice_x + y["open"][0]][souradnice_y + y["open"][1]]) - 3**(y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                        deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]] = str(int(deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]]) - 3**(y["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1))
                    elif (x["pocet_vrade"] + y["pocet_vrade"] == 3):
                        deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]] = str(int(deska[souradnice_x + y["vektor"][0]][souradnice_y + y["vektor"][1]]) - 3**(y["pocet_vrade"]) + 3**(x["pocet_vrade"] + y["pocet_vrade"] + 1) * 2)
                    pocet_vrade.pop(pocet_vrade.index(x))
                    ob1.pop(ob1.index(y))

    if (length != 0):
        for x in pocet_vrade:
            vec = otočit_vektor(copy.deepcopy(x["vektor"]))
            if (x["skipped"] == 1):
                if(len(x["otevreno"]) > 2):
                    if deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O":
                        deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"]) * 2 + 3**(x["pocet_vrade"] +1) *2)
                        deska[souradnice_x + x["otevreno"][2]][souradnice_y + x["otevreno"][3]] = str(int(deska[souradnice_x + x["otevreno"][2]][souradnice_y + x["otevreno"][3]]) - 3**(x["pocet_vrade"]) * 2 + 3**(x["pocet_vrade"] +1) *2)
                        deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"] +1) *2)
                        skore_toadd += (- 3**(x["pocet_vrade"]) * 2 + 3**(x["pocet_vrade"] +1) *2 - 3**(x["pocet_vrade"]) * 2 + 3**(x["pocet_vrade"] +1) *2 + 3**(x["pocet_vrade"] +1) *2)
                    else:
                        deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"] +1))
                        deska[souradnice_x + x["otevreno"][2]][souradnice_y + x["otevreno"][3]] = str(int(deska[souradnice_x + x["otevreno"][2]][souradnice_y + x["otevreno"][3]]) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"] +1))
                        skore_toadd += (- 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"] +1) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"] +1))
                elif(len(x["otevreno"]) > 0):
                    if deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O":
                        deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"] +1))
                        deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"] +1))
                        skore_toadd += (- 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"] +1) + 3**(x["pocet_vrade"] +1))
            if (x["skipped"] == 0):
                if (len(x["otevreno"]) > 0):
                    if deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O":
                        deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"] +1) *2)
                        if x["pocet_vrade"] > 1:
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) - 3**(x["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] +1) *2)
                            skore_toadd += (+ 3**(x["pocet_vrade"] +1) *2 - 3**(x["pocet_vrade"]) *2 + 3**(x["pocet_vrade"] +1) *2)
                        else: 
                            deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] +1) *2)
                            skore_toadd += (+ 3**(x["pocet_vrade"] +1) *2 + 3**(x["pocet_vrade"] +1) *2)
                    else:
                        deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]] = str(int(deska[souradnice_x + x["otevreno"][0]][souradnice_y + x["otevreno"][1]]) + 3**(x["pocet_vrade"] +1))
                        skore_toadd += 3**(x["pocet_vrade"] +1)
                elif deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O":
                    deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"] +1))
                    skore_toadd += 3**(x["pocet_vrade"] +1)

    if (len(blocked) != 0):
        for x in blocked:
            if (x["side"] == 1):
                deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]] = str(int(deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]]) - 3**x["pocet_vrade"])
                skore_toadd += (3**x["pocet_vrade"])
            else:
                if (len(x["blocked"]) > 2):
                    deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]] = str(int(deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]]) - 3**x["pocet_vrade"])
                    deska[souradnice_x + x["blocked"][2]][souradnice_y + x["blocked"][3]] = str(int(deska[souradnice_x + x["blocked"][2]][souradnice_y + x["blocked"][3]]) - 3**x["pocet_vrade"])
                    skore_toadd += (3**x["pocet_vrade"] + 3**x["pocet_vrade"])
                else: 
                    deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]] = str(int(int(deska[souradnice_x + x["blocked"][0]][souradnice_y + x["blocked"][1]]) - ((3**x["pocet_vrade"])+1)/2))
                    skore_toadd += ((3**x["pocet_vrade"])+1)/2

    if (len(ob1) != 0):
        for x in ob1:
            vec = otočit_vektor(copy.deepcopy(x["vektor"]))
            if (x["pocet_vrade"] == 3):
                deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]] = str(int(deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]]) + 3**(x["pocet_vrade"]+1)*2)
                skore_toadd += 3**(x["pocet_vrade"]+1)*2
            elif (deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O") and (len(x["open"]) > 1):
                deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]] = str(int(deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]]) - 3**(x["pocet_vrade"])*2 + 3**(x["pocet_vrade"]+1)*2)
                deska[souradnice_x + x["open"][0]][souradnice_y + x["open"][1]] = str(int(deska[souradnice_x + x["open"][0]][souradnice_y + x["open"][1]]) - 3**(x["pocet_vrade"])*2 + 3**(x["pocet_vrade"]+1)*2)
                deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"]+1)*2)
                skore_toadd += (- 3**(x["pocet_vrade"])*2 + 3**(x["pocet_vrade"]+1)*2 - 3**(x["pocet_vrade"])*2 + 3**(x["pocet_vrade"]+1)*2 + 3**(x["pocet_vrade"]+1)*2)
            elif (len(x["open"]) > 1):
                deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]] = str(int(deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]]) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"]+1))
                deska[souradnice_x + x["open"][0]][souradnice_y + x["open"][1]] = str(int(deska[souradnice_x + x["open"][0]][souradnice_y + x["open"][1]]) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"]+1))
                skore_toadd += (- 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"]+1) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"]+1))
            elif (deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "X" and deska[souradnice_x + vec[0]][souradnice_y + vec[1]] != "O") and (len(x["open"]) == 1):
                deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]] = str(int(deska[souradnice_x + x["vektor"][0]][souradnice_y + x["vektor"][1]]) - 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"]+1))
                deska[souradnice_x + vec[0]][souradnice_y + vec[1]] = str(int(deska[souradnice_x + vec[0]][souradnice_y + vec[1]]) + 3**(x["pocet_vrade"]+1))
                skore_toadd += (- 3**(x["pocet_vrade"]) + 3**(x["pocet_vrade"]+1) + 3**(x["pocet_vrade"]+1))
    return skore_toadd

def otočit_vektor(vektor):
    vektor_new = []
    vektor_new.append(vektor[0] * -1)
    vektor_new.append(vektor[1] * -1)
    return vektor_new


def pocet_pozic(deska, souradnice_x, souradnice_y):
    pocet = 0
    inline = []
    blocked = []
    ob1 = []
    for i in range (-1, 2):
        vektor = []
        if (deska[souradnice_x+i][souradnice_y-1] != "X" and deska[souradnice_x+i][souradnice_y-1] != "O"):
            pocet += 1
            if (deska[souradnice_x+i*2][souradnice_y-2] == deska[souradnice_x][souradnice_y]):
                vektor.append(i)
                vektor.append(-1)
                pocet_vrade, open = skip1(deska, souradnice_x, souradnice_y, vektor)
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "open": open}
                ob1.append(dictionary)
                vektor = []
        elif (deska[souradnice_x][souradnice_y] == deska[souradnice_x+i][souradnice_y-1]):
            vektor.append(i)
            vektor.append(-1)
            pocet_vrade, otevrena, skipped = how_many_more(deska, souradnice_x, souradnice_y, vektor)
            dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "otevreno": otevrena, "skipped": skipped}
            inline.append(dictionary)
            vektor = []
        elif (deska[souradnice_x][souradnice_y] != deska[souradnice_x+i][souradnice_y-1]):
            vektor.append(i)
            vektor.append(-1)
            pocet_vrade, blocked_vec, side = how_many_blocked(deska, souradnice_x, souradnice_y, vektor)
            if (len(blocked_vec) > 0):
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "blocked": blocked_vec, "side": side}
                blocked.append(dictionary)
            vektor = []
        
        if (deska[souradnice_x+i][souradnice_y] != "X" and deska[souradnice_x+i][souradnice_y] != "O" ):
            pocet += 1
            if (deska[souradnice_x+i*2][souradnice_y] == deska[souradnice_x][souradnice_y]):
                vektor.append(i)
                vektor.append(0)
                pocet_vrade, open = skip1(deska, souradnice_x, souradnice_y, vektor)
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "open": open}
                ob1.append(dictionary)
                vektor = []
        elif(deska[souradnice_x][souradnice_y] == deska[souradnice_x+i][souradnice_y] and i != 0):
            vektor.append(i)
            vektor.append(0)
            pocet_vrade, otevrena, skipped = how_many_more(deska, souradnice_x, souradnice_y, vektor)
            dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "otevreno": otevrena, "skipped": skipped}
            inline.append(dictionary)
            vektor = []
        elif(deska[souradnice_x][souradnice_y] != deska[souradnice_x+i][souradnice_y] and i != 0):
            vektor.append(i)
            vektor.append(0)
            pocet_vrade, blocked_vec, side = how_many_blocked(deska, souradnice_x, souradnice_y, vektor)
            if (len(blocked_vec) > 0):
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "blocked": blocked_vec, "side": side}
                blocked.append(dictionary)
            vektor = []
        
        if (deska[souradnice_x+i][souradnice_y+1] != "X" and deska[souradnice_x+i][souradnice_y+1] != "O" ):
            pocet += 1
            if (deska[souradnice_x+i*2][souradnice_y+2] == deska[souradnice_x][souradnice_y]):
                vektor.append(i)
                vektor.append(1)
                pocet_vrade, open = skip1(deska, souradnice_x, souradnice_y, vektor)
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "open": open}
                ob1.append(dictionary)
                vektor = []
        elif(deska[souradnice_x][souradnice_y] == deska[souradnice_x+i][souradnice_y+1]):
            vektor.append(i)
            vektor.append(1)
            pocet_vrade, otevrena, skipped = how_many_more(deska, souradnice_x, souradnice_y, vektor)
            dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "otevreno": otevrena, "skipped": skipped}
            inline.append(dictionary)
            vektor = []
        elif(deska[souradnice_x][souradnice_y] != deska[souradnice_x+i][souradnice_y+1]):
            vektor.append(i)
            vektor.append(1)
            pocet_vrade, blocked_vec, side = how_many_blocked(deska, souradnice_x, souradnice_y, vektor)
            if (len(blocked_vec) > 0):
                dictionary = {"vektor": vektor, "pocet_vrade": pocet_vrade, "blocked": blocked_vec, "side": side}
                blocked.append(dictionary)
            vektor = []
    return pocet, inline, blocked, ob1

def how_many_more(deska, souradnice_x, souradnice_y, vektor):
    more = 1
    list = []
    skipped = 0
    for i in range (2, 5):
        if (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] == deska[souradnice_x][souradnice_y]):
            more += 1
        elif (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "X" and deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "O"):
            list.append(vektor[0] * i)
            list.append(vektor[1] * i)
            if (deska[souradnice_x + vektor[0] * (i + 1)][souradnice_y + vektor[1] * (i + 1)] == deska[souradnice_x][souradnice_y]):
                more +=1
                skipped += 1
                if (deska[souradnice_x + vektor[0] * (i + 2)][souradnice_y + vektor[1] * (i + 2)] != "X" and deska[souradnice_x + vektor[0] * (i + 2)][souradnice_y + vektor[1] * (i + 2)] != "O"):
                    list.append(vektor[0] * (i + 2))
                    list.append(vektor[1] * (i + 2))
                elif (deska[souradnice_x + vektor[0] * (i + 2)][souradnice_y + vektor[1] * (i + 2)] == deska[souradnice_x][souradnice_y]):
                    more +=1
                    if (deska[souradnice_x + vektor[0] * (i + 3)][souradnice_y + vektor[1] * (i + 3)] != "X" and deska[souradnice_x + vektor[0] * (i + 3)][souradnice_y + vektor[1] * (i + 3)] != "O"):
                        list.append(vektor[0] * (i + 3))
                        list.append(vektor[1] * (i + 3))
            return more, list, skipped
        else: return more, list, skipped
    return more, list, skipped

def how_many_blocked(deska, souradnice_x, souradnice_y, vektor):
    more = 1
    x = 1
    y = 1
    list = []
    side = 2
    vec = otočit_vektor(vektor)
    for i in range (2, 5):
        if (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] == deska[souradnice_x + vektor[0]][souradnice_y + vektor[1]] and y == 1):
            more += 1
        elif (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "X" and deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "O" and y == 1):
            list.append(vektor[0] * i)
            list.append(vektor[1] * i)
            y = 2
        elif (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] == "X" or deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] == "O" and y == 1):
            y=2
        if (deska[souradnice_x + vec[0] * (i - 1)][souradnice_y + vec[1] * (i - 1)] == deska[souradnice_x + vektor[0]][souradnice_y + vektor[1]] and x == 1):
            more += 1
        elif (deska[souradnice_x + vec[0] * (i-1)][souradnice_y + vec[1] * (i-1)] != "X" and deska[souradnice_x + vec[0] * (i-1)][souradnice_y + vec[1] * (i-1)] != "O" and x == 1 and i > 2):
            list.append(vec[0] * (i - 1))
            list.append(vec[1] * (i - 1))
            x = 2
        elif (deska[souradnice_x + vec[0] * (i-1)][souradnice_y + vec[1] * (i-1)] != "X" and deska[souradnice_x + vec[0] * (i-1)][souradnice_y + vec[1] * (i-1)] != "O" and x == 1 and i == 2):
            side -= 1
            x = 2 
        else:
            x = 2     
    return more, list, side

def skip1(deska, souradnice_x, souradnice_y, vektor):
    more = 1
    list = []
    for i in range (3,5):
        if (deska[souradnice_x][souradnice_y] == deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i]):
            more += 1
        elif (deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "X" and deska[souradnice_x + vektor[0] * i][souradnice_y + vektor[1] * i] != "O"):
            list.append(vektor[0] * i)
            list.append(vektor[1] * i)
            return more, list
        else: 
            list.append(1) 
            return more, list
    return more, list


