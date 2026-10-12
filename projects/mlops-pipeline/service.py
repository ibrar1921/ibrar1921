"""Tiny reproducible model training and inference core."""
from functools import lru_cache
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

@lru_cache(maxsize=1)
def train_model():
    features, labels = load_iris(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.25, random_state=42, stratify=labels
    )
    model = LogisticRegression(max_iter=500, random_state=42)
    model.fit(x_train, y_train)
    return model, float(accuracy_score(y_test, model.predict(x_test)))

def predict(features):
    model, _ = train_model()
    return int(model.predict([features])[0])
