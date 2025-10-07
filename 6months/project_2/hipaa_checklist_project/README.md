# HIPAA Checklist Project

##  Welcome to the HIPAA Compliance Management System!

A comprehensive, full-stack web application designed to help healthcare organizations manage HIPAA compliance through an intuitive checklist system. Features Django backend, React frontend, JWT authentication, encrypted data storage, and comprehensive security features.

##  Quick Start for Visitors

**New to this project? Start here:**
- **[VISITOR_INSTRUCTIONS.md](VISITOR_INSTRUCTIONS.md)** - Complete visitor guide
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Get started in 5 minutes
- **One-click demo**: Run `run-hipaa-project.bat` and choose options 1 & 2

## Features
- User authentication (JWT)
- Checklist management (with mitigation steps)
- Regulation updates
- Compliance reporting
- Audit log (viewable in admin and frontend)
- Security dashboard with vulnerability scanning
- Role-based access control
- Data encryption and security features

## Deployment

### Backend
1. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```
2. Run migrations:
   ```
   python backend/manage.py makemigrations
   python backend/manage.py migrate
   ```
3. Create a superuser:
   ```
   python backend/manage.py createsuperuser
   ```
4. Start the server:
   ```
   python backend/manage.py runserver
   ```

### Frontend
1. Install dependencies:
   ```
   cd frontend
   npm install
   ```
2. Create a `.env` file in `frontend/`:
   ```
   REACT_APP_API_BASE_URL=http://localhost:8000
   ```
3. Start the React app:
   ```
   npm start
   ```

##  Documentation

### For Visitors
- **[VISITOR_INSTRUCTIONS.md](VISITOR_INSTRUCTIONS.md)** - Complete visitor guide with demo scenarios
- **[QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)** - Quick 5-minute start guide
- **[USER_MANUAL.md](USER_MANUAL.md)** - Detailed user manual

### For Developers
- **[SETUP_AND_INSTALLATION_GUIDE.md](SETUP_AND_INSTALLATION_GUIDE.md)** - Technical setup guide
- **[docs/API.md](docs/API.md)** - API documentation
- **[docs/Risk_Communication.md](docs/Risk_Communication.md)** - Risk communication
- **[docs/](docs/)** - Complete technical documentation

### Demo Scripts
- **`run-hipaa-project.bat`** - One-click demo launcher
- **`start_demo_servers.ps1`** - PowerShell demo script
- **`class_demo.bat`** - Class demonstration script


