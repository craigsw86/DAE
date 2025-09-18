# Multi-stage build for HIPAA Checklist Project
# Stage 1: Frontend build
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend .
RUN npm run build

# Stage 2: Backend build
FROM python:3.11-slim AS backend
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Create necessary directories
RUN mkdir -p /app/logs /app/backups /app/ssl

# Set proper permissions
RUN chown -R www-data:www-data /app
RUN chmod -R 755 /app

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=hipaa_checklist.production_settings

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Default command
CMD ["python", "backend/waitress_server.py"]

# Stage 3: Production image with Nginx
FROM nginx:alpine AS production
WORKDIR /app

# Install additional tools
RUN apk add --no-cache curl

# Copy nginx configuration
COPY nginx-https.conf /etc/nginx/nginx.conf

# Copy SSL certificates (if they exist)
COPY ssl/ /etc/nginx/ssl/

# Copy frontend build
COPY --from=frontend /app/build /usr/share/nginx/html

# Copy backend static files
COPY --from=backend /app/backend/staticfiles /app/backend/staticfiles

# Create nginx user and set permissions
RUN adduser -D -s /bin/sh nginx && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /app

# Expose ports
EXPOSE 80 443

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 