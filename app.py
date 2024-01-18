from flask import Flask, render_template, request, redirect, url_for, session
from bcrypt import hashpw, gensalt
import sqlite3
import random

app = Flask(__name__)
app.secret_key = 'b_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    return render_template('login.html')

def connect_db():
    db_path = 'Pendu.db'
    print(f"Connecté à la base de données : {db_path}")
    return sqlite3.connect(db_path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            return redirect(url_for('dashboard'))
        else:
            error = 'Nom d\'utilisateur ou mot de passe incorrect'
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Avant create_user: {username}, {password}")
        if create_user(username, password):
            print("Après create_user: Utilisateur créé avec succès")
            return redirect(url_for('login'))
        else:
            error = 'Nom d\'utilisateur déjà pris'
    return render_template('signup.html', error=error)



@app.route('/dashboard')
def dashboard():
    return render_template('difficulty.html')

def check_credentials(username, password):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT Mot_De_Passe FROM User WHERE Nom_Utilisateur = ?", (username,))
        stored_password = cursor.fetchone()

    if stored_password is not None:
        stored_password = stored_password[0]
        if hashpw(password.encode('utf-8'), stored_password) == stored_password:
            return True

    return False


def create_user(username, password):
    try:
        hashed_password = hashpw(password.encode('utf-8'), gensalt())
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute("INSERT INTO User (Nom_Utilisateur, Mot_De_Passe) VALUES (?, ?)", (username, hashed_password))
        print(f"Utilisateur {username} créé avec succès")
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de l'utilisateur : {e}")
        return False

@app.route('/dashboard', methods=['GET', 'POST'])
def choose_difficulty():
    if request.method == 'POST':
        difficulty = request.form['difficulty']
        return redirect(url_for('game', difficulty=difficulty))
    return render_template('choose_difficulty.html')

@app.route('/game/<difficulty>')
def game(difficulty):
    return render_template('game.html', difficulty=difficulty)




#Pendu
def choisir_mot():
    mots = ["python"]
    return random.choice(mots)

def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_cache += lettre
        else:
            mot_cache += "_"
    return mot_cache

@app.route("/pendu")
def index():
    if 'mot_a_deviner' not in session:
        session['mot_a_deviner'] = choisir_mot()


    session['lettres_trouvees'] = []
    session['tentatives_restantes'] = 6

    lettres_trouvees = session['lettres_trouvees']
    tentatives_restantes = session['tentatives_restantes']

    mot_cache = afficher_mot_cache(session['mot_a_deviner'], lettres_trouvees)

    return render_template("game.html", resultat=mot_cache, tentatives_restantes=tentatives_restantes, lettres_trouvees=lettres_trouvees, message="")


@app.route("/jouer", methods=["POST"])
def jouer():
    if 'mot_a_deviner' not in session:
        session['mot_a_deviner'] = choisir_mot()

    lettre = request.form.get("lettre").lower()


    if 'lettres_trouvees' not in session:
        session['lettres_trouvees'] = []
    if 'tentatives_restantes' not in session:
        session['tentatives_restantes'] = 6

    lettres_trouvees = session['lettres_trouvees']
    tentatives_restantes = session['tentatives_restantes']

    message = ""

    if len(lettre) != 1 or not lettre.isalpha():
        message = "Veuillez entrer une seule lettre."
    elif lettre in lettres_trouvees:
        message = "Vous avez déjà deviné cette lettre. Essayez une autre."
    elif lettre not in session['mot_a_deviner']:
        tentatives_restantes -= 1
        lettres_trouvees.append(lettre)
    else:
        lettres_trouvees.append(lettre)

    session['lettres_trouvees'] = lettres_trouvees
    session['tentatives_restantes'] = tentatives_restantes

    mot_cache = afficher_mot_cache(session['mot_a_deviner'], lettres_trouvees)

    if "_" not in mot_cache or tentatives_restantes == 0:
        session['message_fin'] = message
        return redirect("/fin-de-partie")

    return render_template("game.html", resultat=mot_cache, tentatives_restantes=tentatives_restantes, lettres_trouvees=lettres_trouvees, message=message)

@app.route("/fin-de-partie")
def fin_de_partie():
    mot_a_deviner = session.get('mot_a_deviner', '')
    message_fin = session.get('message_fin', '')
    
    if "_" not in afficher_mot_cache(mot_a_deviner, session.get('lettres_trouvees', [])):
        resultat = "Gagné"
    else:
        resultat = "Perdu"

    return render_template("fin_de_partie.html", resultat=resultat, mot_a_deviner=mot_a_deviner, message_fin=message_fin)

if __name__ == "__main__":
    app.run(debug=True)

