# Country Currency & Exchange API (Flask + SQLite)

## Setup
1. Clone repository
2. Copy `.env.example` to `.env` and adjust if needed
3. Create virtual environment:
   python3 -m venv venv
   source venv/bin/activate
4. Install dependencies:
   pip install -r requirements.txt

## Run locally
   python app.py
App will run at http://127.0.0.1:5000

## Endpoints
- POST /countries/refresh  → fetch & cache countries + exchange rates
- GET  /countries          → list countries (filters: ?region= & ?currency= & ?sort=gdp_desc)
- GET  /countries/<name>   → get country by name (case-insensitive)
- DELETE /countries/<name> → delete a country (case-insensitive)
- GET /status              → { total_countries, last_refreshed_at }
- GET /countries/image     → serve cache/summary.png

## Notes
- If external APIs fail, `/countries/refresh` returns 503 and does not modify DB.
- Image is written to `cache/summary.png` when refresh succeeds.

