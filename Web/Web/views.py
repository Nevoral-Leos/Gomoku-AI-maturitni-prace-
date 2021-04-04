from Web import app
from flask import render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from Web.Classes import Game
from Web.Mechaniky import AI, Kontrola, Heuristika
import copy

@app.route("/")
def index():
    if "board" not in session:
        array1, array2 = [], []
        for j in range(23): array1.append(None)
        for i in range(23): array2.append(copy.deepcopy(array1))
        session["board"] = copy.deepcopy(array2)
        session["game"] = Game()
        board = session["board"]
        game = session["game"]
        if (game.get_first_player() == 0):
            board[11][11] = session["game"].get_player()
            Heuristika(session["board"], 11, 11)
            game.nove_hranice(11, 11)
            game.change_player()
        elif (game.get_first_player() == 2):
            if (game.get_poradi() == 1):
                game.set_poradi(0)
            elif (game.get_poradi() == 0):
                game.set_poradi(1)
                board[11][11] = game.get_player()
                Heuristika(board, 11, 11)
                game.nove_hranice(11, 11)
                game.change_player()
    board = get_from_session("board")
    game = get_from_session("game")
    return render_template("index.html", playboard = board, winnerFound = game.get_win(), winner = game.get_player(), score = game.get_score())

@app.route("/playfirst")
def playfirst():
    session["game"].set_first_player(1)
    return redirect(url_for("index"))

@app.route("/aifirst")
def aifirst():
    session["game"].set_first_player(0)
    return redirect(url_for("index"))

@app.route("/swap")
def swap():
    session["game"].set_first_player(2)
    return redirect(url_for("index"))

@app.route("/play/<int:x>/<int:y>")
def play(x, y):
    board = get_from_session("board")
    game = get_from_session("game")
    if (board[x+4][y+4] != None and board[x+4][y+4] != "X" and board[x+4][y+4] != "O"): 
        value = int(board[x+4][y+4])
    else: value = 0
    board[x+4][y+4] = game.get_player()
    winner = Kontrola(board, x+4, y+4)
    if (winner):
        game.set_win()
        return redirect(url_for("index"))
    if (game.get_player() == "O"):
        value += Heuristika(board, x+4, y+4)
        game.set_score(-value)
    else:
        game.set_score(Heuristika(board, x+4, y+4) + value)
    game.nove_hranice(x+4, y+4)
    print(game.get_score(), game.get_player())
    game.change_player()
    hranice_topx, hranice_bottomx, hranice_lefty, hrnice_righty = game.get_hranice()
    x, y = AI(board, game.get_player(), game.get_score(), 4, hranice_topx, hranice_bottomx, hranice_lefty, hrnice_righty, game.get_pocet_tahu(), x+4, y+4)
    if (board[x][y] != None): 
        value = int(board[x][y])
    else: value = 0
    board[x][y] = game.get_player()
    winner = Kontrola(board, x, y)
    if (winner):
        game.set_win()
        return redirect(url_for("index"))
    if (game.get_player() == "O"):
        value += Heuristika(board, x, y)
        game.set_score(-value)
    else:
        game.set_score(Heuristika(board, x, y) + value) 
    print(game.get_score(), game.get_player())
    game.nove_hranice(x, y)
    game.change_player()
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    array1, array2 = [], []
    for j in range(23): array1.append(None)
    for i in range(23): array2.append(copy.deepcopy(array1))
    session["board"] = copy.deepcopy(array2)
    board = get_from_session("board")
    game = get_from_session("game")
    game.reset()
    if (game.get_first_player() == 0):
        board[11][11] = game.get_player()
        Heuristika(session["board"], 11, 11)
        game.nove_hranice(11, 11)
        game.change_player()
    elif (game.get_first_player() == 2):
        if (game.get_poradi() == 1):
            game.set_poradi(0)
        elif (game.get_poradi() == 0):
            game.set_poradi(1)
            board[11][11] = game.get_player()
            Heuristika(session["board"], 11, 11)
            game.nove_hranice(11, 11)
            game.change_player()
    return redirect(url_for("index"))

def get_from_session(what):
    obj = None	
    while obj == None:
        try: obj = session[what]
        except: continue
    return obj