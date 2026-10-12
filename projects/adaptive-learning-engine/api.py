"""Educational FastAPI quiz service; in-memory sessions, no personal data."""
from uuid import uuid4
from threading import Lock
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from engine import Progress

app = FastAPI(title="Adaptive Learning Engine", version="1.0.0")
sessions: dict[str,Progress] = {}
lock = Lock()

class AnswerIn(BaseModel):
    question_id: str = Field(min_length=1)
    choice: int = Field(ge=0)

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/sessions", status_code=201)
def create_session():
    with lock:
        sid = str(uuid4())
        sessions[sid] = Progress()
    return {"session_id":sid,"message":"Session stored in memory"}

@app.get("/sessions/{sid}/next")
def next_question(sid: str):
    with lock:
        state = sessions.get(sid)
        if state is None: raise HTTPException(404,"Session not found")
        q = state.next_question()
        return {"question_id":q.id,"skill":q.skill,"prompt":q.prompt,
                "options":q.options,"progress_turn":state.turn}

@app.post("/sessions/{sid}/answer")
def answer(sid: str, payload: AnswerIn):
    with lock:
        state = sessions.get(sid)
        if state is None: raise HTTPException(404,"Session not found")
        try: return state.answer(payload.question_id,payload.choice)
        except ValueError as exc: raise HTTPException(400,str(exc)) from exc

@app.get("/sessions/{sid}/progress")
def progress(sid: str):
    with lock:
        state = sessions.get(sid)
        if state is None: raise HTTPException(404,"Session not found")
        return {"turn":state.turn,"skill_mastery":state.skill_mastery(),
                "questions_attempted":len(state.attempts)}
