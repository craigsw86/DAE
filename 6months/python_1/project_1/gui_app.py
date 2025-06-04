import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from db import connect_db
from shredder import check_shredding_reminders
from datetime import date, datetime
import os
from midnight_check import run_nightly_reminder_check
import csv
import config

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.showtip()

    def leave(self, event=None):
        self.hidetip()

    def showtip(self):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "16", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

def load_patients(tree, status):
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, first_name, last_name, last_visit, death_date FROM patients WHERE is_active = ?", (status,))
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

root = tk.Tk()
root.title("Clinic Patient Manager")
root.geometry("600x600")
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)


notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

active_tab = ttk.Frame(notebook)
inactive_tab = ttk.Frame(notebook)
notebook.add(active_tab, text="🟢 Active Patients")
notebook.add(inactive_tab, text="🔴 Inactive Patients")

active_tab.rowconfigure(0, weight=1)
active_tab.columnconfigure(0, weight=1)
inactive_tab.rowconfigure(0, weight=1)
inactive_tab.columnconfigure(0, weight=1)

active_listbox = tk.Listbox(active_tab)
active_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

inactive_listbox = tk.Listbox(inactive_tab)
inactive_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


form_frame = tk.Frame(root)
form_frame.grid(row=2, column=0, columnspan=2, pady=10)

first_name_entry = tk.Entry(form_frame)
last_name_entry = tk.Entry(form_frame)
last_visit_entry = tk.Entry(form_frame)
death_date_entry = tk.Entry(form_frame)

labels = ["First Name", "Last Name", "Last Visit (YYYY-MM-DD)", "Death Date (YYYY-MM-DD or blank)"]
entries = [first_name_entry, last_name_entry, last_visit_entry, death_date_entry]

tooltips = [
    "Enter the patient's first name",
    "Enter the patient's last name",
    "Enter date of last visit (YYYY-MM-DD)",
    "Optional: Enter death date (YYYY-MM-DD) or leave blank"
]

for i, (label, entry, tip) in enumerate(zip(labels, entries, tooltips)):
    tk.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky='e')
    entry.grid(row=i, column=1)
    CreateToolTip(entry, tip)

submit_button = tk.Button(form_frame, text="Add Patient", command=lambda: add_patient())
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

csv_frame = tk.Frame(root)
csv_frame.grid(row=3, column=0, columnspan=2, pady=10)


def run_reminder_check():
    reminders = check_shredding_reminders()
    load_patients(1, active_listbox)
    load_patients(0, inactive_listbox)
    if reminders:
        messagebox.showinfo("Reminders", "\n".join(reminders))
    else:
        messagebox.showinfo("Reminders", "No files need to be shredded today.")


def choose_output_folder():
    folder = filedialog.askdirectory(title="Select Folder to Save Reminder Files")
    if folder:
        config.output_directory = folder
        messagebox.showinfo("Folder Selected", f"✅ Reminder files will be saved to:\n{folder}")


def handle_reminder_check():
    try:
        result = run_nightly_reminder_check()
        load_patients(1, active_listbox)
        load_patients(0, inactive_listbox)
        if isinstance(result, tuple) and len(result) == 2:
            count, filepath = result
            messagebox.showinfo("Reminder Check Complete", f"✅ {count} reminders written to:\n{filepath}")
        elif result == 0:
            messagebox.showinfo("Reminder Check Complete", "✅ No patients matched shredding criteria today.")
        else:
            messagebox.showwarning("Reminder Check", "Reminder check returned unexpected result.")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Failed to run reminder check:\n{e}")


def add_patient():
    first = first_name_entry.get().strip()
    last = last_name_entry.get().strip()
    visit = last_visit_entry.get().strip()
    death = death_date_entry.get().strip() or None

    if not (first and last and visit):
        messagebox.showerror("Error", "First Name, Last Name, and Last Visit are required.")
        return

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
        load_patients(1, active_listbox)
        for entry in entries:
            entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))


def upload_csv():
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
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
    template_path = "patient_template.csv"
    if not os.path.exists(template_path):
        try:
            with open(template_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["first_name", "last_name", "last_visit", "death_date"])
                writer.writerow(["Alice", "Example", "2016-04-10", "2019-03-01"])
            messagebox.showinfo("Template Created", f"✅ Template saved as {template_path}")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Could not create template:\n{e}")
    else:
        messagebox.showinfo("Template Exists", f"📄 Template already exists at {template_path}")


def show_patient_details(event, active_value):
    widget = event.widget
    index = widget.curselection()
    if not index:
        return
    first, last = widget.get(index[0]).split(" ", 1)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, first_name, last_name, last_visit, death_date, is_active FROM patients WHERE first_name = ? AND last_name = ? AND is_active = ?",
        (first, last, active_value)
    )
    patient = cursor.fetchone()
    conn.close()
    if patient:
        pid, fname, lname, visit, death, is_active = patient
        status = "Active" if is_active else "Inactive"
        messagebox.showinfo("Patient Details", f"ID: {pid}\nName: {fname} {lname}\nLast Visit: {visit or '-'}\nDeath Date: {death or '-'}\nStatus: {status}")


def load_patients(active_value, listbox):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name FROM patients WHERE is_active = ?", (active_value,))
    rows = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, f"{row[0]} {row[1]}")
    listbox.bind("<<ListboxSelect>>", lambda event, act=active_value: show_patient_details(event, act))
    conn.close()


reminder_button = tk.Button(root, text="Run Reminder Check", command=handle_reminder_check)
reminder_button.grid(pady=10)

upload_button = tk.Button(csv_frame, text="Upload Patient CSV", command=upload_csv)
upload_button.grid(row=0, column=0, pady=4)

template_button = tk.Button(csv_frame, text="Download CSV Template", command=download_csv_template)
template_button.grid(row=1, column=0, pady=4)

output_button = tk.Button(csv_frame, text="Select Output Folder", command=choose_output_folder)
output_button.grid(row=2, column=0, pady=4)

CreateToolTip(reminder_button, "Check all patients for shredding eligibility")
CreateToolTip(submit_button, "Add this patient to the database")
CreateToolTip(upload_button, "Select and upload a CSV file with patient data")
CreateToolTip(template_button, "Download a sample CSV file you can use as a template")
CreateToolTip(output_button, "Choose where reminder files are saved")


def show_welcome_message():
    messagebox.showinfo(
        "Welcome to Clinic File Reminder App",
        "This app helps you track which patient files are ready to be shredded:\n\n🟢 3 years since death\n🟢 7 years since last visit\n\nUse the tabs, add patients, or upload CSVs to get started!"
    )


show_welcome_message()
root.mainloop()
