import sqlite3

connection = sqlite3.connect('Pendu.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        US_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_Utilisateur VARCHAR UNIQUE,
        Mot_De_Passe VARCHAR,
        Nb_Partie_Gagner INTEGER DEFAULT 0,
        Nb_Partie_Perdu INTEGER DEFAULT 0,
        Niveau_De_Difficulte VARCHAR,
        Date_Du_Jeu DATETIME
);
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS Liste_De_Mots (
        Li_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Mot VARCHAR,
        Difficulty TINYINT
    );
""")

connection.commit()
connection.close()
