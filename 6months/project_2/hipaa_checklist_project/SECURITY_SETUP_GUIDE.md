# 🔐 Security Setup Guide

## ⚠️ CRITICAL: Before Pushing to GitHub

This project contains sensitive information that MUST be secured before pushing to GitHub.

## 🚨 Security Issues Fixed

The following security vulnerabilities have been addressed:

1. **Hardcoded Django Secret Keys** - Now use environment variables
2. **Hardcoded Database Encryption Passwords** - Now use environment variables  
3. **Hardcoded Field Encryption Keys** - Now use environment variables
4. **Test Credentials** - Removed sensitive test files
5. **Docker Compose Secrets** - Now use environment variables

## 🛡️ How to Set Up Environment Variables

### 1. Create a `.env` file in your project root:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=hipaa_checklist.settings

# Database Settings
DATABASE_URL=sqlite:///db.sqlite3
DB_ENCRYPTION_PASSWORD=your-database-encryption-password-here

# Field Encryption
FIELD_ENCRYPTION_KEY=your-44-character-encryption-key-here

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key-here

# Email Settings (for production)
EMAIL_HOST=your-smtp-host
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

# Server Settings
WAITRESS_HOST=0.0.0.0
WAITRESS_PORT=8000
WAITRESS_THREADS=4

# React Settings
REACT_APP_API_BASE_URL=http://localhost:8000
```

### 2. Generate Secure Keys

#### Django Secret Key:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Field Encryption Key:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

#### JWT Secret Key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Set Environment Variables

#### Windows (PowerShell):
```powershell
$env:SECRET_KEY="your-secret-key"
$env:DB_ENCRYPTION_PASSWORD="your-db-password"
$env:FIELD_ENCRYPTION_KEY="your-encryption-key"
```

#### Windows (CMD):
```cmd
set SECRET_KEY=your-secret-key
set DB_ENCRYPTION_PASSWORD=your-db-password
set FIELD_ENCRYPTION_KEY=your-encryption-key
```

#### Linux/Mac:
```bash
export SECRET_KEY="your-secret-key"
export DB_ENCRYPTION_PASSWORD="your-db-password"
export FIELD_ENCRYPTION_KEY="your-encryption-key"
```

## 🔒 Production Deployment

### For Production Servers:

1. **Never commit `.env` files to version control**
2. **Use a secure secret management system** (AWS Secrets Manager, Azure Key Vault, etc.)
3. **Rotate keys regularly**
4. **Use HTTPS in production**
5. **Set DEBUG=False in production**

### Docker Deployment:

```bash
# Create a .env file with your secrets
cp env.template .env
# Edit .env with your actual values
# Then run:
docker-compose up -d
```

## 🚫 Files That Should Never Be Committed:

- `.env` files
- `*.secret` files
- `*_tokens.txt` files
- `logs/` directory
- `reports/` directory
- Any file containing passwords, keys, or tokens

## ✅ Verification Checklist:

- [ ] All hardcoded secrets removed
- [ ] Environment variables configured
- [ ] `.env` file created (not committed)
- [ ] `.gitignore` updated
- [ ] Test files with credentials removed
- [ ] Docker files use environment variables
- [ ] Production settings use environment variables

## 🆘 If You Accidentally Commit Secrets:

1. **Immediately rotate all exposed secrets**
2. **Remove the commit from history**:
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch path/to/secret/file' HEAD
   ```
3. **Force push** (if already pushed):
   ```bash
   git push origin --force
   ```
4. **Consider the secrets compromised** and generate new ones

## 📞 Support

If you need help with security setup, refer to:
- Django Security Documentation
- OWASP Security Guidelines
- Your organization's security policies
