from Web import app
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from Web.Classes import Game
from Web.Mechaniky import AI, Pick_first_player, Kontrola, Heuristika
import copy

XO = Game()
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if "board" not in session:
        array1, array2 = [], []
        for j in range(23): array1.append(None)
        for i in range(23): array2.append(copy.deepcopy(array1))
        session["board"] = copy.deepcopy(array2)
        if (Pick_first_player()):
            session["board"][11][11] = XO.get_player()
            Heuristika(session["board"], 11, 11)
            XO.nove_hranice(11, 11)
            XO.change_player()
    return render_template("index.html", board = session["board"], winnerFound = XO.get_win(), winner = XO.get_player(), score = XO.get_score())

@app.route("/play/<int:x>/<int:y>")
def play(x, y):
    if ( XO.get_player == "O" and session["board"][x+4][y+4] != None):
        value = -int(session["board"][x+4][y+4])
        XO.set_score(value)
    elif (session["board"][x+4][y+4] != None):
        XO.set_score(int(session["board"][x+4][y+4]))
    session["board"][x+4][y+4] = XO.get_player()
    winner = Kontrola(session["board"], x+4, y+4)
    if (winner):
        XO.set_win()
        return redirect(url_for("index"))
    Heuristika(session["board"], x+4, y+4)
    XO.nove_hranice(x+4, y+4)
    XO.change_player()
    hranice_topx, hranice_bottomx, hranice_lefty, hrnice_righty = XO.get_hranice()
    x, y = AI(session["board"], XO.get_player(), XO.get_score(), 4, hranice_topx, hranice_bottomx, hranice_lefty, hrnice_righty, XO.get_pocet_tahu(), x+4, y+4)
    if (XO.get_player == "O" and session["board"][x][y] != None):
        value = -int(session["board"][x][y])
        XO.set_score(value)
    elif (session["board"][x][y] != None):
        XO.set_score(int(session["board"][x][y]))
    session["board"][x][y] = XO.get_player()
    winner = Kontrola(session["board"], x, y)
    if (winner):
        XO.set_win()
        return redirect(url_for("index"))
    Heuristika(session["board"], x, y)
    XO.nove_hranice(x, y)
    XO.change_player()
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    array1, array2 = [], []
    for j in range(23): array1.append(None)
    for i in range(23): array2.append(copy.deepcopy(array1))
    session["board"] = copy.deepcopy(array2)
    XO.reset()
    if (Pick_first_player()):
        session["board"][11][11] = XO.get_player()
        Heuristika(session["board"], 11, 11)
        XO.nove_hranice(11, 11)
        XO.change_player()
    return redirect(url_for("index"))
