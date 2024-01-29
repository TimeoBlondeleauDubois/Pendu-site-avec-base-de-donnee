import sqlite3
from bcrypt import hashpw, gensalt

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
    Resultat VARCHAR DEFAULT NULL,
    Difficulty VARCHAR DEFAULT NULL,
    User_Id INTEGER,
    FOREIGN KEY(User_Id) REFERENCES User(US_Id)
);
""")

connection.commit()


#Intégrer les mots
cursor.execute("""
INSERT INTO Liste_De_Mots (Mot) VALUES
    ('Banane'), 
    ('Ordinateur'), 
    ('Girafe'), 
    ('Montgolfière'), 
    ('Bibliothèque'), 
    ('Papillon'), 
    ('Licorne'), 
    ('Tableau'), 
    ('Sauterelle'),
    ('Parachute'), 
    ('Coccinelle'), 
    ('Radiateur'), 
    ('Singe'), 
    ('Flamingo'), 
    ('Pamplemousse'), 
    ('Crocodile'), 
    ('Bougie'), 
    ('Astronaute'),
    ('Tornade'), 
    ('Trompette'), 
    ('Avalanche'), 
    ('Dragon'), 
    ('Pomme'), 
    ('Bateau'), 
    ('Cactus'), 
    ('Raisin'), 
    ('Cerise'), 
    ('Pyramide'), 
    ('Fusée'),
    ('Léopard'), 
    ('Escalier'), 
    ('Kangourou'), 
    ('Piano'), 
    ('Aéroport'), 
    ('Aquarium'), 
    ('Croissant'), 
    ('Chandelier'), 
    ('Tortue'),
    ('Pastèque'), 
    ('Cascade'), 
    ('Canapé'), 
    ('Éclair'), 
    ('Girouette'), 
    ('Magicien'), 
    ('Citrouille'), 
    ('Harmonica'), 
    ('Caméléon'), 
    ('Toboggan'),
    ('Clémentine'), 
    ('Miroir'), 
    ('Hibou'), 
    ('Cascade'), 
    ('Méridien'), 
    ('Hélicoptère'), 
    ('Velociraptor'), 
    ('Parapente'),
    ('Papaye'), 
    ('Ananas'), 
    ('Tapis'), 
    ('Ampoule'), 
    ('Zèbre'), 
    ('Parapluie'), 
    ('Fourchette'), 
    ('Volcan'), 
    ('Chien'), 
    ('Cheminée'), 
    ('Grenouille'),
    ('Lune'), 
    ('Labyrinthe'), 
    ('Pizza'), 
    ('Ciseaux'), 
    ('Hibiscus'), 
    ('Toupie'), 
    ('Feuille'), 
    ('Paon'), 
    ('Avion'), 
    ('Échelle'), 
    ('Chapeau'),
    ('Planète'), 
    ('Boussole'), 
    ('Microscope'), 
    ('Ruche'), 
    ('Souris'), 
    ('Perroquet'), 
    ('Tournesol'), 
    ('Escargot'), 
    ('Frisbee'), 
    ('Gâteau'),
    ('Galaxie'), 
    ('Horloge'), 
    ('Téléphone'), 
    ('Meuble'), 
    ('Oiseau'), 
    ('Océan'), 
    ('Harmonica'), 
    ('Tambour'), 
    ('Couronne'), 
    ('Ciseaux'),
    ('Maquillage'), 
    ('Lunettes'), 
    ('Poubelle'), 
    ('Moustache'), 
    ('Piscine'), 
    ('Caméra'), 
    ('Quiche'), 
    ('Cactus'),
    ('Échiquier'), 
    ('Grenade'),
    ('Hamburger'), 
    ('Livre'), 
    ('Pantoufle'), 
    ('Balançoire'), 
    ('Palais'), 
    ('Fusil'), 
    ('Boomerang'), 
    ('Dentifrice'), 
    ('Pneu'), 
    ('Monocycle'),
    ('Champignon'), 
    ('Ancre'), 
    ('Soucoupe'), 
    ('Train'), 
    ('Feuilleton'), 
    ('Filet'), 
    ('Bouclier'), 
    ('Bateau'), 
    ('Météore'), 
    ('Étiquette'),
    ('Réfrigérateur'), 
    ('Trampoline'), 
    ('Échelle'), 
    ('Chariot'), 
    ('Écureuil'), 
    ('Gâteau'), 
    ('Tuyau'), 
    ('Moustique'), 
    ('Tambour'), 
    ('Violon'),
    ('Gondole'), 
    ('Pyramide'), 
    ('Plongeon'), 
    ('Trottinette'), 
    ('Nourriture'), 
    ('Hibou'), 
    ('Baguette'), 
    ('Aile'), 
    ('Serpent'), 
    ('Souffleur'),
    ('Escalier'), 
    ('Pinceau'), 
    ('Clé'), 
    ('Diamant'), 
    ('Alligator'), 
    ('Haltère'), 
    ('Bouclier'), 
    ('Moulin'), 
    ('Toupie'), 
    ('Dauphin'), 
    ('Sorbet'),
    ('Lien'), 
    ('Monde'), 
    ('Clavier'), 
    ('Sandwich'), 
    ('Pince'), 
    ('Plante'), 
    ('Serpent'), 
    ('Piscine'), 
    ('Colibri'), 
    ('Gants'), 
    ('Gâteau'),
    ('Feuille'), 
    ('Hôtel'), 
    ('Porte'), 
    ('Cerf'), 
    ('Zèbre'), 
    ('Ballon'), 
    ('Fusil'), 
    ('Bague'), 
    ('Panda'), 
    ('Saut'), 
    ('Jumelles'), 
    ('Roue'),
    ('Carte'), 
    ('Chasseur'), 
    ('Caméléon'), 
    ('Chaussure'), 
    ('Ferme'), 
    ('Télévision'), 
    ('Râteau'), 
    ('Chouette'), 
    ('Serpent'), 
    ('Écharpe'),
    ('Fromage'), 
    ('Plongée'), 
    ('La');
