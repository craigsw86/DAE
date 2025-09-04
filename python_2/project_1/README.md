# 🏥 Clinic File Reminder App

> A desktop app to remind staff when to shred **physical** patient files based on retention rules.  
> ⚠️ *This does NOT delete digital records.*

---

## 📌 Features

- View 🟢 Active and 🔴 Inactive patient records
- Add new patients via a form or CSV
- Run a **Reminder Check** that:
  - Moves patients to Inactive if:
    - 💀 3+ years since death, or
    - ⏳ 7+ years since last visit
  - Generates `reminders_YYYYMMDD.txt` telling staff which paper files to shred
- Daily check script (`midnight_check.py`)
- GUI made with `tkinter`
- SQLite database backend (`clinic.db`)
- Comes with test data + CSV template

---

## 🧠 How It Works

### Reminder Logic:
1. **Deceased Patients**: If death was 3+ years ago → move to Inactive + add to shred reminders  
2. **Living Patients**: If last visit was 7+ years ago → move to Inactive + add to reminders  
3. Saves updates in the database + generates a `reminders_*.txt` file

📄 Algorithm reference: see flowchart in `Patient_File_Management_with_Stickies.pdf`

---

## 📂 Project Structure

| File | Description |
|------|-------------|
| `gui_app.py` | Main GUI window with tabs and buttons |
| `shredder.py` | Contains logic to determine shred reminders |
| `midnight_check.py` | Script for daily reminder generation |
| `db.py` | Connects to SQLite (`clinic.db`) |
| `config.py` | Stores global constants (e.g., file paths) |
| `setup_db.py` | Creates database schema |
| `send_reminder_alert.py` | Placeholder for email/text alerts |
| `seed_fake_patients.py` | Loads test patient data |
| `seed_hardcoded.py` | Loads a few hardcoded patients |
| `test_insert_patient.py` | Test script for inserting records |
| `view_patients.py` | CLI display of Active/Inactive tabs |
| `clinic.db` | The SQLite database (auto-generated) |
| `patient_template.csv` | Template for adding patients via CSV |
| `fake_patients.csv` | Sample dataset |
| `reminders_YYYYMMDD.txt` | Shred reminder file (auto-created) |

---

## 🛠 How to Run

### 1. Install Python (3.8+)
Make sure you have Python installed.

### 2. Setup Database (first time only)
```bash
python3 setup_db.py
