import sqlite3
from employeur import Employer

class Database:
    def __init__(self, db_name):
        self.connexion = sqlite3.connect(db_name)
        self.cursor = self.connexion.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS emplois (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT,
                entreprise TEXT,
                description TEXT,
                localisation TEXT,
                salaire REAL,
                employeur_id INTEGER,
                employeur_nom TEXT,
                employeur_prenom TEXT,
                employeur_age INTEGER,
                employeur_ville TEXT
            )
        ''')
        self.connexion.commit()

    def ajouter_emploi(self, titre, entreprise, description, localisation, salaire, employeur):
        employeur_id = employeur.id
        employeur_nom = employeur.nom
        employeur_prenom = employeur.prenom
        employeur_age = employeur.age
        employeur_ville = employeur.ville

        self.cursor.execute("""
            INSERT INTO emplois (titre, entreprise, description, localisation, salaire, employeur_id, employeur_nom, employeur_prenom, employeur_age, employeur_ville)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titre, entreprise, description, localisation, salaire, employeur_id, employeur_nom, employeur_prenom, employeur_age, employeur_ville))
        self.connexion.commit()

    def recuperer_emplois(self):
        self.cursor.execute('''
            SELECT * FROM emplois
        ''')
        rows = self.cursor.fetchall()
        emplois = []
        for row in rows:
            employeur = Employer(row[6], row[7], row[8], row[9], row[10])  # Constructing the Employer object
            emploi = {
                "id": row[0],
                "titre": row[1],
                "entreprise": row[2],
                "description": row[3],
                "localisation": row[4],
                "salaire": row[5],
                "employeur": employeur
            }
            emplois.append(emploi)
        return emplois

    def fermer_connexion(self):
        self.connexion.close()
