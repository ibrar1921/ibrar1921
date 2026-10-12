"""Educational clinical-feature classification demo; never for diagnosis."""
import argparse
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

def run(seed=42):
    # Built-in data is a general classification benchmark, NOT cardiovascular data.
    dataset = load_breast_cancer()
    x_train, x_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.25, random_state=seed,
        stratify=dataset.target
    )
    model = RandomForestClassifier(n_estimators=150, random_state=seed)
    model.fit(x_train, y_train)
    probability = model.predict_proba(x_test)[:, 1]
    print("Benchmark dataset: breast cancer (NOT cardiac data)")
    print("ROC AUC:", round(roc_auc_score(y_test, probability), 3))
    print(classification_report(y_test, model.predict(x_test)))
    importance = permutation_importance(model, x_test, y_test, n_repeats=4, random_state=seed)
    for i in np.argsort(importance.importances_mean)[-5:][::-1]:
        print(f"{dataset.feature_names[i]}: {importance.importances_mean[i]:.4f}")
    return model

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    run(parser.parse_args().seed)
