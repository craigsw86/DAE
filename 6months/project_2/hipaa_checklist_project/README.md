# HIPAA Checklist Web Application

## Overview
This project is a secure, web-based HIPAA compliance checklist to help healthcare professionals track regulations from the HHS Office for Civil Rights (OCR). It uses Django for the backend, React for the frontend, and SQLite for local development, with a focus on HIPAA-compliant security practices.

## Week 1 Setup (July 7–17, 2025)
### Day 1: Environment Setup
- Installed Python 3.8+, Node.js 16+, SQLite, VS Code, and Git.
- Initialized Git repository and connected to GitHub.
- Created `frontend/src/main.js` with variables (`complianceScore: int`, `regulationName: string`).

### Day 2: Django Project Creation
- Created Django project (`hipaa_checklist`) and app (`checklist`).
- Configured SQLite in `settings.py` with secure `SECRET_KEY`.
- Installed dependencies via `requirements.txt`.
- Updated `main.js` with math operations and if/else logic.

### Day 3: JavaScript/React Basics
- Explored JavaScript variables, functions, and DOM manipulation.
- Set up React app with Create React App in `frontend/`.
- Connected `main.js` to `App.js` for interactive output (console/DOM).

### Day 4: Database Schema and Cybersecurity
- Created initial Django models and migrations for SQLite.
- Documented setup in `docs/README.md` and cybersecurity policies in `docs/Policies.docx`.
- Discussed risks (e.g., data breaches) and mitigations (e.g., firewalls, encryption).

## Setup Instructions
1. **Clone Repository**:
   git clone <repository-url>
   cd hipaa_checklist


Backend Setup:
Install Python 3.8+ and pip.
Create virtual environment:python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install dependencies:pip install -r backend/requirements.txt


Run migrations:cd backend
python manage.py migrate


Create superuser:python manage.py createsuperuser


Start server:python manage.py runserver




Frontend Setup:
Install Node.js 16+.
Install dependencies:cd frontend
npm install


Start React app:npm start




Access Application:
Backend: http://localhost:8000
Frontend: http://localhost:3000
Django Admin: http://localhost:8000/admin



Cybersecurity Notes

Risks: Data breaches, SQL injection.
Mitigations: Firewalls, encrypted fields (planned), parameterized queries.
Policies: Drafted in docs/Policies.docx (access control, data protection, system use).


