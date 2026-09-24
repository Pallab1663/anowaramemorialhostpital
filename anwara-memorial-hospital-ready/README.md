# Anwara Memorial Hospital & Diagnostic Center

Responsive bilingual hospital website with a FastAPI + MongoDB appointment backend and cookie-session admin workspace.

## Local setup

### Backend
1. Copy `backend/.env.example` to `backend/.env`.
2. Set `MONGO_URL`, `DB_NAME`, and a private `ADMIN_PASSWORD`.
3. Install: `pip install -r backend/requirements.txt`.
4. Seed: `ADMIN_EMAIL=admin@anwarahospital.com ADMIN_PASSWORD='your-password' python backend/seed.py`.
5. Run: `cd backend && uvicorn server:app --reload --port 8000`.

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

Open `http://localhost:5173`.

## Routes
- `/` public hospital site
- `/admin/login` admin sign-in
- `/admin` appointment/admin workspace
- `/api/docs` FastAPI API documentation

## Production notes
- Use HTTPS and set `COOKIE_SECURE=true`.
- Never commit `backend/.env` or real credentials.
- Keep MongoDB private and use a dedicated database user.
