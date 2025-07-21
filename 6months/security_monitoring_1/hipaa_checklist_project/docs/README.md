# HIPAA Checklist Project

## Setup
1. Clone repo.
2. Backend: `cd backend; python manage.py migrate; python manage.py createsuperuser; python manage.py runserver`.
3. Frontend: `cd frontend; npm install; npm start`.
4. Scrape: `python manage.py fetch_hipaa_updates`.
5. Deployment: Configure Nginx/Gunicorn; add crontab.

## Cybersecurity Risks and Mitigations
- Risk: Scraper breaks on site changes. Mitigation: Robust selectors; manual fallback; quarterly reviews (as per NIST 800-53 SI-2).
- Risk: SQL injection. Mitigation: Parameterized queries; ORM preference.
- Risk: PHI exposure. Mitigation: Encryption; HTTPS; audit logs; Wazuh monitoring.
- Risk: Dev delays. Mitigation: MVP focus; training resources.

## Evaluation
- Functionality: End-to-end tests pass.
- Compliance: Audit with OWASP ZAP; 90% update reliability.
- Usability: Responsive UI; 80%+ feedback score.