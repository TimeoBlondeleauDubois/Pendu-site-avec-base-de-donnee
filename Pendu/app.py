from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'b_5#y2L"F4Q8z\n\xec]/'

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

@app.route("/")
def index():
    session.clear()  # Réinitialiser la session
    return render_template("game.html", resultat="")

@app.route("/jouer", methods=["POST"])
def jouer():
    if 'mot_a_deviner' not in session:
        session['mot_a_deviner'] = choisir_mot()

    lettres_trouvees = session.get('lettres_trouvees', [])
    tentatives_max = 6
    tentatives_restantes = session.get('tentatives_restantes', tentatives_max)

    lettre = request.form.get("lettre").lower()

    if len(lettre) != 1 or not lettre.isalpha():
        return render_template("game.html", resultat="Veuillez entrer une seule lettre.")

    if lettre in lettres_trouvees:
        return render_template("game.html", resultat="Vous avez déjà deviné cette lettre. Essayez une autre.")

    if lettre not in session['mot_a_deviner']:
        tentatives_restantes -= 1
        lettres_trouvees.append(lettre)

    session['lettres_trouvees'] = lettres_trouvees
    session['tentatives_restantes'] = tentatives_restantes

    mot_cache = afficher_mot_cache(session['mot_a_deviner'], lettres_trouvees)

    if "_" not in mot_cache:
        resultat = "Félicitations, vous avez deviné le mot!"
    elif tentatives_restantes == 0:
        resultat = "Désolé, vous avez épuisé toutes vos tentatives. Le mot était '{}'.".format(session['mot_a_deviner'])
    else:
        resultat = mot_cache

    return render_template("game.html", resultat=resultat, tentatives_restantes=tentatives_restantes)

if __name__ == "__main__":
    app.run(debug=True)
