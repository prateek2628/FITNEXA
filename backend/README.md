# FitNexa — Complete Student Project Starter

This package preserves the supplied FitNexa landing page and adds a working web app screen plus a Python API backend.

## Features included
- Original responsive landing page.
- App dashboard page (`FitNexa-landing/app.html`) connected to the API.
- FastAPI backend with interactive docs and input validation.
- SQLite persistence for profiles and generated workout plans.
- Rule-based workout generator with equipment/level options.
- Rough nutrition energy estimate for educational use.
- Optional LLM-powered fitness coach via OpenAI API; fallback mode works without a key.
- Workout history endpoint and starter tests.

## Run on Windows (PowerShell)
1. Extract the ZIP and open `TASK 2` in VS Code.
2. In the terminal, run:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```

If `Copy-Item` says `.env` already exists, that's fine. If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again.

3. Open API docs at http://127.0.0.1:8000/docs.
4. Open `FitNexa-landing/app.html` with VS Code Live Server (recommended). Usually it runs at http://127.0.0.1:5500/app.html. If your port differs, set `FRONTEND_ORIGIN` in `backend/.env` to that origin and restart the API. The backend also permits `null` origin for directly opened local files, though Live Server is preferred.
5. Click Save profile, Generate workout, Estimate calories, and Ask FitNexa AI.

## Enable real generated AI replies
1. Obtain an API key from your chosen provider. This may require a paid account; no key is included in this ZIP.
2. Add `OPENAI_API_KEY=your_key_here` to `backend/.env`.
3. Optionally set `OPENAI_MODEL` to a model available to your account.
4. Restart Uvicorn. Never commit `.env` or publish your API key.

The app works without a key, but the coach uses a fallback response. Workout generation is currently rule-based and is not presented as AI-generated.

## Project structure
- `FitNexa-landing/index.html`: marketing landing page
- `FitNexa-landing/app.html`: working app interface
- `FitNexa-landing/app.css`, `app.js`: app styles and API integration
- `backend/app/main.py`: API routes
- `backend/app/models.py`: SQLAlchemy database tables
- `backend/app/services.py`: workout, nutrition, and coach logic
- `backend/.env.example`: configuration template

## Important limitations before public deployment
This is a functional learning prototype, not production-hardened or multi-user secure yet. Add authentication, user-specific authorization, rate limiting, migrations, backups, monitoring, automated integration tests, and production secrets management before exposing it publicly. Health/nutrition responses are educational estimates, not medical advice. Do not claim real wearable integrations or real-time biometric tracking: those are not implemented in this version.
