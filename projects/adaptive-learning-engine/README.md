# Adaptive Learning Engine 🧠

A **working FastAPI tutoring prototype** with 12 original practice questions across Python, SQL and ML, a transparent question-scheduling engine, answer feedback and per-skill progress.

### Highlights
- Session creation and REST endpoints for questions, answers and progress.
- Prefers unattempted questions, weaker skills and previously scheduled review items.
- Modified Leitner-style intervals; smoothed success fraction as a simple mastery *estimate*.
- Input validation, locking for in-memory state and testable pure scheduling functions.

### Run
```bash
python -m pip install -r requirements.txt
python -m unittest discover -v
uvicorn api:app --reload
```

Open `http://localhost:8000/docs` and create a session with `POST /sessions`. Then call `GET /sessions/{sid}/next` and `POST /sessions/{sid}/answer` with the returned question ID and an option index.

This is a **rule-based adaptive learning demonstration**, not a trained deep-learning system or a validated educational intervention. All sessions are in memory and disappear when the service restarts. No authentication or persistent storage is supplied.
