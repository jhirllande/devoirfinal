import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from employee import Employee

root = tk.Tk()
root.title("Employee Database")
root.geometry("600x400")
root.configure(background="#F4F4F4")

db = Database('employee.db')

# Styling
style = ttk.Style()
style.configure("TButton", background="#FF6B6B", foreground="#4949c6")  # Style pour les boutons
style.configure("TLabel", background="#F4F4F4", foreground="#4949c6")  # Style pour les étiquettes de texte
style.configure("TEntry", background="#FFFFFF", fieldbackground="#4949c6")  # Style pour les champs de saisie
style.configure("TText", background="#FFFFFF", foreground="#4949c6")  # Style pour les zones de texte

# Interface du formulaire de saisie
def switch_to_input_form():
    display_frame.pack_forget()
    input_frame.pack()

# ...

# Fonction pour ajouter un employé
def ajouter_employee():
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    age = age_entry.get()
    poste = poste_entry.get()

    if nom and prenom and age and poste:
        try:
            age = int(age)  # Vérifie que l'âge est un entier valide
        except ValueError:
            messagebox.showerror("Âge invalide", "Veuillez entrer un entier valide pour l'âge.")
            return
        db.ajouter_employee(nom, prenom, age, poste)
        result_label.configure(text="Informations sur l'employé enregistrées avec succès dans la base de données 'employee.db'.")
        clear_input_fields()
        switch_to_display_form()  # Rafraîchit le tableau d'affichage
    else:
        result_label.configure(text="Veuillez remplir tous les champs.", foreground="red")

# Dans la classe Database :

def clear_input_fields():
    nom_entry.delete(0, tk.END)
    prenom_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    poste_entry.delete(0, tk.END)

# Interface du formulaire d'affichage
def switch_to_display_form():
    input_frame.pack_forget()
    display_frame.pack()
    afficher_employees()

# ...

# Formulaire de saisie
input_frame = tk.Frame(root, bg="#F4F4F4")
input_label = ttk.Label(input_frame, text="Nouvel employé", font=("Helvetica", 16), background="#F4F4F4")

# ...

nom_label = ttk.Label(input_frame, text="Nom de l'employé:", background="#F4F4F4")
nom_label.pack()
nom_entry = ttk.Entry(input_frame)
nom_entry.pack()

prenom_label = ttk.Label(input_frame, text="Prénom de l'employé:", background="#F4F4F4")
prenom_label.pack()
prenom_entry = ttk.Entry(input_frame)
prenom_entry.pack()

age_label = ttk.Label(input_frame, text="Âge de l'employé:", background="#F4F4F4")
age_label.pack()
age_entry = ttk.Entry(input_frame)
age_entry.pack()

poste_label = ttk.Label(input_frame, text="Poste de l'employé:", background="#F4F4F4")
poste_label.pack()
poste_entry = ttk.Entry(input_frame)
poste_entry.pack()

ajouter_button = ttk.Button(input_frame, text="Ajouter", command=ajouter_employee, style="TButton")
ajouter_button.pack(pady=10)

switch_to_display_button = ttk.Button(input_frame, text="Afficher", command=switch_to_display_form, style="TButton")
switch_to_display_button.pack()

# ...

# Formulaire d'affichage
display_frame = tk.Frame(root, bg="#F4F4F4")

# ...

switch_to_input_button = ttk.Button(display_frame, text="Retour", command=switch_to_input_form, style="TButton")
switch_to_input_button.pack(pady=10)

# Autres fonctions
def on_quit():
    db.fermer_connexion()
    root.destroy()

# Bouton Quitter
quit_button = ttk.Button(root, text="Quitter", command=on_quit, style="TButton")
quit_button.pack(pady=10)

# Lancement du programme
switch_to_input_form()
root.mainloop()

print("Fin du programme.")
