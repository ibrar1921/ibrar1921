"""Synthetic flight-booking UX study. No original FlyEase participant data."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

FEATURES = ["age_band", "booking_frequency", "checkout_steps", "loading_delay_s", "price_transparency", "payment_errors"]

def generate_synthetic_survey(n: int = 500, seed: int = 42) -> pd.DataFrame:
    if n < 30:
        raise ValueError("n must be at least 30")
    rng = np.random.default_rng(seed)
    age = rng.choice(["18-24", "25-34", "35-49", "50+"], n, p=[.22, .37, .29, .12])
    freq = rng.choice(["rare", "occasional", "frequent"], n, p=[.3, .5, .2])
    steps = rng.integers(3, 11, n)
    delay = np.round(rng.gamma(2.1, 1.2, n), 2)
    transparency = rng.integers(1, 6, n)
    errors = rng.binomial(2, .15, n)
    score = (5.7 - .25 * (steps - 3) - .13 * delay + .32 * (transparency - 3) - .62 * errors
             + .15 * (freq == "frequent") + rng.normal(0, .65, n))
    return pd.DataFrame({"age_band": age, "booking_frequency": freq, "checkout_steps": steps,
        "loading_delay_s": delay, "price_transparency": transparency, "payment_errors": errors,
        "satisfaction": np.clip(score, 1, 5).round(2)})

def evaluate(df: pd.DataFrame, seed: int = 42) -> dict:
    missing = sorted(set(FEATURES + ["satisfaction"]) - set(df.columns))
    if missing: raise ValueError(f"Missing required columns: {missing}")
    if len(df) < 30: raise ValueError("Need at least 30 responses")
    numeric = ["checkout_steps", "loading_delay_s", "price_transparency", "payment_errors"]
    categorical = ["age_band", "booking_frequency"]
    preprocessing = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical)])
    X, y = df[FEATURES], df["satisfaction"].astype(float)
    xtr, xte, ytr, yte = train_test_split(X, y, test_size=.25, random_state=seed)
    model = Pipeline([("preprocess", preprocessing), ("regressor", Ridge(alpha=2.0))])
    model.fit(xtr, ytr)
    baseline = DummyRegressor(strategy="mean").fit(xtr, ytr)
    prediction = model.predict(xte)
    importance = permutation_importance(model, xte, yte, n_repeats=5, random_state=seed,
                                        scoring="neg_mean_absolute_error")
    return {"dataset": "synthetic_flight_booking_ux", "responses": len(df),
        "holdout_responses": len(xte), "ridge_mae": round(float(mean_absolute_error(yte, prediction)), 4),
        "baseline_mae": round(float(mean_absolute_error(yte, baseline.predict(xte))), 4),
        "ridge_r2": round(float(r2_score(yte, prediction)), 4),
        "feature_importance_mae_increase": {k: round(float(v), 4) for k, v in
            sorted(zip(FEATURES, importance.importances_mean), key=lambda p: -p[1])}}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--responses", type=int, default=500)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", type=Path, default=Path("results"))
    args = p.parse_args()
    dataset = generate_synthetic_survey(args.responses, args.seed)
    report = evaluate(dataset, args.seed)
    args.out.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(args.out / "synthetic_survey.csv", index=False)
    (args.out / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))

if __name__ == "__main__": main()
