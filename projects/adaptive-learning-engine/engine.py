"""Rule-based adaptive practice engine; NOT trained machine learning."""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Question:
    id: str
    skill: str
    prompt: str
    options: tuple[str, ...]
    correct: int
    explanation: str

QUESTIONS = (
    Question("PY1","python","What does len([2,4,6]) return?",("2","3","6","Error"),1,"len counts list elements."),
    Question("PY2","python","Which type is immutable?",("list","dict","tuple","set"),2,"Tuple elements cannot be reassigned."),
    Question("PY3","python","What does a generator enable?",("Eager load","Lazy iteration","Index creation","Encryption"),1,"Generators yield on demand."),
    Question("PY4","python","What is a context manager useful for?",("Resource cleanup","Inheritance","Routing","Type hints"),0,"Context managers manage enter/exit logic."),
    Question("SQL1","sql","Which SQL clause filters rows?",("GROUP BY","ORDER BY","WHERE","JOIN"),2,"WHERE filters rows."),
    Question("SQL2","sql","What does LEFT JOIN preserve?",("All right rows","All left rows","Only matches","No NULLs"),1,"All left-table records are retained."),
    Question("SQL3","sql","Which action completes a transaction?",("Rollback","Commit","Filter","Index"),1,"A commit makes changes durable."),
    Question("SQL4","sql","What can an index improve?",("Query lookup","Image size","Auth strength","Compression"),0,"Indexes accelerate selected lookup patterns."),
    Question("ML1","machine_learning","What is data leakage?",("Model storage","Future or test data influencing training","Cross validation","Encoding"),1,"Leakage invalidates evaluation."),
    Question("ML2","machine_learning","What does MAE stand for?",("Mean absolute error","Maximum absolute entropy","Model accuracy","Median accuracy"),0,"Mean of absolute prediction errors."),
    Question("ML3","machine_learning","What is a holdout set for?",("Training all parameters","Estimating generalization","Data cleanup","Feature scaling"),1,"Holdout estimates unseen-data performance."),
    Question("ML4","machine_learning","What does calibration evaluate?",("Confidence reliability","Training speed","Feature count","Model size"),0,"Predicted frequencies should align with observed frequencies."),
)
BY_ID = {q.id: q for q in QUESTIONS}

@dataclass
class Progress:
    attempts: dict[str,int] = field(default_factory=dict)
    correct: dict[str,int] = field(default_factory=dict)
    due_at: dict[str,int] = field(default_factory=dict)
    streaks: dict[str,int] = field(default_factory=dict)
    turn: int = 0
    current: str | None = None

    def skill_mastery(self):
        totals = {skill: [0,0] for skill in {q.skill for q in QUESTIONS}}
        for q in QUESTIONS:
            totals[q.skill][0] += self.correct.get(q.id,0)
            totals[q.skill][1] += self.attempts.get(q.id,0)
        return {skill: round((correct+1)/(attempts+2),3)
                for skill,(correct,attempts) in sorted(totals.items())}

    def next_question(self):
        if self.current is not None: return BY_ID[self.current]
        mastery = self.skill_mastery()
        due = [q for q in QUESTIONS if self.due_at.get(q.id,0) <= self.turn]
        if not due: due = list(QUESTIONS)
        ranked = sorted(due, key=lambda q: (
            self.due_at.get(q.id,0) > self.turn,
            self.attempts.get(q.id,0) > 0,
            mastery[q.skill], self.attempts.get(q.id,0), q.id))
        self.current = ranked[0].id
        return ranked[0]

    def answer(self, question_id, choice):
        if self.current != question_id: raise ValueError("Answer only the current question")
        q = BY_ID[question_id]
        if not 0 <= choice < len(q.options): raise ValueError("Choice index outside options")
        right = choice == q.correct
        self.attempts[q.id] = self.attempts.get(q.id,0)+1
        self.correct[q.id] = self.correct.get(q.id,0)+int(right)
        streak = self.streaks.get(q.id,0)+1 if right else 0
        self.streaks[q.id] = streak
        self.turn += 1
        self.due_at[q.id] = self.turn + (min(2**streak,32) if right else 1)
        self.current = None
        return {"correct":right,"correct_choice":q.correct,"explanation":q.explanation,
                "mastery":self.skill_mastery(),"next_review_turn":self.due_at[q.id]}
