# Anwara Memorial Hospital & Diagnostic Center

Responsive bilingual hospital website with a FastAPI + MongoDB appointment backend and cookie-session admin workspace.

## Render deployment

This project is prepared as a **single Render Web Service**. The service builds the React frontend and then FastAPI serves the generated frontend and `/api/*` endpoints from the same origin. This keeps the admin session cookie same-origin and avoids a separate frontend/backend CORS setup.

### 1. Create MongoDB Atlas database

Create a MongoDB database and copy its connection string. Use a dedicated database user and restrict network access appropriately for your deployment.

### 2. Deploy to Render

Push this repository to GitHub, then create a Render Web Service from the repository. Render can also use the included `render.yaml` as the service blueprint.

The important commands are already configured:

```text
Build: pip install -r backend/requirements.txt && cd frontend && npm install && npm run build
Start: cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT
```

### 3. Set Render environment variables

Set these in Render's Environment section. Do not commit the real values.

```text
MONGO_URL=<your MongoDB Atlas connection string>
DB_NAME=anwara_hospital
APP_TZ=Asia/Dhaka
SESSION_DAYS=7
COOKIE_SECURE=true
ADMIN_EMAIL=<your admin email>
ADMIN_PASSWORD=<a long unique admin password>
ADMIN_NAME=Anwara Hospital Admin
```

On the first successful startup, the backend creates the admin account if the configured email does not already exist.

### 4. Verify deployment

After deployment:

- Public site: `/`
- Admin login: `/admin/login`
- Admin dashboard: `/admin`
- API health: `/api/health`
- API documentation: `/api/docs`

The `/api/health` response should be:

```json
{"status":"ok","service":"anwara-memorial-hospital"}
```

## Local setup

### Backend

1. Copy `backend/.env.example` to `backend/.env`.
2. Set `MONGO_URL`, `DB_NAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD`.
3. Install: `pip install -r backend/requirements.txt`.
4. Run: `cd backend && uvicorn server:app --reload --port 8000`.

### Frontend

1. `cd frontend`
2. `npm install`
3. `npm run dev`

Open `http://localhost:5173`.

## Security notes

- Never commit `backend/.env`, real passwords, or production MongoDB credentials.
- Use a long unique `ADMIN_PASSWORD` in Render.
- Production uses `COOKIE_SECURE=true` so the admin session cookie is sent only over HTTPS.
- MongoDB should use a dedicated database user with only the permissions required by this application.
- The admin session token is stored as a SHA-256 hash in MongoDB rather than as the raw cookie value.
