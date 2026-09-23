"""
Simple URL Shortener
---------------------
Flask backend that:
  - Accepts a long URL via API (or the web form)
  - Generates a unique short code
  - Stores the mapping in a SQLite database
  - Redirects short codes to their original long URL
"""

import re
import sqlite3
import string
import random
from datetime import datetime
from pathlib import Path

from flask import Flask, request, jsonify, redirect, render_template, g, abort

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "shortener.db"
SHORT_CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits  # a-zA-Z0-9

app = Flask(__name__)


# --------------------------------------------------------------------------
# Database helpers
# --------------------------------------------------------------------------
def get_db():
    """Get a per-request SQLite connection."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create the urls table if it doesn't already exist."""
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                created_at TEXT NOT NULL,
                clicks INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.commit()


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
URL_REGEX = re.compile(
    r"^(https?://)?"  # optional scheme
    r"([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"  # domain
    r"(:\d+)?(/.*)?$"  # optional port + path
)


def is_valid_url(url: str) -> bool:
    return bool(url) and bool(URL_REGEX.match(url.strip()))


def normalize_url(url: str) -> str:
    """Add https:// if the URL has no scheme."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    """Generate a random alphanumeric short code, guaranteed unique."""
    db = get_db()
    while True:
        code = "".join(random.choices(ALPHABET, k=length))
        existing = db.execute(
            "SELECT 1 FROM urls WHERE short_code = ?", (code,)
        ).fetchone()
        if not existing:
            return code


# --------------------------------------------------------------------------
# Routes - Frontend
# --------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------------------------------
# Routes - API
# --------------------------------------------------------------------------
@app.route("/api/shorten", methods=["POST"])
def shorten_url():
    """
    Accepts JSON: { "url": "https://example.com/very/long/path", "custom_code": "optional" }
    Returns JSON: { "short_code": "abc123", "short_url": ".../abc123", "original_url": "..." }
    """
    data = request.get_json(silent=True) or request.form
    original_url = (data.get("url") or "").strip()
    custom_code = (data.get("custom_code") or "").strip()

    if not original_url:
        return jsonify({"error": "A 'url' field is required."}), 400

    if not is_valid_url(original_url):
        return jsonify({"error": "That doesn't look like a valid URL."}), 400

    original_url = normalize_url(original_url)
    db = get_db()

    # If the same URL was already shortened, return the existing code
    existing = db.execute(
        "SELECT short_code FROM urls WHERE original_url = ?", (original_url,)
    ).fetchone()
    if existing and not custom_code:
        short_code = existing["short_code"]
    else:
        if custom_code:
            if not re.match(r"^[A-Za-z0-9_-]{3,32}$", custom_code):
                return jsonify({
                    "error": "Custom code must be 3-32 chars: letters, numbers, - or _."
                }), 400
            taken = db.execute(
                "SELECT 1 FROM urls WHERE short_code = ?", (custom_code,)
            ).fetchone()
            if taken:
                return jsonify({"error": "That custom code is already taken."}), 409
            short_code = custom_code
        else:
            short_code = generate_short_code()

        db.execute(
            "INSERT INTO urls (short_code, original_url, created_at) VALUES (?, ?, ?)",
            (short_code, original_url, datetime.utcnow().isoformat()),
        )
        db.commit()

    short_url = request.host_url.rstrip("/") + "/" + short_code
    return jsonify({
        "short_code": short_code,
        "short_url": short_url,
        "original_url": original_url,
    }), 201


@app.route("/api/urls", methods=["GET"])
def list_urls():
    """Return all shortened URLs, most recent first (for the frontend table)."""
    db = get_db()
    rows = db.execute(
        "SELECT short_code, original_url, created_at, clicks FROM urls ORDER BY id DESC"
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.route("/api/urls/<short_code>", methods=["DELETE"])
def delete_url(short_code):
    db = get_db()
    result = db.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
    db.commit()
    if result.rowcount == 0:
        return jsonify({"error": "Short code not found."}), 404
    return jsonify({"message": "Deleted."}), 200


# --------------------------------------------------------------------------
# Routes - Redirect
# --------------------------------------------------------------------------
@app.route("/<short_code>")
def redirect_to_url(short_code):
    db = get_db()
    row = db.execute(
        "SELECT original_url FROM urls WHERE short_code = ?", (short_code,)
    ).fetchone()
    if row is None:
        abort(404)

    db.execute(
        "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (short_code,)
    )
    db.commit()
    return redirect(row["original_url"])


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Short URL not found."}), 404


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
init_db()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
