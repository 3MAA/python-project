# Math Microservice API

This project is a complete microservice solution for executing and displaying mathematical operations, both via API and a modern Web UI.

---

## Features

| Functionality                | Status |
|-----------------------------|--------|
| REST API (FastAPI)          | ✅     |
| Operations: pow, fib, factorial | ✅ |
| Persistent Task Queue (SQLite)          | ✅     |
| Background Worker (Python)              | ✅     |
| Result caching              | ✅     |
| Error handling   | ✅     |
| Web UI (HTML + JS)          | ✅     |
| Responsive styling          | ✅     |
| MVCS architecture           | ✅     |

---

## Tech Stack

- Python 3.10+
- FastAPI
- Pydantic
- SQLite
- Uvicorn
- Vanilla JS + HTML + CSS

---

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate  # or source .venv/bin/activate
pip install -r requirements.txt
```

---

## ▶Run the API + Worker

#### Start the API (and web interface):
```bash
uvicorn app.main:app --reload
```

#### Start the background worker (in a new terminal):
```bash
python -m app.worker
```

#### Then open in browser:

```
http://localhost:8000/
```

---

## Web UI Overview

- ✅ Interactive inputs for pow, fib, factorial
- ✅ Displays results and errors in real-time
- ✅ Load full operation history
- ✅ Styled with clean, modern layout

---

## API Endpoints

| Method | Endpoint        | Payload Example               |
|--------|------------------|-------------------------------|
| POST   | `/api/pow`       | `{ "base": 2, "exp": 5 }`     |
| POST   | `/api/fib`       | `{ "n": 10 }`                 |
| POST   | `/api/factorial` | `{ "n": 5 }`                  |
| GET    | `/api/history`   | Returns all saved operations  |

---

## Project structure

```
math_api_project/
├── app/
│   ├── main.py
│   ├── api.py
│   ├── models.py
│   ├── services.py
│   ├── database.py
│   └── static/
│       └── index.html
├── operations.db
├── requirements.txt
└── README.md
```

---

## Notes

- Worker processes tasks asynchronously and caches results.
- Negative inputs return validation errors with UI messages.


---
