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
    CREATE TABLE IF NOT EXISTS Partie (
        Partie_Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_Du_Jeu DATETIME DEFAULT CURRENT_TIMESTAMP,
        Mot_A_Deviner VARCHAR,
        Gagne_Facile INTEGER DEFAULT 0,
        Perdu_Facile INTEGER DEFAULT 0,
        Gagne_Moyen INTEGER DEFAULT 0,
        Perdu_Moyen INTEGER DEFAULT 0,
        Gagne_Difficile INTEGER DEFAULT 0,
        Perdu_Difficile INTEGER DEFAULT 0,
        User_Id INTEGER,
        FOREIGN KEY(User_Id) REFERENCES User(US_Id)
    );
""")

connection.commit()
connection.close()
