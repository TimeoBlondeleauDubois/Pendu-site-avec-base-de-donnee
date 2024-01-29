from flask import Flask, render_template, request, redirect, url_for, session
from bcrypt import hashpw, gensalt
import sqlite3, random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'b_5#y2L"F4Q8z\n\xec]/'


connection = sqlite3.connect('Pendu.db')
cursor = connection.cursor()

@app.route('/')
def home():
    return render_template('login.html')

def connect_db():
    db_path = 'Pendu.db'
    print(f"Connecté à la base de données : {db_path}")
    return sqlite3.connect(db_path)


#Utilisateur
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
        cursor.execute("SELECT US_Id, Mot_De_Passe FROM User WHERE Nom_Utilisateur = ?", (username,))
        user_data = cursor.fetchone()

    if user_data is not None:
        user_id, stored_password = user_data
        if hashpw(password.encode('utf-8'), stored_password) == stored_password:
            session['user_id'] = user_id
            return user_id

    return None



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


#Difficulté
@app.route('/game/<difficulty>')
def game(difficulty):
    session['mot_a_deviner'] = choisir_mot(difficulty)
    session['lettres_trouvees'] = []
    session['tentatives_restantes'] = 6
    session['difficulty'] = difficulty
    session.pop('message_fin', None)
    session['Date_Du_Jeu'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('game.html', difficulty=difficulty)



#Pendu
def choisir_mot(difficulty):
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT Mot FROM Liste_De_Mots WHERE Difficulty = ? ORDER BY RANDOM() LIMIT 1", (difficulty,))
        mot = cursor.fetchone()

    if mot:
        mot = mot[0].lower()
        print(f"Mot choisi : {mot}")
        return mot
    else:
        print("Aucun mot trouvé dans la base de données.")
        return None


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

    print(f"Mot à deviner : {session['mot_a_deviner']}")
    print(f"Lettres trouvées : {lettres_trouvees}")
    print(f"Tentatives restantes : {tentatives_restantes}")

    session.pop('message_fin', None)
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
        message = "Veuillez entrer une lettre."
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


@app.route('/recommencer_une_partie')
def recommencer_une_partie():
    return render_template('difficulty.html')

#Score
@app.route("/fin-de-partie")
def fin_de_partie():
    mot_a_deviner = session.get('mot_a_deviner', '')
    message_fin = session.get('message_fin', '')
    user_id = session.get('user_id')
    difficulty = session.get('difficulty', 'Facile')
    
    Date_Du_Jeu = session.get('Date_Du_Jeu', '')
    
    if "_" not in afficher_mot_cache(mot_a_deviner, session.get('lettres_trouvees', [])):
        resultat = "Gagné"
        update_column = f'Nb_Partie_Gagner_{difficulty}'
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute(f"UPDATE User SET {update_column} = {update_column} + 1, Date_Du_Jeu = ? WHERE US_Id = ?", (Date_Du_Jeu, user_id,))
            print(f"Mise à jour du nombre de parties gagnées et de la date pour l'utilisateur {user_id}")
    else:
        resultat = "Perdu"
        update_column = f'Nb_Partie_Perdu_{difficulty}'
        with connect_db() as db:
            cursor = db.cursor()
            cursor.execute(f"UPDATE User SET {update_column} = {update_column} + 1, Date_Du_Jeu = ? WHERE US_Id = ?", (Date_Du_Jeu, user_id,))
            print(f"Mise à jour du nombre de parties perdues et de la date pour l'utilisateur {user_id}")

    return render_template("fin_de_partie.html", resultat=resultat, mot_a_deviner=mot_a_deviner, message_fin=message_fin, difficulty=difficulty)

if __name__ == "__main__":
    app.run(debug=True)

connection.commit()
connection.close()

