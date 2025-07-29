# Security Architecture and Advanced Defense Strategies

## Zero Trust Architecture

This project applies Zero Trust principles by enforcing access controls at multiple layers:
- **Layer 1: Backend (Django) Authentication**
    All sensitive API endpoints require user authentication using JWT tokens. Only authenticated users can access or modify checklist data.
- **Layer 2: Frontend (React) Route Protection**
    The React app checks for a valid JWT token before allowing access to protected routes (e.g., checklist, compliance report). If no token is present, the user is redirected to the login page.

## Defense in Depth

The system implements at least three layers of defense:
1. **Network Layer:** The application is intended to be deployed behind a firewall and reverse proxy (e.g., Nginx) to filter unwanted traffic.
2. **Application Layer:** Django authentication and permissions restrict access to sensitive data and actions.
3. **Data Layer:** Sensitive fields in the database are encrypted at rest using `django-encrypted-model-fields`.

## Supply Chain Security

- All Python and JavaScript dependencies are regularly checked for vulnerabilities using `pip-audit` and `npm-audit`.
- **Example:**
    During development, a vulnerability was found in the `axios` package. The package was updated to the latest secure version, and the change was documented in the project changelog.

## Advanced Security Model: Bell-LaPadula

The Bell-LaPadula model enforces data confidentiality by restricting information flow based on security levels.
- **Application:**
    In this project, only users with appropriate rules (e.g., admin) can view or modify sensitive compliance data. Regular users cannot access admin-only data, ensuring "no read up, no write down" as per Bell-LaPadula.

---

*This document demonstrates the application of advanced cybersecurity defense strategies in the HIPAA Checklist project.*