import sqlite3

connection = sqlite3.connect('Pendu.db')
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS User (
        US_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nom_Utilisateur VARCHAR UNIQUE,
        Mot_De_Passe VARCHAR
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Liste_De_Mots (
        Li_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Mot VARCHAR,
        Difficulty TINYINT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Score (
        SC_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        US_Id INTEGER,
        Nb_Partie_Gagner TINYINT,
        Nb_Partie_Perdu TINYINT,
        Niveau_De_Difficulte VARCHAR,
        Date_Du_Jeu DATETIME,
        FOREIGN KEY (US_Id) REFERENCES User(US_Id)
    );
""")
connection.commit()
connection.close()
