# Week 1 Cybersecurity Documentation

## Setup Process
- **Environment**: Installed Python 3.8+, Node.js 16+, SQLite, VS Code, Git.
- **Django**: Created project (`hipaa_checklist`) and app (`checklist`). Configured SQLite in `settings.py`.
- **React**: Set up Create React App in `frontend/`. Created `main.js` for JavaScript rubric.
- **Git**: Initialized repository and pushed to GitHub.

## Cybersecurity Risks and Mitigations
- **Risk**: Data breaches exposing PHI.
  - **Mitigation**: Encrypt sensitive fields (`notes`, `description`) using `django-encrypted-model-fields`. Plan for HTTPS via Nginx (Week 10).
- **Risk**: SQL injection in database queries.
  - **Mitigation**: Use Django ORM for CRUD operations; plan parameterized raw SQL queries (Week 4).
- **Risk**: Supply chain attacks via unverified dependencies.
  - **Mitigation**: Verified dependencies in `requirements.txt` and `package.json` using `pip list` and `npm audit`.

## Policies
- Documented in `docs/Policies.docx`: Access control, data protection, system use.
- Aligns with HIPAA Security Rule and Zero Trust (JWT planned for Week 4).
