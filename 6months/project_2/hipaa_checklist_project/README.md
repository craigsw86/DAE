# HIPAA Checklist Project

## Features
- User authentication (JWT)
- Checklist management (with mitigation steps)
- Regulation updates
- Compliance reporting
- Audit log (viewable in admin and frontend)

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

## Documentation
- See `docs/API.md` for API details.
- See `docs/Risk_Communication.md` for risk comms.


