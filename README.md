# PocketSmart AI

Full-stack implementation of the supplied PocketSmart AI specification.

Stack:
- FastAPI + Uvicorn
- Jinja2 + HTML/CSS/JavaScript
- SQLite locally / PostgreSQL-ready
- Gemini API
- JWT authentication
- Recommendation history
- Home, Party and Jewelry planners
- Optional outfit image analysis
- Fallback recommendations

## Run on Windows

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

API docs: http://127.0.0.1:8000/docs

The supplied PDF permits mock/simulated marketplace sourcing. This implementation therefore creates search links for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO rather than pretending prices or inventory are live/verified.
