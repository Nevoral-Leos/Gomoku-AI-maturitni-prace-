from Web import app
from flask import render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
from Web.Classes import Game
from Web.Mechaniky import AI, Kontrola, Heuristika
import copy

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if "board" not in session:
        array1, array2 = [], []
        for j in range(23): array1.append(None)
        for i in range(23): array2.append(copy.deepcopy(array1))
        session["board"] = copy.deepcopy(array2)
        session["game"] = Game()
        if (session["game"].get_first_player() == 0):
            session["board"][11][11] = session["game"].get_player()
            Heuristika(session["board"], 11, 11)
            session["game"].nove_hranice(11, 11)
            session["game"].change_player()
        elif (session["game"].get_first_player() == 2):
            if (session["game"].get_poradi() == 1):
                session["game"].set_poradi(0)
            elif (session["game"].get_poradi() == 0):
                session["game"].set_poradi(1)
                session["board"][11][11] = session["game"].get_player()
                Heuristika(session["board"], 11, 11)
                session["game"].nove_hranice(11, 11)
                session["game"].change_player()
    return render_template("index.html", board = session["board"], winnerFound = session["game"].get_win(), winner = session["game"].get_player(), score = session["game"].get_score())

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
    if (session["board"][x+4][y+4] != None): 
        value = int(session["board"][x+4][y+4])
    else: value = 0
    session["board"][x+4][y+4] = session["game"].get_player()
    winner = Kontrola(session["board"], x+4, y+4)
    if (winner):
        session["game"].set_win()
        return redirect(url_for("index"))
    if (session["game"].get_player() == "O"):
        value += Heuristika(session["board"], x+4, y+4)
        session["game"].set_score(-value)
    else:
        session["game"].set_score(Heuristika(session["board"], x+4, y+4) + value)
    session["game"].nove_hranice(x+4, y+4)
    print(session["game"].get_score(), session["game"].get_player())
    session["game"].change_player()
    hranice_topx, hranice_bottomx, hranice_lefty, hrnice_righty = session["game"].get_hranice()
    x, y = AI(session["board"], session["game"].get_player(), session["game"].get_score(), 4, hranice_topx, hranice_bottomx, hranice_lefty, hrnice_righty, session["game"].get_pocet_tahu(), x+4, y+4)
    if (session["board"][x][y] != None): 
        value = int(session["board"][x][y])
    else: value = 0
    session["board"][x][y] = session["game"].get_player()
    winner = Kontrola(session["board"], x, y)
    if (winner):
        session["game"].set_win()
        return redirect(url_for("index"))
    if (session["game"].get_player() == "O"):
        value += Heuristika(session["board"], x, y)
        session["game"].set_score(-value)
    else:
        session["game"].set_score(Heuristika(session["board"], x, y) + value) 
    print(session["game"].get_score(), session["game"].get_player())
    session["game"].nove_hranice(x, y)
    session["game"].change_player()
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    array1, array2 = [], []
    for j in range(23): array1.append(None)
    for i in range(23): array2.append(copy.deepcopy(array1))
    session["board"] = copy.deepcopy(array2)
    session["game"].reset()
    if (session["game"].get_first_player() == 0):
        session["board"][11][11] = session["game"].get_player()
        Heuristika(session["board"], 11, 11)
        session["game"].nove_hranice(11, 11)
        session["game"].change_player()
    elif (session["game"].get_first_player() == 2):
        if (session["game"].get_poradi() == 1):
            session["game"].set_poradi(0)
        elif (session["game"].get_poradi() == 0):
            session["game"].set_poradi(1)
            session["board"][11][11] = session["game"].get_player()
            Heuristika(session["board"], 11, 11)
            session["game"].nove_hranice(11, 11)
            session["game"].change_player()
    return redirect(url_for("index"))
