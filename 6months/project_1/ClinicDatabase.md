# Clinic Database

## An ideal little app for reminding you when to shred old patient files!

### (NOTE: This is NOT a program to delete electronic records, but is instead a reminder app for safely disposing of physical records.)

Flowchart Notes

Change first box to START
Fix whether or not the Login is correct!
Change parallelogram to square for the PROCESS
Put “3 years since date of death” BEFORE “7 years since date of last visit”

# Clinic File Reminder App

A simple desktop application that reminds clinic staff when it's time to shred physical patient files, based on legal retention guidelines.

---

## 📋 Features

- 🟢 View **Active** and 🔴 **Inactive** patient records
- 🧾 Add new patients using a built-in form
- ⏰ Run a **reminder check** to find patients:
  - 3+ years since death
  - 7+ years since last visit
- 📤 Automatically updates the database
- 🖥️ User-friendly GUI built with `tkinter`
- 💾 Uses SQLite database (`clinic.db`)

---

## 🏥 Use Case

This tool helps clinics and offices track physical records that must be safely disposed of after a certain time — helping stay compliant without deleting digital records.

---

## 📂 File Structure

| File | Purpose |
|------|---------|
| `gui_app.py` | Main GUI application |
| `shredder.py` | Logic for reminder/shredding rules |
| `db.py` | Database connection logic |
| `clinic.db` | SQLite database (automatically created) |

---

## 🛠 How to Run

### 1. Open Terminal
Navigate to the folder where your files are stored.

```bash
cd /path/to/project_1
