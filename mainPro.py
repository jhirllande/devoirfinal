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
style.configure("TButton", background="#FF6B6B", foreground="#4949c6")
style.configure("TLabel", background="#F4F4F4", foreground="#4949c6")
style.configure("TEntry", background="#FFFFFF", fieldbackground="#4949c6")
style.configure("TText", background="#FFFFFF", foreground="#4949c6")

# Input Form Interface
def switch_to_input_form():
    display_frame.pack_forget()
    input_frame.pack()

def ajouter_employee():
    nom = nom_entry.get()
    prenom = prenom_entry.get()
    age = age_entry.get()
    poste = poste_entry.get()

    if nom and prenom and age and poste:
        try:
            age = int(age)  # Make sure age is a valid integer
        except ValueError:
            messagebox.showerror("Invalid Age", "Please enter a valid integer for age.")
            return
        db.ajouter_employee(nom, prenom, age, poste)
        result_label.configure(text="Employee information successfully saved in the 'employee.db' database.")
        clear_input_fields()
        switch_to_display_form()  # Refresh the display table
    else:
        result_label.configure(text="Please fill in all the fields.", foreground="red")

# In the Database class:
def clear_input_fields():
    nom_entry.delete(0, tk.END)
    prenom_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    poste_entry.delete(0, tk.END)

# Display Form Interface
def switch_to_display_form():
    input_frame.pack_forget()
    display_frame.pack()
    afficher_employees()

def afficher_employees():
    employees = db.recuperer_employees()

    for row in table.get_children():
        table.delete(row)

    for employee in employees:
        table.insert("", "end", values=(employee.id, employee.nom, employee.prenom, employee.age, employee.poste))

    result_label.configure(text="Employee information successfully retrieved from the 'employee.db' database.")

# Input Form
input_frame = tk.Frame(root, bg="#F4F4F4")
input_label = ttk.Label(input_frame, text="New Employee", font=("Helvetica", 16), background="#F4F4F4")

input_label.pack(pady=5)
result_label = ttk.Label(input_frame, text="", background="#F4F4F4")
result_label.pack()

nom_label = ttk.Label(input_frame, text="Employee Name:", background="#F4F4F4")
nom_label.pack()
nom_entry = ttk.Entry(input_frame)
nom_entry.pack()

prenom_label = ttk.Label(input_frame, text="Employee First Name:", background="#F4F4F4")
prenom_label.pack()
prenom_entry = ttk.Entry(input_frame)
prenom_entry.pack()

age_label = ttk.Label(input_frame, text="Employee Age:", background="#F4F4F4")
age_label.pack()
age_entry = ttk.Entry(input_frame)
age_entry.pack()

poste_label = ttk.Label(input_frame, text="Employee Position:", background="#F4F4F4")
poste_label.pack()
poste_entry = ttk.Entry(input_frame)
poste_entry.pack()

ajouter_button = ttk.Button(input_frame, text="Add", command=ajouter_employee, style="TButton")
ajouter_button.pack(pady=10)

switch_to_display_button = ttk.Button(input_frame, text="Display", command=switch_to_display_form, style="TButton")
switch_to_display_button.pack()

# Display Form
display_frame = tk.Frame(root, bg="#F4F4F4")

display_label = ttk.Label(display_frame, text="Registered Employees", font=("Helvetica", 16), background="#F4F4F4")
display_label.pack(pady=10)

table_frame = ttk.Frame(display_frame)
table = ttk.Treeview(table_frame, columns=("ID", "Name", "First Name", "Age", "Position"), show="headings")
table.heading("ID", text="ID")
table.heading("Name", text="Name")
table.heading("First Name", text="First Name")
table.heading("Age", text="Age")
table.heading("Position", text="Position")

table.column("ID", width=20)
table.column("Name", width=150)
table.column("First Name", width=150)
table.column("Age", width=80)
table.column("Position", width=150)

table.tag_configure("oddrow", background="#E8E8E8")
table.tag_configure("evenrow", background="#FFFFFF")

table.pack(padx=10, pady=10)
table_frame.pack(padx=10, pady=5)

switch_to_input_button = ttk.Button(display_frame, text="Back", command=switch_to_input_form, style="TButton")
switch_to_input_button.pack(pady=10)

# Other Functions
def on_quit():
    db.fermer_connexion()
    root.destroy()

# Quit Button
quit_button = ttk.Button(root, text="Quit", command=on_quit, style="TButton")
quit_button.pack(pady=10)

# Start the program
switch_to_input_form()
root.mainloop()

print("Program end.")
