"""FastAPI prediction endpoint over an Iris baseline model."""
from fastapi import FastAPI
from pydantic import BaseModel, Field
from service import predict, train_model

app = FastAPI(title="Iris Model Service", version="1.0.0")

class IrisFeatures(BaseModel):
    sepal_length: float = Field(gt=0)
    sepal_width: float = Field(gt=0)
    petal_length: float = Field(gt=0)
    petal_width: float = Field(gt=0)

@app.get("/health")
def health():
    _, test_accuracy = train_model()
    return {"status": "ok", "baseline_test_accuracy": test_accuracy}

@app.post("/predict")
def classify(item: IrisFeatures):
    return {"class_index": predict(list(item.model_dump().values())), "dataset": "iris"}
