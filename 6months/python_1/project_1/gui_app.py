"""
gui_app.py

Graphical user interface for the Clinic File Reminder App.

This GUI allows users to:
- View active and inactive patients in tabs
- Run a reminder check to determine which files should be shredded
- Add new patient records to the database
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from db import connect_db
from shredder import check_shredding_reminders
from datetime import date, datetime
import os
from midnight_check import run_nightly_reminder_check
import csv


root = tk.Tk()
root.title("Clinic Patient Manager")
root.geometry("600x600")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
# Fixed the size of the GUI display

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

def handle_reminder_check():
    try:
        count = run_nightly_reminder_check()
        if count > 0:
            messagebox.showinfo("Reminder Check Complete", f"✅ {count} reminders written to file.")
        else:
            messagebox.showinfo("Reminder Check Complete", "✅ No patients matched shredding criteria today.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to run reminder check:\n{e}")

reminder_button = tk.Button(root, text="Run Reminder Check", command=handle_reminder_check)
reminder_button.grid(pady=10)

notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Create frames for each tab
active_tab = ttk.Frame(notebook)
inactive_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(active_tab, text="🟢 Active Patients")
notebook.add(inactive_tab, text="🔴 Inactive Patients")
active_tab.rowconfigure(0, weight=1)
active_tab.columnconfigure(0, weight=1)
inactive_tab.rowconfigure(0, weight=1)
inactive_tab.columnconfigure(0, weight=1)

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
active_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Listbox for Inactive Patients
inactive_listbox = tk.Listbox(inactive_tab)
inactive_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Load data into both
load_patients(1, active_listbox)    # 1 = Active, or is_active
load_patients(0, inactive_listbox)  # 0 = Inactive, or not active

# This is the "Add Patient" form

form_frame = tk.Frame(root)
form_frame.grid(row=2, column=0, columnspan=2, pady=10)

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

# === CSV Upload and Template Buttons ===
csv_frame = tk.Frame(root)
csv_frame.grid(row=3, column=0, columnspan=2, pady=10) # Below the form rows

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
    
    # ✅ Validate date formats (YYYY-MM-DD)
    try:
        datetime.strptime(visit, "%Y-%m-%d")
        if death:
            datetime.strptime(death, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date Format", "Please enter dates in YYYY-MM-DD format.")
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

def upload_csv():
    """
    Allows the user to select and upload a CSV file of patients.
    """
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    inserted = 0
    skipped = 0

    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    first = row["first_name"].strip()
                    last = row["last_name"].strip()
                    visit = row["last_visit"].strip()
                    death = row.get("death_date", "").strip() or None

                    if not (first and last and visit):
                        skipped += 1
                        continue

                    datetime.strptime(visit, "%Y-%m-%d")
                    if death:
                        datetime.strptime(death, "%Y-%m-%d")

                    conn = connect_db()
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO patients (first_name, last_name, last_visit, death_date, is_active) VALUES (?, ?, ?, ?, 1)",
                        (first, last, visit, death)
                    )
                    conn.commit()
                    conn.close()
                    inserted += 1
                except Exception as e:
                    print(f"⚠️ Skipped row due to error: {e}")
                    skipped += 1

        messagebox.showinfo("CSV Upload Complete", f"✅ Imported {inserted} patients.\n❌ Skipped {skipped} rows.")
        load_patients(1, active_listbox)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV:\n{e}")                   

def download_csv_template():
    """
    Creates a CSV template file for patient data if it doesn't already exist.
    """
    template_path = "patient_template.csv"

    if not os.path.exists(template_path):
        try:
            with open(template_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["first_name", "last_name", "last_visit", "death_date"])
                writer.writerow(["Alice", "Example", "2016-04-10", "2019-03-01"])  # Sample row

            messagebox.showinfo("Template Created", f"✅ Template saved as {template_path}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Could not create template:\n{e}")
    else:
        messagebox.showinfo("Template Exists", f"📄 Template already exists at {template_path}")

def show_welcome_message():
    messagebox.showinfo(
        "Welcome to Clinic File Reminder App",
        "This app helps you track which patient files are ready to be shredded:\n\n"
        "🟢 3 years since death\n🟢 7 years since last visit\n\n"
        "Use the tabs, add patients, or upload CSVs to get started!"
    )

upload_button = tk.Button(csv_frame, text="Upload Patient CSV", command=upload_csv)
upload_button.grid(row=0, column=0, pady=4)

template_button = tk.Button(csv_frame, text="Download CSV Template", command=download_csv_template)
template_button.grid(row=1, column=0, pady=4)

show_welcome_message()
root.mainloop()