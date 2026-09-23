# Simple URL Shortener

A minimal URL shortener built with **Flask** + **SQLite**, with a small
vanilla-JS frontend.

## Features
- `POST /api/shorten` — accepts a long URL (and optional custom short code),
  returns a unique short code
- `GET /<short_code>` — redirects to the original long URL, tracks clicks
- `GET /api/urls` — lists all saved mappings
- `DELETE /api/urls/<short_code>` — removes a mapping
- SQLite storage (`shortener.db`, created automatically)
- Basic frontend to submit URLs and see/copy the shortened result

## Setup

```bash
pip install -r requirements.txt
python app.py
```

The app runs at `http://localhost:5000`. Visiting `/` shows the frontend.
The database file `shortener.db` is created automatically on first run.

## API examples

**Shorten a URL**
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/some/very/long/path"}'
```
Response:
```json
{
  "short_code": "aB3xY9",
  "short_url": "http://localhost:5000/aB3xY9",
  "original_url": "https://example.com/some/very/long/path"
}
```

**Use a custom code**
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "custom_code": "my-link"}'
```

**Visit the short link** — open `http://localhost:5000/aB3xY9` in a browser
and it redirects to the original URL.

**List all links**
```bash
curl http://localhost:5000/api/urls
```

## Project structure
```
url-shortener/
├── app.py              # Flask backend (routes, DB logic, redirect)
├── requirements.txt
├── shortener.db         # created automatically on first run
├── templates/
│   └── index.html      # frontend page
└── static/
    ├── style.css
    └── app.js
```

## Notes / possible extensions
- Short codes are 6-character random alphanumeric strings, checked for
  uniqueness against the DB before saving.
- Submitting the same long URL twice returns the existing short code
  (unless you request a custom one).
- To swap SQLite for another DB (e.g. MongoDB/Postgres), only the functions
  in the "Database helpers" section of `app.py` need to change — the routes
  don't touch SQL directly.
