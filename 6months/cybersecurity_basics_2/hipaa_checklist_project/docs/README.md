# HIPAA Checklist Project

## Manual Updates Process
1. Sign up for HHS OCR Privacy & Security Listserv: Visit https://www.hhs.gov/hipaa/for-professionals/list-serve/index.html, provide email, and confirm subscription. Receive emails on HIPAA privacy/security updates, guidance, and changes.
2. Optionally, sign up for HHS Weekly News Digest: Visit https://cloud.connect.hhs.gov/subscriptioncenter, select options, and subscribe for weekly summaries including health regulations.
3. When receiving an email update: Log in as admin[](http://localhost:8000/admin/), add new RegulationUpdate with details (title, description, source_url, pub_date).
4. Users will see in-app alerts for recently added items.

## Setup
1. Clone repo.
2. Backend: `cd backend; python manage.py migrate; python manage.py createsuperuser; python manage.py runserver`.
3. Frontend: `cd frontend; npm install; npm start`.

## Cybersecurity Risks and Mitigations
- Risk: Delayed updates from manual entry. Mitigation: Encourage regular email checks; use Wazuh to monitor admin logins/additions for governance oversight (NIST CM-3).
- Risk: SQL injection vulnerabilities in raw SQL queries compromise data security. Mitigation: Use parameterized queries for all raw SQL operations to prevent injection attacks, leverage Django’s ORM for standard CRUD tasks to minimize raw SQL usage, and conduct regular security audits using tools like OWASP ZAP to identify and fix vulnerabilities.
- Risk: Failure to meet HIPAA compliance requirements due to improper handling of protected health information (PHI) in a local environment. Mitigation: Encrypt PHI (e.g., notes field) using django-encrypted-model-fields, enforce HTTPS with self-signed certificates (or trusted certs for production), implement physical security for the local server (e.g., firewalls, locked access), and use audit logging with django-auditlog to track all data access and changes, verified through a local compliance audit.
- Risk: Limited developer experience with React.js delays front-end development. Mitigation: Utilize Material-UI’s pre-built components to accelerate UI development, provide developers with targeted React training resources (e.g., freeCodeCamp tutorials), and prioritize a minimal viable product (MVP) with a core checklist and reporting features to meet deadlines, with iterative enhancements planned post-launch.

## Evaluation
- Functionality: The app displays HIPAA regulations, allows users to mark items as completed, add encrypted notes, and view accurate compliance reports, verified through end-to-end testing.
- HIPAA Compliance: All sensitive data (e.g., notes) is encrypted, access is restricted via JWT authentication, audit logs capture all changes, and the local setup includes physical security measures (e.g., firewalls), confirmed by a security audit.
- Usability: The React.js interface is responsive, intuitive, and accessible on desktops and tablets, with in-app alerts for updates, achieving a user satisfaction score of at least 80% in stakeholder feedback.
- Update Reliability: Manual additions from HHS emails are integrated accurately during testing.