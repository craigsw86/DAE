# HIPAA Checklist Project Documentation

## Project Overview
The HIPAA Checklist project is a secure, full-stack web application for managing HIPAA compliance checklists and regulation updates. It features a Django backend, React frontend, JWT authentication, encrypted data storage, and comprehensive audit logging.

## Getting Started
### Prerequisites
- Python 3.8+
- Node.js 16+
- SQLite (default) or PostgreSQL
- VS Code or your preferred editor
- Git

### Setup Process
1. **Clone the repository**
2. **Backend:**
   - Install dependencies: `pip install -r requirements.txt`
   - Run migrations: `python manage.py migrate`
   - Create a superuser: `python manage.py createsuperuser`
   - Start the server: `python manage.py runserver`
3. **Frontend:**
   - Navigate to `frontend/`
   - Install dependencies: `npm install`
   - Start the React app: `npm start`

## Directory Structure
```
project_root/
├── backend/                # Django backend
│   ├── checklist/          # Main app (models, views, admin, tests)
│   ├── hipaa_checklist/    # Project settings
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/                # React source code
│   ├── public/             # Static files
│   └── package.json        # JS dependencies
├── docs/                   # Documentation
│   ├── API.md
│   ├── API_Testing_Postman.md
│   ├── Security_Architecture.md
│   ├── Security_Policy.md
│   ├── Security_Playbooks.md
│   ├── Incident_Response_Plan.md
│   └── ...
└── README.md               # This file
```

## Security & Compliance Summary
- **Data Protection:** Encrypted fields for sensitive data, HTTPS enforced via Nginx and Django settings.
- **Authentication:** JWT for all API endpoints, MFA for admin accounts.
- **Audit Logging:** All changes tracked with django-auditlog and Wazuh agent.
- **Incident Response:** Documented playbooks and regular log review.
- **Compliance:** Aligns with HIPAA Security Rule and NIST CSF.

## Policies & Documentation
- [API.md](API.md): API reference and usage
- [API_Testing_Postman.md](API_Testing_Postman.md): Postman testing guide
- [Security_Architecture.md](Security_Architecture.md): Security layers and controls
- [Security_Policy.md](Security_Policy.md): Security policy and governance
- [Security_Playbooks.md](Security_Playbooks.md): Incident response playbooks
- [Incident_Response_Plan.md](Incident_Response_Plan.md): IRP details

## Contact / Maintainers
- Project Lead: [Your Name or Team]
- Email: [your.email@example.com]
- For issues, open a GitHub issue or contact the maintainer.

---
*For more details, see the docs/ directory and referenced files above.*
