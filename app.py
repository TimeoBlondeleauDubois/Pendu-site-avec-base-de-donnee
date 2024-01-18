from flask import Flask, render_template, request, redirect, url_for
from bcrypt import hashpw, gensalt
import sqlite3
import random

app = Flask(__name__)

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



def choisir_mot():
    mots = ["python", "programmation", "informatique", "algorithmique", "developpement"]
    return random.choice(mots)

def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_cache += lettre
        else:
            mot_cache += "_"
    return mot_cache

def pendu():
    mot_a_deviner = choisir_mot()
    lettres_trouvees = []
    tentatives_max = 6
    tentatives_restantes = tentatives_max

    print("Bienvenue dans le jeu du pendu!")
    print(afficher_mot_cache(mot_a_deviner, lettres_trouvees))

    while tentatives_restantes > 0:
        lettre = input("Devinez une lettre : ").lower()

        if len(lettre) != 1 or not lettre.isalpha():
            print("Veuillez entrer une seule lettre.")
            continue

        if lettre in lettres_trouvees:
            print("Vous avez déjà deviné cette lettre. Essayez une autre.")
            continue

        if lettre in mot_a_deviner:
            print("Bonne devinette!")
            lettres_trouvees.append(lettre)
        else:
            print("Incorrect. Vous avez {} tentatives restantes.".format(tentatives_restantes - 1))
            tentatives_restantes -= 1

        mot_cache = afficher_mot_cache(mot_a_deviner, lettres_trouvees)
        print(mot_cache)

        if "_" not in mot_cache:
            print("Félicitations, vous avez deviné le mot!")
            break

    if "_" in afficher_mot_cache(mot_a_deviner, lettres_trouvees):
        print("Désolé, vous avez épuisé toutes vos tentatives. Le mot était '{}'.".format(mot_a_deviner))

if __name__ == "__main__":
    pendu()

