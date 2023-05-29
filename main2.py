import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# Classe Database
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS emplois (id INTEGER PRIMARY KEY AUTOINCREMENT, titreEmploi TEXT, entreprise TEXT, description TEXT, localisation TEXT, salaire REAL)")

    def ajouter_emploi(self, titreEmploi, entreprise, description, localisation, salaire):
        self.cursor.execute(
            "INSERT INTO emplois (titreEmploi, entreprise, description, localisation, salaire) VALUES (?, ?, ?, ?, ?)",
            (titreEmploi, entreprise, description, localisation, salaire))
        self.conn.commit()

    def recuperer_emplois(self):
        self.cursor.execute("SELECT * FROM emplois")
        rows = self.cursor.fetchall()
        emplois = []
        for row in rows:
            emplois.append({
                "id": row[0],
                "titreEmploi": row[1],
                "entreprise": row[2],
                "description": row[3],
                "localisation": row[4],
                "salaire": row[5]
            })
        return emplois

    def fermer_connexion(self):
        self.cursor.close()
        self.conn.close()


# Interface graphique
root = tk.Tk()
root.title("employerDatabase")
root.geometry("600x400")
root.configure(background="#F4F4F4")

db = Database('employer.db')

# Style
style = ttk.Style()
style.configure("TButton", background="#FF6B6B", foreground="#4949c6")
style.configure("TLabel", background="#F4F4F4", foreground="#4949c6")
style.configure("TEntry", background="#FFFFFF", fieldbackground="#4949c6")
style.configure("TText", background="#FFFFFF", foreground="#4949c6")


# Interface du formulaire de saisie
def switch_to_input_form():
    display_frame.pack_forget()
    input_frame.pack()


def ajouter_emploi():
    titreEmploi = titreEmploi_entry.get()
    entreprise = entreprise_entry.get()
    description = description_entry.get()
    localisation = localisation_entry.get()
    salaire = salaire_entry.get()

    if titreEmploi and entreprise and description and localisation and salaire:
        try:
            salaire = float(salaire)  # Vérifie que salaire est un nombre flottant valide
        except ValueError:
            messagebox.showerror("Salaire invalide", "Veuillez entrer un nombre valide pour le salaire.")
            return
        db.ajouter_emploi(titreEmploi, entreprise, description, localisation, salaire)
        result_label.configure(text="L'emploi a été enregistré avec succès dans la base de données 'jobs.db'.")
        clear_input_fields()
        switch_to_display_form()  # Rafraîchit le tableau d'affichage
    else:
        result_label.configure(text="Veuillez remplir tous les champs.", foreground="red")


def clear_input_fields():
    titreEmploi_entry.delete(0, tk.END)
    entreprise_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    localisation_entry.delete(0, tk.END)
    salaire_entry.delete(0, tk.END)


# Interface du formulaire d'affichage
def switch_to_display_form():
    input_frame.pack_forget()
    display_frame.pack()
    afficher_emplois()


def afficher_emplois():
    emplois = db.recuperer_emplois()

    for row in table.get_children():
        table.delete(row)

    for emploi in emplois:
        table.insert("", "end", values=(
        emploi["id"], emploi["titreEmploi"], emploi["entreprise"], emploi["description"], emploi["localisation"],
        emploi["salaire"]))

    result_label.configure(text="Les emplois ont été récupérés avec succès depuis la base de données 'employer.db'.")


# Formulaire de saisie
input_frame = tk.Frame(root, bg="#F4F4F4")
input_label = ttk.Label(input_frame, text="Nouvel Emploi", font=("Helvetica", 16), background="#F4F4F4")
result_label = ttk.Label(input_frame, text="", background="#F4F4F4")

titreEmploi_label = ttk.Label(input_frame, text="Titre de l'emploi:", background="#F4F4F4")
titreEmploi_entry = ttk.Entry(input_frame)

entreprise_label = ttk.Label(input_frame, text="Entreprise:", background="#F4F4F4")
entreprise_entry = ttk.Entry(input_frame)

description_label = ttk.Label(input_frame, text="Description:", background="#F4F4F4")
description_entry = ttk.Entry(input_frame)

localisation_label = ttk.Label(input_frame, text="Localisation:", background="#F4F4F4")
localisation_entry = ttk.Entry(input_frame)

salaire_label = ttk.Label(input_frame, text="Salaire:", background="#F4F4F4")
salaire_entry = ttk.Entry(input_frame)

ajouter_button = ttk.Button(input_frame, text="Ajouter", command=ajouter_emploi)
switch_to_display_button = ttk.Button(input_frame, text="Afficher", command=switch_to_display_form)

# Utilisation de grid pour positionner les widgets horizontalement
input_label.grid(row=0, column=0, columnspan=4, pady=5)
result_label.grid(row=1, column=0, columnspan=4)

titreEmploi_label.grid(row=2, column=0)
titreEmploi_entry.grid(row=2, column=1)

entreprise_label.grid(row=2, column=2)
entreprise_entry.grid(row=2, column=3)

description_label.grid(row=3, column=0)
description_entry.grid(row=3, column=1)

localisation_label.grid(row=3, column=2)
localisation_entry.grid(row=3, column=3)

salaire_label.grid(row=4, column=0)
salaire_entry.grid(row=4, column=1)

ajouter_button.grid(row=5, column=0, columnspan=2, pady=10)
switch_to_display_button.grid(row=5, column=2, columnspan=2)

# Formulaire d'affichage
display_frame = tk.Frame(root, bg="#F4F4F4")

display_label = ttk.Label(display_frame, text="Emplois enregistrés", font=("Helvetica", 16), background="#F4F4F4")
display_label.pack(pady=10)

table_frame = ttk.Frame(display_frame)
table = ttk.Treeview(table_frame,
                     columns=("ID", "Titre d'emploi", "Entreprise", "Description", "Localisation", "Salaire"),
                     show="headings")
table.heading("ID", text="ID")
table.heading("Titre d'emploi", text="Titre d'emploi")
table.heading("Entreprise", text="Entreprise")
table.heading("Description", text="Description")
table.heading("Localisation", text="Localisation")
table.heading("Salaire", text="Salaire")

table.column("ID", width=20)
table.column("Titre d'emploi", width=150)
table.column("Entreprise", width=150)
table.column("Description", width=150)
table.column("Localisation", width=150)
table.column("Salaire", width=80)

table.tag_configure("oddrow", background="#E8E8E8")
table.tag_configure("evenrow", background="#FFFFFF")

table.pack(padx=10, pady=10)
table_frame.pack(padx=10, pady=5)

switch_to_input_button = ttk.Button(display_frame, text="Retour", command=switch_to_input_form)
switch_to_input_button.pack(pady=10)


# Autres fonctions
def on_quit():
    db.fermer_connexion()
    root.destroy()


# Bouton Quitter
quit_button = ttk.Button(root, text="Quitter", command=on_quit)
quit_button.pack(pady=10)

# Lancement du programme
switch_to_input_form()
root.mainloop()

print("Fin du programme.")
