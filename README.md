# ⚖ Yojana Mitra — Government Scheme Eligibility Finder

A full-stack web application that checks a user's eligibility across 13 Indian central government schemes, classifying results as **Eligible**, **Almost Eligible**, or **Not Eligible** with detailed per-criterion explanations.

---

## Tech Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python 3 + Flask                    |
| Database  | SQLite 3 (via Python stdlib)        |
| Frontend  | Vanilla HTML/CSS/JS (no frameworks) |
| Fonts     | Google Fonts (Libre Baskerville + Plus Jakarta Sans) |

No external Python packages beyond Flask are required.

---

## Project Structure

```
scheme-finder/
├── app.py           # Flask API server + route handlers
├── eligibility.py   # Eligibility engine (operator-based rule evaluator)
├── db_init.py       # DB schema + 13 scheme seed data
├── schemes.db       # SQLite database (auto-created on first run)
├── start.sh         # One-command startup script
├── static/
│   └── index.html   # Full frontend SPA (3 pages)
└── README.md
```

---

## Quick Start

### Option 1 — Shell script (recommended)
```bash
chmod +x start.sh
./start.sh
```

### Option 2 — Manual
```bash
python3 db_init.py        # create + seed the database
python3 app.py            # start the Flask server
```

Then open **http://localhost:5000** in your browser.

---

## API Endpoints

| Method | Endpoint               | Description                              |
|--------|------------------------|------------------------------------------|
| GET    | `/`                    | Serve the frontend SPA                   |
| GET    | `/api/schemes`         | List all schemes (optional `?category=`) |
| GET    | `/api/schemes/<id>`    | Full scheme detail (docs, steps, rules)  |
| GET    | `/api/categories`      | List distinct categories                 |
| POST   | `/api/check`           | **Main eligibility check endpoint**      |
| GET    | `/api/stats`           | Anonymized usage analytics               |

### POST /api/check — Request Body

```json
{
  "age":        28,
  "gender":     "female",
  "income":     120000,
  "state":      "Bihar",
  "category":   "sc",
  "occupation": "farmer",
  "marital":    "married",
  "land":       2.5,
  "extras":     ["bank-account", "bpl", "ration-card", "no-house"]
}
```

**extras** values: `bpl`, `disabled`, `no-house`, `ration-card`, `bank-account`, `class-10`, `class-12`, `graduate`

### POST /api/check — Response

```json
{
  "summary": { "eligible": 11, "almost": 1, "not_eligible": 1, "total": 13 },
  "results": [
    {
      "scheme":    { "id": "pm-kisan", "name": "PM-KISAN", ... },
      "status":    "eligible",
      "criteria":  [ { "label": "Must be a farmer", "met": true, "required": true }, ... ],
      "missing":   [],
      "met_count": 4,
      "total":     4
    },
    ...
  ]
}
```

---

## Eligibility Engine

`eligibility.py` evaluates schemes using a **declarative rule system**. Each scheme stores its rules as a JSON array in the database:

```json
[
  { "field": "occupation", "operator": "eq",       "value": "farmer",              "label": "Must be a farmer",         "required": true  },
  { "field": "income",     "operator": "lte",      "value": 600000,               "label": "Income below ₹6 lakh",     "required": true  },
  { "field": "extras",     "operator": "contains", "value": "bank-account",        "label": "Should have bank account", "required": false }
]
```

**Supported operators:** `eq`, `neq`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in`, `contains`, `contains_any`, `any`

**Status logic:**
- `eligible`     — all `required: true` criteria met
- `almost`       — exactly 1 required criterion unmet
- `not_eligible` — 2+ required criteria unmet

---

## Covered Schemes (13)

| Scheme         | Category   | Benefit                              |
|----------------|------------|--------------------------------------|
| PM-KISAN       | Farmers    | ₹6,000/year income support           |
| PMAY-G         | Housing    | ₹1.2–1.3L house construction grant  |
| Ayushman Bharat | Health    | ₹5L/year health insurance            |
| PMSBY          | Health     | ₹2L accident cover @ ₹20/year        |
| PMJJBY         | Health     | ₹2L life cover @ ₹436/year           |
| NSP Scholarships | Students | ₹3K–12K/year + tuition fee           |
| PMEGP          | Employment | 15–35% subsidy on ₹50L loan          |
| MGNREGS        | Employment | 100 days guaranteed work/year        |
| PM MUDRA       | Employment | Collateral-free loan up to ₹10L      |
| PMKVY 4.0      | Employment | Free skill training + ₹8K reward     |
| Atal Pension   | Employment | ₹1K–5K/month pension after 60        |
| Sukanya Samriddhi | Women  | 8.2% tax-free savings for girl child |
| PM Ujjwala 2.0 | Women      | Free LPG connection + stove          |

---

## Adding a New Scheme

Add a new entry to the `SCHEMES` list in `db_init.py`, then re-run `python3 db_init.py`. No changes to `app.py` or `eligibility.py` are needed.

```python
{
    "id": "my-new-scheme",
    "name": "Scheme Short Name",
    "full_name": "Full Official Name",
    "ministry": "Ministry Name",
    "category": "health",          # farmers|health|housing|students|women|employment
    "icon": "💊",
    "description": "...",
    "benefit": "What the beneficiary gets",
    "link": "https://official-portal.gov.in",
    "documents": json.dumps(["Doc 1", "Doc 2"]),
    "apply_steps": json.dumps(["Step 1", "Step 2"]),
    "eligibility_rules": json.dumps([
        {"field": "age", "operator": "gte", "value": 18, "label": "Age 18+", "required": True},
        {"field": "income", "operator": "lte", "value": 300000, "label": "Income below ₹3L", "required": True},
    ])
}
```

---

## Analytics

Every eligibility check is logged (anonymized via SHA-256 hash of non-PII fields) to the `eligibility_checks` table, enabling the `/api/stats` dashboard showing:
- Total unique checks run
- Most frequently eligible schemes
- Most checked schemes
- Breakdown by category and status
