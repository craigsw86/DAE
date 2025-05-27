"""
gui_app.py

Graphical user interface for the Clinic File Reminder App.

This GUI allows users to:
- View active and inactive patients in tabs
- Run a reminder check to determine which files should be shredded
- Add new patient records to the database
"""

import tkinter as tk
from tkinter import messagebox, ttk
from db import connect_db
from shredder import check_shredding_reminders
from datetime import date
import os

root = tk.Tk()
root.title("Clinic Patient Manager")
root.geometry("600x400")

def run_reminder_check():
    """
    Runs the shredding reminder logic and displays results.

    Calls the check_shredding_reminders function from shredder.py,
    updates the database as needed, and shows a popup with reminder messages.
    """
    reminders = check_shredding_reminders()

    # 🔁 Refresh both patient tabs
    load_patients(1, active_listbox)
    load_patients(0, inactive_listbox)

    if reminders:
        messagebox.showinfo("Reminders", "\n".join(reminders))
    else:
        messagebox.showinfo("Reminders", "No files need to be shredded today.")

reminder_button = tk.Button(root, text="Run Reminder Check", command=run_reminder_check)
reminder_button.pack(pady=10)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create frames for each tab
active_tab = ttk.Frame(notebook)
inactive_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(active_tab, text="🟢 Active Patients")
notebook.add(inactive_tab, text="🔴 Inactive Patients")

def load_patients(active_value, listbox):
    """
    Loads patients from the database into the given listbox.

    Parameters:
    - active_value (int): 1 for active patients, 0 for inactive
    - listbox (tk.Listbox): The listbox to populate with patient names
    """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name FROM patients WHERE is_active = ?", (active_value,))
    rows = cursor.fetchall()
    listbox.delete(0, tk.END) # Clear previous entries
    for row in rows:
        listbox.insert(tk.END, f"{row[0]} {row[1]}")
    conn.close()

# Listbox for Active Patients
active_listbox = tk.Listbox(active_tab)
active_listbox.pack(expand=True, fill="both", padx=10, pady=10)

# Listbox for Inactive Patients
inactive_listbox = tk.Listbox(inactive_tab)
inactive_listbox.pack(expand=True, fill="both", padx=10, pady=10)

# Load data into both
load_patients(1, active_listbox)    # 1 = Active, or is_active
load_patients(0, inactive_listbox)  # 0 = Inactive, or not active

# This is the "Add Patient" form

form_frame = tk.Frame(root)
form_frame.pack(pady=10)

tk.Label(form_frame, text="First Name").grid(row=0, column=0, padx=5, pady=2, sticky='e')
first_name_entry = tk.Entry(form_frame)
first_name_entry.grid(row=0, column=1)

tk.Label(form_frame, text="Last Name").grid(row=1, column=0, padx=5, pady=2, sticky='e')
last_name_entry = tk.Entry(form_frame)
last_name_entry.grid(row=1, column=1)

tk.Label(form_frame, text="Last Visit (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=2, sticky='e')
last_visit_entry = tk.Entry(form_frame)
last_visit_entry.grid(row=2, column=1)

tk.Label(form_frame, text="Death Date (YYYY-MM-DD or blank)").grid(row=3, column=0, padx=5, pady=2, sticky='e')
death_date_entry = tk.Entry(form_frame)
death_date_entry.grid(row=3, column=1)

submit_button = tk.Button(form_frame, text="Add Patient", command=lambda: add_patient())
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

def add_patient():
    """
    Adds a new patient to the database based on form input.
    """
    first = first_name_entry.get().strip()
    last = last_name_entry.get().strip()
    visit = last_visit_entry.get().strip()
    death =  death_date_entry.get().strip() or None

    if not (first and last and visit):
        messagebox.showerror("Error", "First Name, Last Name, and Last Visit are required.")
        return
    
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients (first_name, last_name, last_visit, death_date, is_active) VALUES (?, ?, ?, ?, 1)",
            (first, last, visit, death)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Patient {first} {last} added.")
        load_patients(1, active_listbox)    # Refresh Active tab
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        last_visit_entry.delete(0, tk.END)
        death_date_entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

root.mainloop()