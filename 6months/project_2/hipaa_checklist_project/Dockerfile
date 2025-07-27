# build frontend
FROM node:20-alpine AS frontend
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend .
RUN npm run build

FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN apt-get update && apt-get install -y nginx && pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY --from=frontend /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
ENV PYTHONUNBUFFERED=1
EXPOSE 80
CMD sh -c "gunicorn backend.hipaa_checklist.wsgi:application --chdir backend --bind 0.0.0.0:8000 & nginx -g 'daemon off;'" 