"""
Government Scheme Eligibility Finder — Flask Backend
=====================================================
Routes:
  GET  /api/schemes                  — list all schemes (summary)
  GET  /api/schemes/<id>             — scheme detail + documents + steps
  GET  /api/categories               — distinct category list
  POST /api/check                    — eligibility check (main endpoint)
  GET  /api/stats                    — aggregate stats from checks table
  GET  /                             — serve frontend HTML
"""

import sqlite3, json, hashlib, os
from flask import Flask, request, jsonify, g, send_from_directory
from eligibility import evaluate

BASE   = os.path.dirname(__file__)
DB     = os.path.join(BASE, "schemes.db")
STATIC = os.path.join(BASE, "static")

app = Flask(__name__, static_folder=STATIC)
app.config["JSON_AS_ASCII"] = False


# ─── DB helpers ────────────────────────────────────────────────────────────

def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DB)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

@app.teardown_appcontext
def close_db(_):
    db = g.pop("db", None)
    if db: db.close()

def q(sql, params=()):
    return get_db().execute(sql, params).fetchall()

def q1(sql, params=()):
    return get_db().execute(sql, params).fetchone()


# ─── CORS (manual, no flask-cors needed) ────────────────────────────────────

@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return resp

@app.route("/api/<path:p>", methods=["OPTIONS"])
def options(_p):
    return "", 204


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(STATIC, filename)


@app.route("/api/categories")
def categories():
    rows = q("SELECT DISTINCT category FROM schemes ORDER BY category")
    return jsonify([r["category"] for r in rows])


@app.route("/api/schemes")
def schemes_list():
    cat = request.args.get("category")
    if cat:
        rows = q("SELECT id,name,full_name,ministry,category,icon,benefit FROM schemes WHERE category=? ORDER BY name", (cat,))
    else:
        rows = q("SELECT id,name,full_name,ministry,category,icon,benefit FROM schemes ORDER BY category,name")
    return jsonify([dict(r) for r in rows])


@app.route("/api/schemes/<scheme_id>")
def scheme_detail(scheme_id):
    row = q1("SELECT * FROM schemes WHERE id=?", (scheme_id,))
    if not row:
        return jsonify({"error": "Scheme not found"}), 404
    d = dict(row)
    d["documents"]        = json.loads(d["documents"])
    d["apply_steps"]      = json.loads(d["apply_steps"])
    d["eligibility_rules"] = json.loads(d["eligibility_rules"])
    return jsonify(d)


@app.route("/api/check", methods=["POST"])
def check():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "JSON body required"}), 400

    # ── Validate required fields ─────────────────────────────────────────────
    required = ["age", "gender", "income", "state", "category", "occupation"]
    missing  = [f for f in required if body.get(f) in (None, "", 0)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 422

    # ── Normalize user profile ────────────────────────────────────────────────
    user = {
        "age":        int(body.get("age", 0)),
        "gender":     body.get("gender", "").lower(),
        "income":     int(body.get("income", 0)),
        "state":      body.get("state", ""),
        "category":   body.get("category", "").lower(),
        "occupation": body.get("occupation", "").lower(),
        "marital":    body.get("marital", "").lower(),
        "land":       float(body.get("land", 0)),
        "extras":     body.get("extras", []),
    }

    # ── Deterministic user hash (for analytics, no PII stored) ───────────────
    user_hash = hashlib.sha256(
        json.dumps({k: v for k, v in user.items() if k != "extras"}, sort_keys=True).encode()
    ).hexdigest()[:16]

    # ── Evaluate all schemes ─────────────────────────────────────────────────
    all_schemes = q("SELECT * FROM schemes ORDER BY name")
    results     = []
    db          = get_db()

    for scheme in all_schemes:
        ev = evaluate(scheme, user)

        # Persist to analytics table
        db.execute(
            "INSERT INTO eligibility_checks (user_hash, scheme_id, status, met_criteria, total_criteria) VALUES (?,?,?,?,?)",
            (user_hash, scheme["id"], ev["status"], ev["met_count"], ev["total"])
        )

        results.append({
            "scheme": {
                "id":       scheme["id"],
                "name":     scheme["name"],
                "full_name": scheme["full_name"],
                "ministry": scheme["ministry"],
                "category": scheme["category"],
                "icon":     scheme["icon"],
                "benefit":  scheme["benefit"],
                "link":     scheme["link"],
            },
            "status":    ev["status"],
            "criteria":  ev["criteria"],
            "missing":   ev["missing"],
            "met_count": ev["met_count"],
            "total":     ev["total"],
        })

    db.commit()

    # Sort: eligible → almost → not_eligible, then by met_count desc
    order = {"eligible": 0, "almost": 1, "not_eligible": 2}
    results.sort(key=lambda r: (order[r["status"]], -r["met_count"]))

    summary = {
        "eligible":    sum(1 for r in results if r["status"] == "eligible"),
        "almost":      sum(1 for r in results if r["status"] == "almost"),
        "not_eligible": sum(1 for r in results if r["status"] == "not_eligible"),
        "total":       len(results),
    }

    return jsonify({"summary": summary, "results": results})


@app.route("/api/stats")
def stats():
    total_checks  = q1("SELECT COUNT(DISTINCT user_hash) as c FROM eligibility_checks")["c"]
    top_eligible  = q("""
        SELECT s.name, s.category, COUNT(*) as c
        FROM eligibility_checks ec JOIN schemes s ON ec.scheme_id=s.id
        WHERE ec.status='eligible'
        GROUP BY ec.scheme_id ORDER BY c DESC LIMIT 5
    """)
    most_searched = q("""
        SELECT s.name, COUNT(*) as c
        FROM eligibility_checks ec JOIN schemes s ON ec.scheme_id=s.id
        GROUP BY ec.scheme_id ORDER BY c DESC LIMIT 5
    """)
    by_category   = q("""
        SELECT s.category, ec.status, COUNT(*) as c
        FROM eligibility_checks ec JOIN schemes s ON ec.scheme_id=s.id
        GROUP BY s.category, ec.status
    """)
    return jsonify({
        "total_checks":  total_checks,
        "top_eligible":  [dict(r) for r in top_eligible],
        "most_searched": [dict(r) for r in most_searched],
        "by_category":   [dict(r) for r in by_category],
    })


# ─── Boot ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not os.path.exists(DB):
        from db_init import init_db
        init_db()

port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
