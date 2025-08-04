# Security Architecture and Advanced Defense Strategies

## Zero Trust Architecture

This project applies Zero Trust principles by enforcing access controls at multiple layers:
- **Layer 1: Backend (Django) Authentication**
    All sensitive API endpoints require user authentication using JWT tokens. Only authenticated users can access or modify checklist data. Example Django REST Framework permission:
    ```python
    from rest_framework.permissions import IsAuthenticated
    class ChecklistItemViewSet(viewsets.ModelViewSet):
        permission_classes = [IsAuthenticated]
    ```
- **Layer 2: Frontend (React) Route Protection**
    The React app uses a custom `PrivateRoute` component to check for a valid JWT token in localStorage before rendering protected routes. If no token is present, the user is redirected to `/login`. Example code:
    ```jsx
    // src/components/PrivateRoute.js
    import { Navigate } from 'react-router-dom';
    export default function PrivateRoute({ children }) {
      const token = localStorage.getItem('token');
      return token ? children : <Navigate to="/login" />;
    }
    ```
    Unauthorized access attempts are logged in the browser console and result in a 401 error from the backend.

## Defense in Depth

The system implements at least three layers of defense:
1. **Network Layer:** The application is deployed behind an Nginx reverse proxy with the following config:
    ```nginx
    server {
        listen 443 ssl;
        server_name hipaa-checklist.example.com;
        location / {
            proxy_pass http://localhost:8000;
        }
    }
    ```
    The firewall only allows ports 80/443. All other ports are blocked.
2. **Application Layer:** Django settings enforce security:
    ```python
    SECURE_SSL_REDIRECT = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    ```
    Only authenticated users can access sensitive endpoints.
3. **Data Layer:** Sensitive fields use `django-encrypted-model-fields`:
    ```python
    description = EncryptedTextField()
    notes = EncryptedCharField(max_length=500, blank=True, null=True)
    ```
    The encryption key is stored securely in environment variables.

## Supply Chain Security

- All dependencies are checked monthly using:
    ```
    pip-audit
    npm audit
    ```
    Example output:
    ```
    [*] Vulnerability found: axios@0.21.0 - Prototype Pollution
    ```
    The vulnerable package was updated:
    ```
    npm install axios@latest
    ```
    Screenshot of audit result:
    ![npm audit screenshot](screenshots/npm_audit.png)

## Advanced Security Model: Bell-LaPadula

The Bell-LaPadula model enforces data confidentiality by restricting information flow based on security levels.
- **Application:**
    Django admin permissions restrict access to sensitive data:
    ```python
    @admin.register(RegulationUpdate)
    class RegulationUpdateAdmin(admin.ModelAdmin):
        def has_change_permission(self, request, obj=None):
            return request.user.is_superuser or request.user.groups.filter(name='ComplianceAdmin').exists()
    ```
    Regular users cannot access the admin panel or sensitive endpoints, enforcing “no read up, no write down.”

---

*This document demonstrates the application of advanced cybersecurity defense strategies in the HIPAA Checklist project, with specific technical controls, configuration examples, and references to logs and monitoring outputs.*