""")

#Difficulté
cursor.execute("""
    UPDATE Liste_De_Mots
    SET Difficulty = 
        CASE 
            WHEN LENGTH(Mot) < 6 THEN "facile"
            WHEN LENGTH(Mot) BETWEEN 6 AND 9 THEN "moyen"
            ELSE "difficile"
        END
""")

# Création de l'utilisateur 'a' avec mot de passe 'a'
hashed_password_a = hashpw('a'.encode('utf-8'), gensalt())
cursor.execute("INSERT INTO User (Nom_Utilisateur, Mot_De_Passe) VALUES (?, ?)", ('a', hashed_password_a))

# Exemples pour l'utilisateur a avec des dates différentes
cursor.execute("""
    INSERT INTO Partie (Date_Du_Jeu, Mot_A_Deviner, Gagne_Facile, Perdu_Facile, Gagne_Moyen, Perdu_Moyen,
                       Gagne_Difficile, Perdu_Difficile, Resultat, Difficulty, User_Id)
    VALUES (DATETIME('now', '-7 days'), 'voiture', 0, 1, 0, 1, 0, 1, 'Perdu', 'Facile', 1)
""")

cursor.execute("""
    INSERT INTO Partie (Date_Du_Jeu, Mot_A_Deviner, Gagne_Facile, Perdu_Facile, Gagne_Moyen, Perdu_Moyen,
                       Gagne_Difficile, Perdu_Difficile, Resultat, Difficulty, User_Id)
    VALUES (DATETIME('now', '-5 days'), 'avion', 0, 0, 1, 1, 0, 1, 'Perdu', 'Moyen', 1)
""")

cursor.execute("""
    INSERT INTO Partie (Date_Du_Jeu, Mot_A_Deviner, Gagne_Facile, Perdu_Facile, Gagne_Moyen, Perdu_Moyen,
                       Gagne_Difficile, Perdu_Difficile, Resultat, Difficulty, User_Id)
    VALUES (DATETIME('now', '-3 days'), 'argent', 0, 0, 0, 0, 1, 1, 'Perdu', 'Difficile', 1)
""")

cursor.execute("""
    INSERT INTO Partie (Date_Du_Jeu, Mot_A_Deviner, Gagne_Facile, Perdu_Facile, Gagne_Moyen, Perdu_Moyen,
                       Gagne_Difficile, Perdu_Difficile, Resultat, Difficulty, User_Id)
    VALUES (DATETIME('now', '-2 days'), 'minuscule', 1, 0, 0, 0, 1, 0, 'Gagné', 'Difficile', 1)
""")

cursor.execute("""
    INSERT INTO Partie (Date_Du_Jeu, Mot_A_Deviner, Gagne_Facile, Perdu_Facile, Gagne_Moyen, Perdu_Moyen,
                       Gagne_Difficile, Perdu_Difficile, Resultat, Difficulty, User_Id)
    VALUES (DATETIME('now', '-1 day'), 'index', 1, 0, 0, 0, 0, 0, 'Gagné', 'Facile', 1)
""")

cursor.execute("""
    INSERT INTO Partie (Date_Du_Jeu, Mot_A_Deviner, Gagne_Facile, Perdu_Facile, Gagne_Moyen, Perdu_Moyen,
                       Gagne_Difficile, Perdu_Difficile, Resultat, Difficulty, User_Id)
    VALUES (DATETIME('now'), 'sortir', 0, 0, 1, 0, 0, 1, 'Perdu', 'Moyen', 1)
""")

connection.commit()
connection.close()
