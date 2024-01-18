from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = 'b_5#y2L"F4Q8z\n\xec]/'

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

@app.route("/")
def index():
    if 'mot_a_deviner' not in session:
        session['mot_a_deviner'] = choisir_mot()

    # Réinitialiser les valeurs de session pour une nouvelle partie
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

    # Assurez-vous que les valeurs de session sont correctement initialisées
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
